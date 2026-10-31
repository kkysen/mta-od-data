//! The OpenStreetMap data streets are made from: nodes' locations and ways' nodes and tags.

use std::path::Path;

use anyhow::{Context, Result};
use osmpbf::{Element, ElementReader};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};

use crate::permissions;

/// A node's or way's tags.
#[derive(Clone, Debug, Default)]
pub struct Tags(Vec<(String, String)>);

impl Tags {
    pub fn get(&self, key: &str) -> Option<&str> {
        self.0
            .iter()
            .find(|(k, _)| k == key)
            .map(|(_, v)| v.as_str())
    }

    pub fn has(&self, key: &str) -> bool {
        self.get(key).is_some()
    }

    pub fn is(&self, key: &str, value: &str) -> bool {
        self.get(key) == Some(value)
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }
}

impl FromIterator<(String, String)> for Tags {
    fn from_iter<I: IntoIterator<Item = (String, String)>>(iter: I) -> Self {
        Self(iter.into_iter().collect())
    }
}

#[derive(Clone, Debug)]
pub struct Way {
    pub nodes: Vec<i64>,
    pub tags: Tags,
}

/// The ways streets may be made of, and their nodes.
#[derive(Debug, Default)]
pub struct Osm {
    /// `(latitude, longitude)` by node ID.
    pub nodes: HashMap<i64, (f64, f64)>,
    /// Nodes that can't be passed (`permissions::impassable`).
    pub impassable: HashSet<i64>,
    /// Only the routable ones (`permissions::routable`).
    pub ways: Vec<Way>,
    /// Nodes on more than one way, or twice on one, of every way read, routable or not,
    /// where R5 splits ways into edges.
    pub intersections: HashSet<i64>,
}

impl Osm {
    /// Reads `path`, an `.osm.pbf`.
    pub fn read(path: &Path) -> Result<Self> {
        let mut osm = Self::default();
        let mut seen = HashSet::default();
        let reader = ElementReader::from_path(path)
            .with_context(|| format!("opening {}", path.display()))?;
        let owned = |tags: &mut dyn Iterator<Item = (&str, &str)>| {
            tags.map(|(k, v)| (k.to_owned(), v.to_owned()))
                .collect::<Tags>()
        };
        reader
            .for_each(|element| match element {
                Element::Node(n) => {
                    osm.node(n.id(), n.lat(), n.lon(), owned(&mut n.tags()));
                }
                Element::DenseNode(n) => {
                    osm.node(n.id(), n.lat(), n.lon(), owned(&mut n.tags()));
                }
                Element::Way(w) => {
                    for node in w.refs() {
                        if !seen.insert(node) {
                            osm.intersections.insert(node);
                        }
                    }
                    let tags = owned(&mut w.tags());
                    if permissions::routable(&tags) {
                        osm.ways.push(Way {
                            nodes: w.refs().collect(),
                            tags,
                        });
                    }
                }
                Element::Relation(_) => {}
            })
            .with_context(|| format!("reading {}", path.display()))?;
        Ok(osm)
    }

    fn node(&mut self, id: i64, lat: f64, lon: f64, tags: Tags) {
        self.nodes.insert(id, (lat, lon));
        if permissions::impassable(&tags) {
            self.impassable.insert(id);
        }
    }
}
