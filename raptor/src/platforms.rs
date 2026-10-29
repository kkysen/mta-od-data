//! Each route's stops' physical platforms, from OpenStreetMap
//! (`platforms.csv`, `mta-od-data fetch-platforms`'s).

use std::collections::HashMap;
use std::path::Path;

use anyhow::{Context, Result};
use serde::Deserialize;

/// `(route, previous stop, stop, next stop)`, by station ID,
/// "" for no previous or next stop.
type Key = (String, String, String, String);

#[derive(Debug, Default)]
pub struct Platforms(HashMap<Key, String>);

#[derive(Deserialize)]
struct Row {
    route: String,
    prev_stop: String,
    stop: String,
    next_stop: String,
    platform: String,
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
        Ok(Self(platforms))
    }

    /// The platform `route`'s trains from `prev` to `next` stop at at `stop`, if known.
    pub fn get(&self, route: &str, prev: &str, stop: &str, next: &str) -> Option<&str> {
        let key = (route.into(), prev.into(), stop.into(), next.into());
        self.0.get(&key).map(String::as_str)
    }
}

#[cfg(test)]
impl FromIterator<(Key, String)> for Platforms {
    fn from_iter<I: IntoIterator<Item = (Key, String)>>(iter: I) -> Self {
        Self(iter.into_iter().collect())
    }
}
