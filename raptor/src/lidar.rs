//! Walks between platforms measured off LiDAR station maps (`raptor/lidar_walks.csv`),
//! made by `mta-od-data lidar-walks` from Sabrina Mielke's maps,
//! and from the 3D models she drew some from, as 14 St-Union Sq's.
//! They take precedence over every other walk inside the fare gates,
//! from OSM, `transfers.txt`, or pathways, and passages are walked from them,
//! as the maps are drawn from 3D scans of the stations themselves.
//! A pair of platforms the maps don't cover keeps the walk it had.
//! OSM's indoor ways give walks in the same form (`raptor/osm_walks.csv`),
//! over OSM transfers' but under pathways' and the maps'.
//!
//! The file holds geometry only, in metres:
//! the straight line on the level between the connectors used,
//! or the walk along the floors, where corridors are bent or measured off a model,
//! and how far up and down stairs and escalators, along their slopes,
//! each flight measured off the map where its drawing shows it whole, or the model.
//! It's timed here by `Speeds`.
//! A pair of platforms may have several rows, one for each way off the first,
//! each with its foot's spot along it, `along_m`, of `platform_m`:
//! a transfer takes the average over riders' spots along the train (`Cars`).
//!
//! The models give walks between stations' street entrances and their platforms too
//! (`raptor/lidar_access.csv`, `mta-od-data lidar-access`), in the same form,
//! for walks on the streets between stations (`walks.rs`), over the entrances' estimates.

use std::collections::HashMap;

use anyhow::{Context, Result};
use serde::Deserialize;

use crate::cars::{Cars, Path};
use crate::gtfs::Secs;
use crate::pathways::GATE_SECS;
use crate::speeds::{Speeds, m_per_s};
use crate::timetable::{StopIdx, Timetable};
use crate::walks::Entrance;

#[derive(Clone, Copy, Debug, Deserialize, PartialEq)]
pub struct LidarWalk {
    /// The straight line on the level between the two connectors used.
    pub metres: f64,
    pub stairs_up_m: f64,
    pub stairs_down_m: f64,
    pub escalator_up_m: f64,
    pub escalator_down_m: f64,
    /// Where its foot is along the first platform, from one end, if known,
    #[serde(default)]
    pub along_m: Option<f64>,
    /// of the first platform's length.
    #[serde(default)]
    pub platform_m: Option<f64>,
}

#[derive(Deserialize)]
struct Row {
    from_platform: String,
    to_platform: String,
    #[serde(flatten)]
    walk: LidarWalk,
}

/// Walks from one OSM platform to another, by their way IDs,
/// each way off the first.
pub type LidarWalks = HashMap<(String, String), Vec<LidarWalk>>;

/// `lidar_walks.csv`'s walks, in `dir`, beside the config (`raptor/`):
/// read each run rather than built in, so a stale build can't keep old ones.
pub fn load(dir: &std::path::Path) -> Result<LidarWalks> {
    parse(&read(dir, "lidar_walks.csv")?, "lidar_walks.csv")
}

fn read(dir: &std::path::Path, name: &str) -> Result<String> {
    let path = dir.join(name);
    std::fs::read_to_string(&path).with_context(|| format!("reading {}", path.display()))
}

/// `osm_walks.csv`'s, in `dir` too, along OSM's indoor ways (`mta-od-data osm-walks`),
/// in the same form, where OSM joins two platforms;
/// OSM is taken as right where it maps a walk at all.
pub fn load_osm(dir: &std::path::Path) -> Result<LidarWalks> {
    parse(&read(dir, "osm_walks.csv")?, "osm_walks.csv")
}

fn parse(text: &str, name: &str) -> Result<LidarWalks> {
    let mut walks = LidarWalks::new();
    let mut reader = csv::Reader::from_reader(text.as_bytes());
    for row in reader.deserialize() {
        let row: Row = row.with_context(|| format!("parsing {name}"))?;
        walks
            .entry((row.from_platform, row.to_platform))
            .or_default()
            .push(row.walk);
    }
    Ok(walks)
}

impl LidarWalk {
    /// Its time from its foot, at `speeds`.
    pub fn secs(&self, speeds: &Speeds) -> f64 {
        let at = |metres: f64, mph: f64| metres / m_per_s(mph);
        at(self.metres, speeds.walk_mph)
            + at(self.stairs_up_m, speeds.stairs_up_mph)
            + at(self.stairs_down_m, speeds.stairs_down_mph)
            + at(self.escalator_up_m, speeds.escalator_up_mph)
            + at(self.escalator_down_m, speeds.escalator_down_mph)
    }
}

