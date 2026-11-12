//! Walks between platforms measured off LiDAR station maps (`raptor/lidar_walks.csv`),
//! made by `mta-od-data lidar-walks` from Sabrina Mielke's maps.
//! They take precedence over every other walk inside the fare gates,
//! from OSM, `transfers.txt`, or pathways, and passages are walked from them,
//! as the maps are drawn from 3D scans of the stations themselves.
//! A pair of platforms the maps don't cover keeps the walk it had.
//!
//! The file holds geometry only, in metres:
//! the straight line on the level between the connectors used,
//! and how far up and down stairs and escalators, along their slopes,
//! each flight measured off the map where its drawing shows it whole.
//! It's timed here by `Speeds`.

use std::collections::HashMap;

use anyhow::{Context, Result};
use serde::Deserialize;

use crate::gtfs::Secs;
use crate::timetable::{StopIdx, Timetable};

#[derive(Clone, Copy, Debug, Deserialize, PartialEq)]
pub struct LidarWalk {
    /// The straight line on the level between the two connectors used.
    pub metres: f64,
    pub stairs_up_m: f64,
    pub stairs_down_m: f64,
    pub escalator_up_m: f64,
    pub escalator_down_m: f64,
}

/// Walking speeds in a station, in miles an hour,
/// on stairs and escalators along their slopes.
#[derive(Clone, Copy, Debug, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct Speeds {
    pub walk_mph: f64,
    pub stairs_up_mph: f64,
    pub stairs_down_mph: f64,
    pub escalator_up_mph: f64,
    pub escalator_down_mph: f64,
}

impl Default for Speeds {
    /// Guesses the user agreed to: walking 3 mph, as on the street;
    /// stairs slower up than down; an escalator's 1.1 mph,
    /// with some riders walking up or down it.
    fn default() -> Self {
        Self {
            walk_mph: 3.0,
            stairs_up_mph: 1.1,
            stairs_down_mph: 1.6,
            escalator_up_mph: 1.3,
            escalator_down_mph: 1.6,
        }
    }
}

const METRES_PER_MILE: f64 = 1609.344;

#[derive(Deserialize)]
struct Row {
    from_platform: String,
    to_platform: String,
    #[serde(flatten)]
    walk: LidarWalk,
}

/// Walks from one OSM platform to another, by their way IDs.
pub type LidarWalks = HashMap<(String, String), LidarWalk>;

/// `raptor/lidar_walks.csv`'s walks, built in, so every run walks the same ones.
pub fn load() -> Result<LidarWalks> {
    let mut walks = LidarWalks::new();
    let mut reader = csv::Reader::from_reader(include_str!("../lidar_walks.csv").as_bytes());
    for row in reader.deserialize() {
        let row: Row = row.context("parsing lidar_walks.csv")?;
        walks.insert((row.from_platform, row.to_platform), row.walk);
    }
    Ok(walks)
}

impl LidarWalk {
    /// Its time, at `speeds`.
    pub fn secs(&self, speeds: &Speeds) -> Secs {
        let at = |metres: f64, mph: f64| metres / (mph * METRES_PER_MILE / 3600.0);
        (at(self.metres, speeds.walk_mph)
            + at(self.stairs_up_m, speeds.stairs_up_mph)
            + at(self.stairs_down_m, speeds.stairs_down_mph)
            + at(self.escalator_up_m, speeds.escalator_up_mph)
            + at(self.escalator_down_m, speeds.escalator_down_mph))
        .round() as Secs
    }
}

impl Timetable {
    /// `walks` between every two stops on platforms they join,
    /// replacing any footpath there was.
    /// Stops need their platforms from `split_platforms`.
    pub fn use_lidar_walks(&mut self, walks: &LidarWalks, speeds: &Speeds) {
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
                let secs = walk.secs(speeds);
                let paths = &mut self.footpaths[a as usize];
                match paths.iter_mut().find(|(s, _)| *s == b) {
                    Some((_, t)) => *t = secs,
                    None => paths.push((b, secs)),
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
        let up_to_down = walks[&("w513706097".to_owned(), "w513706098".to_owned())];
        assert!(up_to_down.metres > 0.0);
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
        };
        // 20s at 3 mph, then 10s each up and down stairs, and on an escalator.
        assert_eq!(walk.secs(&Speeds::default()), 50);
    }
}
