//! Walks between stations, and from origins to them, in seconds,
//! on OpenStreetMap's streets (the `streets` crate),
//! through stations' entrances, each with its own time between the street and the platforms
//! (`mta-od-data fetch-station-access`'s `data/station_access.csv`),
//! timed for the edge of the platform each stop's trains stop at (`platform_edges.csv`),
//! or, where a 3D model measures them, each platform's own, in and out (`lidar::access`).
//!
//! The streets are walked once, for every feed's stations (`StreetWalks`),
//! and each feed takes its own stops' walks from them (`Walks`).
//! Changing trains within a station or complex is left to the timetable;
//! only changes between them walk the streets, out through one entrance and in through another.
//! Moved from `subway-sheds`, which walks from origins too, and draws the walks.

use rayon::iter::{IndexedParallelIterator, IntoParallelRefIterator, ParallelIterator};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use streets::{Graph, Mm, Search, Split};

use crate::cars::{Cars, Path};
use crate::gtfs::Secs;
use crate::lidar;
use crate::speeds::Speeds;
use crate::timetable::{StopIdx, Timetable};

/// Walking on the streets at 3 mph, as R5 does, in millimeters a second.
pub const WALKING_SPEED_MM_PER_S: Mm = 1341;

/// How far apart stations may be to change between them on the streets:
/// about the 1000 m R5 walked between stops, as a time, entrances included.
const TRANSFER_LIMIT: Secs = 15 * 60;

/// A station's entrance, and its time from the street to the platforms and back out.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Entrance {
    pub lat: f64,
    pub lon: f64,
    pub in_secs: Secs,
    pub out_secs: Secs,
}

/// A station's entrances, or with `platform`, its OSM way's,
/// for the station's stops on that platform alone,
/// or with `stop` too, for that GTFS stop's alone,
/// timed for the edge of the platform its trains stop at.
#[derive(Clone, Debug, PartialEq)]
pub struct Station {
    pub id: String,
    pub stop: Option<String>,
    pub platform: Option<String>,
    pub complex: String,
    pub entrances: Vec<Entrance>,
}

/// Every walk, from origins and stations by their IDs, whatever feed has them.
pub struct StreetWalks {
    /// Each station's ID, by its index here.
    stations: Vec<String>,
    /// Each one's GTFS stop, if it's one stop's at one platform.
    stops: Vec<Option<String>>,
    /// Each one's platform, if it's one platform's.
    platforms: Vec<Option<String>>,
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

/// A station's entrances on the streets,
/// each with its times in to the platforms and out from them, as distances.
struct Snapped {
    entrances: Vec<(Split, Mm, Mm)>,
}

impl Snapped {
    /// The vertices to search from, starting on the platforms, going out,
    /// or, with `inside` false, the street.
    fn sources(&self, inside: bool) -> Vec<(u32, Mm)> {
        self.entrances
            .iter()
            .flat_map(|&(ref split, _, out)| {
                let cost = if inside { out } else { 0 };
                split.ends().map(move |(v, d)| (v, d.saturating_add(cost)))
            })
            .collect()
    }

