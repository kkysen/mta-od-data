//! Walks between stations, and from origins to them, in seconds,
//! on OpenStreetMap's streets (the `streets` crate),
//! through stations' entrances, each with its own time between the street and the platforms
//! (`mta-od-data fetch-station-access`'s `data/station_access.csv`).
//!
//! The streets are walked once, for every feed's stations (`StreetWalks`),
//! and each feed takes its own stops' walks from them (`Walks`).
//! Changing trains within a station or complex is left to the timetable;
//! only changes between them walk the streets, out through one entrance and in through another.
//! Moved from `subway-sheds`, which walks from origins too, and draws the walks.

use rayon::iter::{IndexedParallelIterator, IntoParallelRefIterator, ParallelIterator};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use streets::{Graph, Mm, Search, Split};

use crate::gtfs::Secs;
use crate::timetable::{StopIdx, Timetable};

/// Walking on the streets at 3 mph, as R5 does, in millimeters a second.
pub const WALKING_SPEED_MM_PER_S: Mm = 1341;

/// How far apart stations may be to change between them on the streets:
/// about the 1000 m R5 walked between stops, as a time, entrances included.
const TRANSFER_LIMIT: Secs = 15 * 60;

/// A station's entrance: `(latitude, longitude, seconds between it and the platforms)`.
pub type Entrance = (f64, f64, Secs);

/// A station: `(id, complex, entrances)`.
pub type Station = (String, String, Vec<Entrance>);

/// Every walk, from origins and stations by their IDs, whatever feed has them.
pub struct StreetWalks {
    /// Each station's ID, by its index here.
    stations: Vec<String>,
    /// Each station's complex, by its index.
    complexes: Vec<String>,
    /// From each origin to the stations' platforms it walks to, by index.
    access: HashMap<String, Vec<(u32, Secs)>>,
    /// From each station's platforms to other stations' within `TRANSFER_LIMIT`.
    near: Vec<Vec<(u32, Secs)>>,
}

/// One feed's walks, by its stops' indices.
#[derive(Debug, Default)]
pub struct Walks {
    /// From each origin to the stops it walks to.
    pub access: HashMap<String, Vec<(StopIdx, Secs)>>,
    /// `(from, to, walk)` between stops of stations in different complexes.
    pub transfers: Vec<(StopIdx, StopIdx, Secs)>,
    /// Every `(from, to, walk)` between them, to every stop, not just the closest on each pattern,
    /// for telling which station riders walk to apart from which is quickest to board at.
    pub all_transfers: Vec<(StopIdx, StopIdx, Secs)>,
    /// Those of them between complexes changed between free though out of the system,
    /// to every stop, not just the closest on each pattern, which may not be free.
    pub free_transfers: Vec<(StopIdx, StopIdx, Secs)>,
    /// Each stop's complex, to tell which of `transfers.txt`'s footpaths to keep.
    pub complexes: Vec<Option<String>>,
    /// Each stop's station, by its index in `StreetWalks`' stations.
    pub stations: Vec<Option<u32>>,
}

/// A station's entrances on the streets, each with its time to the platforms as a distance.
struct Snapped {
    entrances: Vec<(Split, Mm)>,
}

impl Snapped {
    /// The vertices to search from, starting on the platforms or, with `inside` false, the street.
    fn sources(&self, inside: bool) -> Vec<(u32, Mm)> {
        self.entrances
            .iter()
            .flat_map(|(split, cost)| {
                let cost = if inside { *cost } else { 0 };
                split.ends().map(|(v, d)| (v, d.saturating_add(cost)))
            })
            .collect()
    }

    /// How far the latest search reached this station's platforms, through its entrances.
    fn reached(&self, search: &Search) -> Option<Mm> {
        self.entrances
            .iter()
            .filter_map(|(split, cost)| Some(search.to(split)?.saturating_add(*cost)))
            .min()
    }
}

