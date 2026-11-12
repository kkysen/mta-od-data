//! Walks between platforms measured off LiDAR station maps (`raptor/lidar_walks.csv`),
//! made by `mta-od-data lidar-walks` from Sabrina Mielke's maps.
//! They take precedence over every other walk inside the fare gates,
//! from OSM, `transfers.txt`, or pathways, and passages are walked from them,
//! as the maps are drawn from 3D scans of the stations themselves.
//! A pair of platforms the maps don't cover keeps the walk it had.
//!
//! The file holds geometry only, the distance and the levels climbed and descended,
//! timed here as OSM transfers are: `WALK_SPEED` on the level,
//! and a flight of stairs a level.

use std::collections::HashMap;

use anyhow::{Context, Result};
use serde::Deserialize;

use crate::gtfs::Secs;
use crate::timetable::{StopIdx, Timetable, WALK_SPEED};

#[derive(Clone, Copy, Debug, Deserialize, PartialEq)]
pub struct LidarWalk {
    /// The straight line on the level between the two connectors used.
    pub metres: f64,
    pub levels_up: u8,
    pub levels_down: u8,
}

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
    /// Its time, at `WALK_SPEED` and `secs_per_level` a flight, up or down.
    pub fn secs(&self, secs_per_level: Secs) -> Secs {
        let levels = Secs::from(self.levels_up) + Secs::from(self.levels_down);
        (self.metres / WALK_SPEED).round() as Secs + levels * secs_per_level
    }
}

impl Timetable {
    /// `walks` between every two stops on platforms they join,
    /// replacing any footpath there was.
    /// Stops need their platforms from `split_platforms`.
    pub fn use_lidar_walks(&mut self, walks: &LidarWalks, secs_per_level: Secs) {
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
                let secs = walk.secs(secs_per_level);
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
            metres: 24.0,
            levels_up: 1,
            levels_down: 2,
        };
        assert_eq!(walk.secs(30), 20 + 90);
    }
}