    /// How far the latest search reached this station's platforms, in through its entrances.
    fn reached(&self, search: &Search) -> Option<Mm> {
        self.entrances
            .iter()
            .filter_map(|(split, into, _)| Some(search.to(split)?.saturating_add(*into)))
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
            .map(|station| Snapped {
                entrances: station
                    .entrances
                    .iter()
                    .filter_map(|e| {
                        Some((graph.snap(e.lat, e.lon)?, mm(e.in_secs), mm(e.out_secs)))
                    })
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

        // An origin starts at its station's own entrances, not one platform's.
        let index: HashMap<&str, usize> = stations
            .iter()
            .enumerate()
            .filter(|(_, s)| s.platform.is_none())
            .map(|(i, s)| (s.id.as_str(), i))
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
            stations: stations.iter().map(|s| s.id.clone()).collect(),
            stops: stations.iter().map(|s| s.stop.clone()).collect(),
            platforms: stations.iter().map(|s| s.platform.clone()).collect(),
            complexes: stations.iter().map(|s| s.complex.clone()).collect(),
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

    /// The complex of the station `id`, if it's one of these.
    pub fn complex(&self, id: &str) -> Option<&str> {
        let i = self.stations.iter().position(|s| s == id)?;
        Some(&self.complexes[i])
    }
}

#[derive(Clone, serde::Deserialize)]
struct AccessRow {
    station: String,
    complex: String,
    lat: f64,
    lon: f64,
    /// From the street to where the stairs reach the platform, or for a long walk
    /// inside the station, to its middle.
    secs: Secs,
    /// How far from the platform's middle the stairs reach it, in feet,
    /// past its end if more than half its length, by a corridor.
    platform_ft: f64,
    /// The platform's length in feet, the station's longest edge,
    /// or blank for a long walk inside the station, all in `secs`.
    length_ft: Option<f64>,
}

/// A row of `platform_edges.csv`, beside `station_access.csv`:
/// the length of the edge of `platform`, an OSM way,
/// that the GTFS stop `stop`, as `127N`, has its trains stop at.
#[derive(serde::Deserialize)]
struct EdgeRow {
    stop: String,
    platform: String,
    length_ft: f64,
}

/// The file beside `station_access.csv` with each stop's platform edge.
const EDGES: &str = "platform_edges.csv";

const METRES_PER_FOOT: f64 = 0.3048;

impl AccessRow {
    /// This estimate's times at `speeds`:
    /// in, boarding where the stairs reach the platform;
    /// out, on average from riders' spots along the train (`cars`) to there;
    /// both by any corridor past the platform's end.
    fn entrance(&self, speeds: &Speeds, cars: &Cars) -> Entrance {
        let (in_secs, out_secs) = match self.length_ft {
            None => (self.secs, self.secs),
            Some(length_ft) => {
                let length = length_ft * METRES_PER_FOOT;
                let from_middle = self.platform_ft * METRES_PER_FOOT;
                let half = length / 2.0;
                let to_end = f64::from(self.secs) + speeds.walk_secs((from_middle - half).max(0.0));
                let stairs = Path {
                    along: half + from_middle.min(half),
                    secs: to_end,
                };
                let out = cars.expected_secs(length, &[stairs], speeds);
                (to_end.round() as Secs, out.round() as Secs)
            }
        };
        Entrance {
            lat: self.lat,
            lon: self.lon,
            in_secs,
            out_secs,
        }
    }
}

/// Each station's entrances in `mta-od-data fetch-station-access`'s `station_access.csv`,
/// in the order it first lists them, timed by `AccessRow::entrance`;
/// then again, as its own, for each stop `platform_edges.csv` beside it lists
/// at an edge of its platform other than as long as the station's,
/// timed for that edge;
/// then each modeled platform's, its own station's complex's (`lidar::access`, in `dir`),
/// instead of its stops' there,
/// timed at `speeds` with riders spread along the train by `cars`.
pub fn load_stations(
    path: &std::path::Path,
    dir: &std::path::Path,
    speeds: &Speeds,
    cars: &Cars,
) -> anyhow::Result<Vec<Station>> {
    use anyhow::Context;
    let mut reader =
        csv::Reader::from_path(path).with_context(|| format!("opening {}", path.display()))?;
    let mut rows: Vec<(String, Vec<AccessRow>)> = Vec::new();
    let mut index: HashMap<String, usize> = HashMap::default();
    for row in reader.deserialize() {
        let row: AccessRow = row?;
        let i = *index.entry(row.station.clone()).or_insert_with(|| {
            rows.push((row.station.clone(), Vec::new()));
            rows.len() - 1
        });
        rows[i].1.push(row);
    }
    let station = |id: &str, stop: Option<String>, platform: Option<String>, length_ft| {
        let rows = &rows[index[id]].1;
        Station {
            id: id.to_owned(),
            stop,
            platform,
            complex: rows[0].complex.clone(),
            entrances: rows
                .iter()
                .map(|r| match (r.length_ft, length_ft) {
                    (Some(_), Some(ft)) => AccessRow {
                        length_ft: Some(ft),
                        ..r.clone()
                    },
                    _ => r.clone(),
                })
                .map(|r| r.entrance(speeds, cars))
                .collect(),
        }
    };
    let mut stations: Vec<Station> = rows
        .iter()
        .map(|(id, _)| station(id, None, None, None))
        .collect();
    let modeled: Vec<lidar::PlatformAccess> = lidar::access(dir, speeds, cars)?;
    let is_modeled: HashSet<(&str, &str)> = modeled
        .iter()
        .map(|m| (m.station.as_str(), m.platform.as_str()))
        .collect();
    let edges = path.with_file_name(EDGES);
    let mut reader =
        csv::Reader::from_path(&edges).with_context(|| format!("opening {}", edges.display()))?;
    for row in reader.deserialize() {
        let row: EdgeRow = row?;
        // A GTFS stop's station is its ID but its direction.
        let id = row.stop[..row.stop.len() - 1].to_owned();
        let id = id.as_str();
        let Some(&i) = index.get(id) else { continue };
        let longest = rows[i].1.iter().find_map(|r| r.length_ft);
        // A modeled platform's stops take its model's, not their edge's estimate.
        if longest.is_none_or(|ft| ft == row.length_ft)
            || is_modeled.contains(&(id, row.platform.as_str()))
        {
            continue;
        }
        stations.push(station(
            id,
            Some(row.stop),
            Some(row.platform),
            Some(row.length_ft),
        ));
    }
    for p in modeled {
        let complex = index
            .get(&p.station)
            .map(|&i| rows[i].1[0].complex.clone())
            .with_context(|| format!("{} has no entrances in {}", p.station, path.display()))?;
        stations.push(Station {
            id: p.station,
            stop: None,
            platform: Some(p.platform),
            complex,
            entrances: p.entrances,
        });
    }
    Ok(stations)
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
        let index: HashMap<(&str, Option<&str>, Option<&str>), u32> = all
            .stations
            .iter()
            .zip(&all.stops)
            .zip(&all.platforms)
            .enumerate()
            .map(|(i, ((s, stop), p))| ((s.as_str(), stop.as_deref(), p.as_deref()), i as u32))
            .collect();
        // Each stop's station in `all`, if it has it:
        // its platform's own entrances if measured,
        // or else its own, timed for the edge of its platform it's at,
        // or else its station's, never more than one.
        let station: Vec<Option<u32>> = tt
            .stops
            .iter()
            .map(|s| {
                let station = s.station.as_str();
                let platform = s.platform.as_deref();
                platform
                    .and_then(|p| {
                        index
                            .get(&(station, None, Some(p)))
                            .or_else(|| index.get(&(station, Some(s.id.as_str()), Some(p))))
                    })
                    .or_else(|| index.get(&(station, None, None)))
                    .copied()
            })
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
    fn estimates_board_where_the_stairs_land_and_leave_from_along_the_train() {
        let speeds = Speeds::default();
        let cars = Cars {
            plan_share: 0.0,
            plan_sigma_m: 18.0,
        };
        let row = |platform_ft: f64, length_ft: Option<f64>| AccessRow {
            station: "A01".to_owned(),
            complex: "1".to_owned(),
            lat: 40.7,
            lon: -74.0,
            secs: 40,
            platform_ft,
            length_ft,
        };
        let times = |r: AccessRow| {
            let e = r.entrance(&speeds, &cars);
            (e.in_secs, e.out_secs)
        };
        // At the middle of a 100 m platform: in, right there;
        // out, 25 m on average from along the train, 19s at 3 mph.
        let length = Some(100.0 / METRES_PER_FOOT);
        assert_eq!(times(row(0.0, length)), (40, 59));
        // At its end: 50 m on average, 37s.
        assert_eq!(times(row(50.0 / METRES_PER_FOOT, length)), (40, 77));
        // 20 m past its end, 15s by a corridor, both ways.
        assert_eq!(times(row(70.0 / METRES_PER_FOOT, length)), (55, 92));
        // A long walk inside the station, all in its time.
        assert_eq!(times(row(0.0, None)), (40, 40));
    }

    #[test]
    fn stops_walk_as_their_platform_model_their_edge_or_their_station() {
        // A's two directions at an island, `wI`, B's at a modeled platform, `wM`.
        let stops = "stop_id,stop_name,location_type,parent_station\n\
            A,Alpha,1,\nAN,Alpha,,A\nAS,Alpha,,A\nB,Beta,1,\nBN,Beta,,B\nBS,Beta,,B\n";
        let files = std::collections::HashMap::from([
            ("stops.txt", stops),
            ("trips.txt", "route_id,trip_id,service_id\n1,t,Weekday\n"),
            (
                "stop_times.txt",
                "trip_id,stop_id,arrival_time,departure_time,stop_sequence\n\
                 t,AN,08:00:00,08:00:00,1\nt,BN,08:10:00,08:10:00,2\n",
            ),
            (
                "calendar.txt",
                "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,\
                 start_date,end_date\nWeekday,1,1,1,1,1,0,0,20250811,20251101\n",
            ),
        ]);
        let feed = crate::gtfs::Feed::load(&mut { files }).unwrap();
        let mut tt = Timetable::build(&feed, jiff::civil::date(2025, 9, 3)).unwrap();
        let idx = |id: &str| tt.stops.iter().position(|s| s.id == id).unwrap();
        let (an, a_s, bn, bs) = (idx("AN"), idx("AS"), idx("BN"), idx("BS"));
        for i in [an, a_s] {
            tt.stops[i].platform = Some("wI".into());
        }
        tt.stops[bn].platform = Some("wM".into());
        let some = |s: &str| Some(s.to_owned());
        let all = StreetWalks {
            stations: ["A", "A", "B", "B"].map(str::to_owned).to_vec(),
            // AS at the island's shorter edge; AN at its longer, the station's.
            stops: vec![None, some("AS"), None, None],
            platforms: vec![None, some("wI"), None, some("wM")],
            complexes: ["1", "1", "2", "2"].map(str::to_owned).to_vec(),
            access: HashMap::default(),
            near: vec![Vec::new(); 4],
        };
        let walks = Walks::for_feed(&all, &[&tt], &[]);
        assert_eq!(walks.stations[an], Some(0));
        assert_eq!(walks.stations[a_s], Some(1));
        assert_eq!(walks.stations[bn], Some(3));
        // Its platform unknown: its station's.
        assert_eq!(walks.stations[bs], Some(2));
    }
}