impl StreetWalks {
    /// The walks from `origins`, by station ID, starting on the street at their entrances,
    /// and between `stations`' platforms,
    /// at `speed` millimeters a second, rounded down to whole seconds,
    /// walking from origins for at most `max_secs`.
    pub fn compute(
        graph: &Graph,
        stations: &[Station],
        origins: &[String],
        speed: Mm,
        max_secs: Secs,
    ) -> Self {
        let secs = |d: Mm| (d / speed) as Secs;
        let mm = |s: Secs| speed.saturating_mul(s as Mm);
        let snapped: Vec<Snapped> = stations
            .iter()
            .map(|(_, _, entrances)| Snapped {
                entrances: entrances
                    .iter()
                    .filter_map(|&(lat, lon, s)| Some((graph.snap(lat, lon)?, mm(s))))
                    .collect(),
            })
            .collect();
        let to_stations = |search: &Search, skip: Option<usize>, limit: Mm| -> Vec<(u32, Secs)> {
            snapped
                .iter()
                .enumerate()
                .filter(|&(t, _)| Some(t) != skip)
                .filter_map(|(t, station)| {
                    let reached = station.reached(search).filter(|&r| r <= limit)?;
                    Some((t as u32, secs(reached)))
                })
                .collect()
        };

        let near = snapped
            .par_iter()
            .enumerate()
            .map_init(
                || Search::new(graph),
                |search, (s, station)| {
                    search.run_from_vertices(&station.sources(true), mm(TRANSFER_LIMIT));
                    to_stations(search, Some(s), mm(TRANSFER_LIMIT))
                },
            )
            .collect();

        let index: HashMap<&str, usize> = stations
            .iter()
            .enumerate()
            .map(|(i, (id, ..))| (id.as_str(), i))
            .collect();
        let walk_limit = mm(max_secs);
        let from_origins: Vec<_> = origins
            .par_iter()
            .map_init(
                || Search::new(graph),
                |search, origin| {
                    let Some(&o) = index.get(origin.as_str()) else {
                        return (origin.clone(), Vec::new());
                    };
                    search.run_from_vertices(&snapped[o].sources(false), walk_limit);
                    (origin.clone(), to_stations(search, None, walk_limit))
                },
            )
            .collect();
        Self {
            stations: stations.iter().map(|(id, ..)| id.clone()).collect(),
            complexes: stations.iter().map(|(_, c, _)| c.clone()).collect(),
            access: from_origins.into_iter().collect(),
            near,
        }
    }
}

impl StreetWalks {
    /// Each station's ID, by its index.
    pub fn stations(&self) -> &[String] {
        &self.stations
    }

    /// Every walk between stations of different complexes, as `(from, to, seconds)`, by their IDs.
    pub fn transfers(&self) -> Vec<(String, String, Secs)> {
        self.near
            .iter()
            .enumerate()
            .flat_map(|(s, near)| near.iter().map(move |&(t, walk)| (s, t as usize, walk)))
            .filter(|&(s, t, _)| self.complexes[s] != self.complexes[t])
            .map(|(s, t, walk)| (self.stations[s].clone(), self.stations[t].clone(), walk))
            .collect()
    }

    /// The complex of the station `id`, if it's one of these.
    pub fn complex(&self, id: &str) -> Option<&str> {
        let i = self.stations.iter().position(|s| s == id)?;
        Some(&self.complexes[i])
    }

    /// Writes these to `path`, to `read` back without walking the streets again,
    /// all little-endian: each station's ID and complex,
    /// each station's walks to others, and each origin's ID and its walks,
    /// each list after its length as a `u32`, and each string as its UTF-8 bytes.
    pub fn write(&self, path: &std::path::Path) -> anyhow::Result<()> {
        let mut out = Vec::new();
        let len = |out: &mut Vec<u8>, n: usize| out.extend((n as u32).to_le_bytes());
        let string = |out: &mut Vec<u8>, s: &str| {
            len(out, s.len());
            out.extend(s.as_bytes());
        };
        let walks = |out: &mut Vec<u8>, walks: &[(u32, Secs)]| {
            len(out, walks.len());
            for &(to, secs) in walks {
                out.extend(to.to_le_bytes());
                out.extend(secs.to_le_bytes());
            }
        };
        len(&mut out, self.stations.len());
        for (id, complex) in self.stations.iter().zip(&self.complexes) {
            string(&mut out, id);
            string(&mut out, complex);
        }
        for near in &self.near {
            walks(&mut out, near);
        }
        // By origin, so the same walks always write the same bytes.
        let mut origins: Vec<_> = self.access.iter().collect();
        origins.sort_unstable_by_key(|(origin, _)| origin.as_str());
        len(&mut out, origins.len());
        for (origin, access) in origins {
            string(&mut out, origin);
            walks(&mut out, access);
        }
        Ok(std::fs::write(path, out)?)
    }