/// The time to change trains by any of `paths` off one platform:
/// on average from riders' spots along the train if each path's foot is known,
/// or else the quickest, from its foot.
pub fn transfer_secs(paths: &[LidarWalk], speeds: &Speeds, cars: &Cars) -> Secs {
    let timed: Vec<(&LidarWalk, f64)> = paths.iter().map(|w| (w, w.secs(speeds))).collect();
    expected_secs(&timed, speeds, cars).round() as Secs
}

/// `transfer_secs`, but of `paths` each already timed.
fn expected_secs(paths: &[(&LidarWalk, f64)], speeds: &Speeds, cars: &Cars) -> f64 {
    let feet: Option<Vec<Path>> = paths
        .iter()
        .map(|&(w, secs)| {
            Some(Path {
                along: w.along_m?,
                secs,
            })
        })
        .collect();
    match (feet, paths.first().and_then(|(w, _)| w.platform_m)) {
        (Some(feet), Some(platform_m)) => cars.expected_secs(platform_m, &feet, speeds),
        _ => paths
            .iter()
            .map(|&(_, secs)| secs)
            .fold(f64::INFINITY, f64::min),
    }
}

/// Which way an entrance's walk goes: into the station from the street, or out.
#[derive(Clone, Copy, Debug, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum Way {
    In,
    Out,
}

#[derive(Deserialize)]
struct AccessRow {
    station: String,
    platform: String,
    lat: f64,
    lon: f64,
    way: Way,
    metres: f64,
    stairs_up_m: f64,
    stairs_down_m: f64,
    escalator_up_m: f64,
    escalator_down_m: f64,
    gates: Secs,
    // Not `LidarWalk` flattened, which reads an empty `along_m` as a string.
    along_m: Option<f64>,
    platform_m: Option<f64>,
}

impl AccessRow {
    fn walk(&self) -> LidarWalk {
        LidarWalk {
            metres: self.metres,
            stairs_up_m: self.stairs_up_m,
            stairs_down_m: self.stairs_down_m,
            escalator_up_m: self.escalator_up_m,
            escalator_down_m: self.escalator_down_m,
            along_m: self.along_m,
            platform_m: self.platform_m,
        }
    }
}

/// A platform's street entrances, as walked off a 3D model.
#[derive(Debug, PartialEq)]
pub struct PlatformAccess {
    /// Its GTFS station,
    pub station: String,
    /// its OSM way,
    pub platform: String,
    /// and its entrances.
    pub entrances: Vec<Entrance>,
}

/// `lidar_access.csv`'s walks, in `dir` (`raptor/`), between modeled stations' street entrances
/// and their platforms (`mta-od-data lidar-access`), timed at `speeds`,
/// through each fare gate in `GATE_SECS`, by platform:
/// in, the quickest to anywhere on the platform, where riders board;
/// out, on average from riders' spots along the train (`cars`),
/// as a transfer off a platform is.
pub fn access(dir: &std::path::Path, speeds: &Speeds, cars: &Cars) -> Result<Vec<PlatformAccess>> {
    parse_access(&read(dir, "lidar_access.csv")?, speeds, cars)
}

fn parse_access(text: &str, speeds: &Speeds, cars: &Cars) -> Result<Vec<PlatformAccess>> {
    let mut reader = csv::Reader::from_reader(text.as_bytes());
    let rows: Vec<AccessRow> = reader
        .deserialize()
        .collect::<Result<_, _>>()
        .context("parsing lidar_access.csv")?;
    // In the order the file lists them, platform by platform, then entrance by entrance.
    let mut out: Vec<PlatformAccess> = Vec::new();
    for (i, row) in rows.iter().enumerate() {
        let same = |r: &AccessRow| {
            (r.station.as_str(), r.platform.as_str(), r.lat, r.lon)
                == (
                    row.station.as_str(),
                    row.platform.as_str(),
                    row.lat,
                    row.lon,
                )
        };
        if rows[..i].iter().any(same) {
            continue;
        }
        let secs = |way: Way| -> Secs {
            let walks: Vec<(LidarWalk, Secs)> = rows
                .iter()
                .filter(|r| same(r) && r.way == way)
                .map(|r| (r.walk(), r.gates))
                .collect();
            let timed: Vec<(&LidarWalk, f64)> = walks
                .iter()
                .map(|(w, gates)| (w, w.secs(speeds) + f64::from(gates * GATE_SECS)))
                .collect();
            expected_secs(&timed, speeds, cars).round() as Secs
        };
        let entrance = Entrance {
            lat: row.lat,
            lon: row.lon,
            in_secs: secs(Way::In),
            out_secs: secs(Way::Out),
        };
        match out
            .iter_mut()
            .find(|p| (p.station.as_str(), p.platform.as_str()) == (&row.station, &row.platform))
        {
            Some(p) => p.entrances.push(entrance),
            None => out.push(PlatformAccess {
                station: row.station.clone(),
                platform: row.platform.clone(),
                entrances: vec![entrance],
            }),
        }
    }
    Ok(out)
}

