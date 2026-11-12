//! Walks between platforms measured off LiDAR station maps (`raptor/lidar_walks.csv`),
//! made by `mta-od-data lidar-walks` from Sabrina Mielke's maps.
//! They take precedence over every other walk inside the fare gates,
//! from OSM, `transfers.txt`, pathways, or passages,
//! as the maps are drawn from 3D scans of the stations themselves.
//! A pair of platforms the maps don't cover keeps the walk it had.

use std::collections::HashMap;

use anyhow::{Context, Result};
use serde::Deserialize;

use crate::gtfs::Secs;
use crate::timetable::Timetable;

#[derive(Deserialize)]
struct Row {
    from_platform: String,
    to_platform: String,
    secs: Secs,
}

/// Seconds to walk from one OSM platform to another, by their way IDs.
pub type LidarWalks = HashMap<(String, String), Secs>;

/// `raptor/lidar_walks.csv`'s walks, built in, so every run walks the same ones.
pub fn load() -> Result<LidarWalks> {
    let mut walks = LidarWalks::new();
    let mut reader = csv::Reader::from_reader(include_str!("../lidar_walks.csv").as_bytes());
    for row in reader.deserialize() {
        let row: Row = row.context("parsing lidar_walks.csv")?;
        walks.insert((row.from_platform, row.to_platform), row.secs);
    }
    Ok(walks)
}

impl Timetable {
    /// `walks` between every two stops on platforms they join,
    /// replacing any footpath there was.
    /// Stops need their platforms from `split_platforms`.
    pub fn use_lidar_walks(&mut self, walks: &LidarWalks) {
        let on_mapped: Vec<(usize, &str)> = self
            .stops
            .iter()
            .enumerate()
            .filter_map(|(i, s)| {
                let p = s.platform.as_deref()?;
                walks
                    .keys()
                    .any(|(a, b)| a == p || b == p)
                    .then_some((i, p))
            })
            .collect();
        for &(a, pa) in &on_mapped {
            for &(b, pb) in &on_mapped {
                let Some(&secs) = walks.get(&(pa.to_owned(), pb.to_owned())) else {
                    continue;
                };
                let to = b as crate::timetable::StopIdx;
                let paths = &mut self.footpaths[a];
                match paths.iter_mut().find(|(s, _)| *s == to) {
                    Some((_, t)) => *t = secs,
                    None => paths.push((to, secs)),
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
        assert!(up_to_down > 0);
        assert!(walks.contains_key(&("w513706084".to_owned(), "w513706097".to_owned())));
    }
}