    /// Reads back what `write` wrote to `path`.
    pub fn read(path: &std::path::Path) -> anyhow::Result<Self> {
        let bytes = std::fs::read(path)?;
        let mut r = Reader {
            bytes: &bytes,
            at: 0,
        };
        let n = r.len()?;
        let mut stations = Vec::with_capacity(n);
        let mut complexes = Vec::with_capacity(n);
        for _ in 0..n {
            stations.push(r.string()?);
            complexes.push(r.string()?);
        }
        let near = (0..n).map(|_| r.walks()).collect::<anyhow::Result<_>>()?;
        let origins = r.len()?;
        let access = (0..origins)
            .map(|_| Ok((r.string()?, r.walks()?)))
            .collect::<anyhow::Result<_>>()?;
        if r.at != bytes.len() {
            anyhow::bail!("{} has more than walks", path.display());
        }
        Ok(Self {
            stations,
            complexes,
            access,
            near,
        })
    }
}

#[derive(serde::Deserialize)]
struct AccessRow {
    station: String,
    complex: String,
    lat: f64,
    lon: f64,
    secs: Secs,
}

/// Each station's entrances in `mta-od-data fetch-station-access`'s `station_access.csv`,
/// in the order it first lists them.
pub fn load_stations(path: &std::path::Path) -> anyhow::Result<Vec<Station>> {
    use anyhow::Context;
    let mut reader =
        csv::Reader::from_path(path).with_context(|| format!("opening {}", path.display()))?;
    let mut stations: Vec<Station> = Vec::new();
    let mut index: HashMap<String, usize> = HashMap::default();
    for row in reader.deserialize() {
        let row: AccessRow = row?;
        let i = *index.entry(row.station.clone()).or_insert_with(|| {
            stations.push((row.station.clone(), row.complex.clone(), Vec::new()));
            stations.len() - 1
        });
        stations[i].2.push((row.lat, row.lon, row.secs));
    }
    Ok(stations)
}

/// Reads what `StreetWalks::write` writes, from the start of `bytes`.
struct Reader<'a> {
    bytes: &'a [u8],
    at: usize,
}

impl<'a> Reader<'a> {
    fn take<const N: usize>(&mut self) -> anyhow::Result<[u8; N]> {
        let taken = self.bytes.get(self.at..self.at + N);
        let taken = taken.ok_or_else(|| anyhow::anyhow!("walks end early"))?;
        self.at += N;
        Ok(taken.try_into()?)
    }

    fn len(&mut self) -> anyhow::Result<usize> {
        Ok(u32::from_le_bytes(self.take()?) as usize)
    }

    fn string(&mut self) -> anyhow::Result<String> {
        let n = self.len()?;
        let s = self.bytes.get(self.at..self.at + n);
        let s = s.ok_or_else(|| anyhow::anyhow!("walks end early"))?;
        self.at += n;
        Ok(std::str::from_utf8(s)?.to_owned())
    }

    fn walks(&mut self) -> anyhow::Result<Vec<(u32, Secs)>> {
        let n = self.len()?;
        (0..n)
            .map(|_| {
                Ok((
                    u32::from_le_bytes(self.take()?),
                    Secs::from_le_bytes(self.take()?),
                ))
            })
            .collect()
    }
}

/// Of `reached` stops, only the closest on each of `tts`' patterns, as R5 keeps
/// (`TransferFinder.retainClosestStopsOnPatterns`), the first stop of any tie:
/// walking on to another of a pattern's stops is never quicker than riding to it.
fn closest_on_patterns(tts: &[&Timetable], reached: &[(StopIdx, Secs)]) -> Vec<(StopIdx, Secs)> {
    let at: HashMap<StopIdx, Secs> = reached.iter().copied().collect();
    let mut kept: Vec<(StopIdx, Secs)> = tts
        .iter()
        .flat_map(|tt| &tt.patterns)
        .filter_map(|p| {
            p.stops
                .iter()
                .filter_map(|s| at.get(s).map(|&d| (d, *s)))
                .min()
                .map(|(d, s)| (s, d))
        })
        .collect();
    kept.sort_unstable();
    kept.dedup();
    kept
}