impl Timetable {
    /// `walks` between every two stops on platforms they join,
    /// replacing the footpath there was; none is added where there was none.
    /// Stops need their platforms from `split_platforms`.
    pub fn use_walks(&mut self, walks: &LidarWalks, speeds: &Speeds, cars: &Cars) {
        let on_mapped: Vec<(StopIdx, &str)> = self
            .stops
            .iter()
            .enumerate()
            .filter_map(|(i, s)| {
                let p = s.platform.as_deref()?;
                walks
                    .keys()
                    .any(|(a, b)| a == p || b == p)
                    .then_some((i as StopIdx, p))
            })
            .collect();
        for &(a, pa) in &on_mapped {
            for &(b, pb) in &on_mapped {
                let Some(walk) = walks.get(&(pa.to_owned(), pb.to_owned())) else {
                    continue;
                };
                // Only a walk there already is, between a complex's stops:
                // OSM doesn't map fare gates, so a walk it finds between complexes
                // may cross an unpaid mezzanine, not a free transfer.
                if let Some((_, t)) = self.footpaths[a as usize].iter_mut().find(|(s, _)| *s == b) {
                    *t = transfer_secs(walk, speeds, cars);
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn loads_times_square() {
        let walks = load(std::path::Path::new(env!("CARGO_MANIFEST_DIR"))).unwrap();
        let up_to_down = &walks[&("w513706097".to_owned(), "w513706098".to_owned())];
        assert!(up_to_down[0].metres > 0.0);
        assert!(walks.contains_key(&("w513706084".to_owned(), "w513706097".to_owned())));
    }

    #[test]
    fn entrances_board_where_they_land_and_leave_from_along_the_train() {
        let text = "station,platform,lat,lon,way,metres,stairs_up_m,stairs_down_m,\
                    escalator_up_m,escalator_down_m,gates,along_m,platform_m,name\n\
                    A01,w1,40.7,-74.0,in,13.4112,0,0,0,0,1,,,A\n\
                    A01,w1,40.7,-74.0,out,0,0,0,0,0,1,0,100,A\n";
        let cars = Cars {
            plan_share: 0.0,
            plan_sigma_m: 18.0,
        };
        let access = parse_access(text, &Speeds::default(), &cars).unwrap();
        // In: 10s at 3 mph, then the gate's 3s, boarding right there.
        // Out: 50 m on average from along the train to the stairs at its end, 37s, and the gate.
        assert_eq!(
            access,
            [PlatformAccess {
                station: "A01".to_owned(),
                platform: "w1".to_owned(),
                entrances: vec![Entrance {
                    lat: 40.7,
                    lon: -74.0,
                    in_secs: 13,
                    out_secs: 40,
                }],
            }]
        );
    }

    #[test]
    fn union_sq_entrances_reach_the_l() {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
        let access = access(dir, &Speeds::default(), &Cars::default()).unwrap();
        let l = access.iter().find(|p| p.station == "L03").unwrap();
        assert_eq!(l.entrances.len(), 12);
        assert!(l.entrances.iter().all(|e| e.in_secs < e.out_secs));
    }

    #[test]
    fn secs_walk_and_climb() {
        let walk = LidarWalk {
            metres: 26.8224,
            stairs_up_m: 4.9175,
            stairs_down_m: 7.1526,
            escalator_up_m: 5.8115,
            escalator_down_m: 0.0,
            along_m: None,
            platform_m: None,
        };
        // 20s at 3 mph, then 10s each up and down stairs, and on an escalator.
        assert_eq!(walk.secs(&Speeds::default()).round(), 50.0);
    }
}
