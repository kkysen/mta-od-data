//! Each route's stops' physical platforms, from OpenStreetMap
//! (`platforms.csv`, `mta-od-data fetch-platforms`'s),
//! and which are stacked one right over another (`stacked_platforms.csv`, beside it).

use std::collections::HashMap;
use std::path::Path;

use anyhow::{Context, Result};
use serde::Deserialize;

/// `(route, previous stop, stop, next stop)`, by station ID,
/// "" for no previous or next stop.
type Key = (String, String, String, String);

#[derive(Debug, Default)]
pub struct Platforms {
    platforms: HashMap<Key, String>,
    /// Pairs of platforms one right over the other, each way round,
    /// and how many levels apart.
    stacked: HashMap<(String, String), u8>,
}

#[derive(Deserialize)]
struct Row {
    route: String,
    prev_stop: String,
    stop: String,
    next_stop: String,
    platform: String,
}

#[derive(Deserialize)]
struct StackedRow {
    platform: String,
    other: String,
    levels: u8,
}

impl Platforms {
    pub fn load(path: &Path) -> Result<Self> {
        let mut reader =
            csv::Reader::from_path(path).with_context(|| format!("opening {}", path.display()))?;
        let mut platforms = HashMap::new();
        for row in reader.deserialize() {
            let row: Row = row.with_context(|| format!("reading {}", path.display()))?;
            if !row.platform.is_empty() {
                platforms.insert(
                    (row.route, row.prev_stop, row.stop, row.next_stop),
                    row.platform,
                );
            }
        }
        let stacked_path = path.with_file_name("stacked_platforms.csv");
        let mut reader = csv::Reader::from_path(&stacked_path)
            .with_context(|| format!("opening {}", stacked_path.display()))?;
        let mut stacked = HashMap::new();
        for row in reader.deserialize() {
            let row: StackedRow =
                row.with_context(|| format!("reading {}", stacked_path.display()))?;
            stacked.insert((row.other.clone(), row.platform.clone()), row.levels);
            stacked.insert((row.platform, row.other), row.levels);
        }
        Ok(Self { platforms, stacked })
    }

    /// The platform `route`'s trains from `prev` to `next` stop at at `stop`, if known.
    pub fn get(&self, route: &str, prev: &str, stop: &str, next: &str) -> Option<&str> {
        let key = (route.into(), prev.into(), stop.into(), next.into());
        self.platforms.get(&key).map(String::as_str)
    }

    /// How many levels apart platforms `a` and `b` are, if stacked one over the other.
    pub fn stacked(&self, a: &str, b: &str) -> Option<u8> {
        self.stacked.get(&(a.into(), b.into())).copied()
    }
}

#[cfg(test)]
impl Platforms {
    /// These platforms, with these pairs stacked, so many levels apart.
    pub fn with_stacked(mut self, pairs: &[(&str, &str, u8)]) -> Self {
        for &(a, b, levels) in pairs {
            self.stacked.insert((a.into(), b.into()), levels);
            self.stacked.insert((b.into(), a.into()), levels);
        }
        self
    }
}

#[cfg(test)]
impl FromIterator<(Key, String)> for Platforms {
    fn from_iter<I: IntoIterator<Item = (Key, String)>>(iter: I) -> Self {
        Self {
            platforms: iter.into_iter().collect(),
            stacked: HashMap::new(),
        }
    }
}
