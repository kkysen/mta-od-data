//! Walks between platforms measured off LiDAR station maps (`raptor/lidar_walks.csv`),
//! made by `mta-od-data lidar-walks` from Sabrina Mielke's maps.
//! They take precedence over every other walk inside the fare gates,
//! from OSM, `transfers.txt`, or pathways, and passages are walked from them,
//! as the maps are drawn from 3D scans of the stations themselves.
//! A pair of platforms the maps don't cover keeps the walk it had.
//! OSM's indoor ways give walks in the same form (`raptor/osm_walks.csv`),
//! over OSM transfers' but under pathways' and the maps'.
//!
//! The file holds geometry only, in metres:
//! the straight line on the level between the connectors used,
//! and how far up and down stairs and escalators, along their slopes,
//! each flight measured off the map where its drawing shows it whole.
//! It's timed here by `Speeds`.
//! A pair of platforms may have several rows, one for each way off the first,
//! each with its foot's spot along it, `along_m`, of `platform_m`:
//! a transfer takes the average over riders' spots along the train (`Cars`).

use std::collections::HashMap;

use anyhow::{Context, Result};
use serde::Deserialize;

use crate::cars::{Cars, Path};
use crate::gtfs::Secs;
use crate::speeds::{Speeds, m_per_s};
use crate::timetable::{StopIdx, Timetable};

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

/// `raptor/lidar_walks.csv`'s walks, built in, so every run walks the same ones.
pub fn load() -> Result<LidarWalks> {
    parse(include_str!("../lidar_walks.csv"), "lidar_walks.csv")
}

/// `raptor/osm_walks.csv`'s, along OSM's indoor ways (`mta-od-data osm-walks`),
/// in the same form, where OSM joins two platforms;
/// OSM is taken as right where it maps a walk at all.
pub fn load_osm() -> Result<LidarWalks> {
    parse(include_str!("../osm_walks.csv"), "osm_walks.csv")
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
    let feet: Option<Vec<Path>> = paths
        .iter()
        .map(|w| {
            Some(Path {
                along: w.along_m?,
                secs: w.secs(speeds),
            })
        })
        .collect();
    let secs = match (feet, paths.first().and_then(|w| w.platform_m)) {
        (Some(feet), Some(platform_m)) => cars.expected_secs(platform_m, &feet, speeds),
        _ => paths
            .iter()
            .map(|w| w.secs(speeds))
            .fold(f64::INFINITY, f64::min),
    };
    secs.round() as Secs
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
        let walks = load().unwrap();
        let up_to_down = &walks[&("w513706097".to_owned(), "w513706098".to_owned())];
        assert!(up_to_down[0].metres > 0.0);
        assert!(walks.contains_key(&("w513706084".to_owned(), "w513706097".to_owned())));
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