impl Walks {
    /// `all`'s walks for `tts`' stops, timetables of one feed on different dates,
    /// which number their stops alike, each stop walking as its station does,
    /// and changing between stations of different complexes
    /// only to the closest stop on each pattern,
    /// or free between `free`'s complexes, by a pair of their stations' IDs, to every stop.
    pub fn for_feed(all: &StreetWalks, tts: &[&Timetable], free: &[(String, String)]) -> Self {
        let free: HashSet<(&str, &str)> = free
            .iter()
            .filter_map(|(a, b)| Some((all.complex(a)?, all.complex(b)?)))
            .flat_map(|(a, b)| [(a, b), (b, a)])
            .collect();
        let tt = tts[0];
        let index: HashMap<&str, u32> = all
            .stations
            .iter()
            .enumerate()
            .map(|(i, s)| (s.as_str(), i as u32))
            .collect();
        // Each stop's station in `all`, if it has it.
        let station: Vec<Option<u32>> = tt
            .stops
            .iter()
            .map(|s| index.get(s.station.as_str()).copied())
            .collect();
        // Each of `all`'s stations' stops.
        let mut stops: Vec<Vec<StopIdx>> = vec![Vec::new(); all.stations.len()];
        for (i, s) in station.iter().enumerate() {
            if let Some(s) = s {
                stops[*s as usize].push(i as StopIdx);
            }
        }
        let mut walks = Self {
            stations: station.clone(),
            complexes: station
                .iter()
                .map(|s| s.map(|s| all.complexes[s as usize].clone()))
                .collect(),
            ..Self::default()
        };
        for (i, &s) in station.iter().enumerate() {
            let Some(s) = s else { continue };
            let complex = &all.complexes[s as usize];
            let near: Vec<(StopIdx, Secs)> = all.near[s as usize]
                .iter()
                .filter(|&&(t, _)| &all.complexes[t as usize] != complex)
                .flat_map(|&(t, walk)| stops[t as usize].iter().map(move |&b| (b, walk)))
                .collect();
            walks
                .all_transfers
                .extend(near.iter().map(|&(to, walk)| (i as StopIdx, to, walk)));
            for (to, walk) in closest_on_patterns(tts, &near) {
                walks.transfers.push((i as StopIdx, to, walk));
            }
            for &(t, walk) in &all.near[s as usize] {
                if free.contains(&(complex.as_str(), all.complexes[t as usize].as_str())) {
                    for &b in &stops[t as usize] {
                        walks.free_transfers.push((i as StopIdx, b, walk));
                    }
                }
            }
        }
        for (origin, access) in &all.access {
            let access = access
                .iter()
                .flat_map(|&(t, walk)| stops[t as usize].iter().map(move |&b| (b, walk)))
                .collect();
            walks.access.insert(origin.clone(), access);
        }
        walks
    }
}

impl Timetable {
    /// `transfers`, `(from, to, walk)`, as footpaths,
    /// but those between stops it has a footpath between already,
    /// like `transfers.txt`'s free ones out of the system, or a passage inside it,
    /// each only for changing trains (`changes_only`).
    /// Those it adds.
    pub fn use_street_transfers(
        &mut self,
        transfers: &[(StopIdx, StopIdx, Secs)],
    ) -> Vec<(StopIdx, StopIdx, Secs)> {
        let mut added = Vec::new();
        for &(from, to, walk) in transfers {
            let paths = &mut self.footpaths[from as usize];
            if from == to || paths.iter().any(|&(s, _)| s == to) {
                continue;
            }
            paths.push((to, walk));
            self.changes_only.insert((from, to));
            added.push((from, to, walk));
        }
        added
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn street_walks_read_back_as_written() {
        let walks = StreetWalks {
            stations: vec!["A01".to_owned(), "V01".to_owned()],
            complexes: vec!["1".to_owned(), "V01".to_owned()],
            access: [
                ("V01".to_owned(), vec![(0, 300), (1, 0)]),
                ("A01".to_owned(), vec![(0, 0)]),
            ]
            .into_iter()
            .collect(),
            near: vec![vec![(1, 600)], vec![]],
        };
        let path = std::env::temp_dir().join(format!("street-walks-{}.bin", std::process::id()));
        walks.write(&path).unwrap();
        let read = StreetWalks::read(&path).unwrap();
        std::fs::remove_file(&path).unwrap();
        assert_eq!(read.stations, walks.stations);
        assert_eq!(read.complexes, walks.complexes);
        assert_eq!(read.access, walks.access);
        assert_eq!(read.near, walks.near);
    }
}
