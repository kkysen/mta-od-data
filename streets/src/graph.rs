//! The walking network: vertices where ways meet or end, and edges along ways between them,
//! made as R5 7.5.1's `StreetLayer.loadFromOsm` makes them.

use std::ops::Range;

use rustc_hash::FxHashMap as HashMap;

use crate::osm::Osm;
use crate::permissions::{self, Walk};
use crate::snap::Index;
use crate::{Mm, Split};

/// The Earth's radius R5 measures with (`GeometryUtils.RADIUS_OF_EARTH_M`).
const EARTH_RADIUS_M: f64 = 6_367_450.0;

/// Walking is taken from pieces of the network with fewer vertices than this,
/// as R5 does (`StreetLayer.MIN_SUBGRAPH_SIZE`).
const MIN_PIECE: usize = 40;

/// A street between two vertices, walkable one way, both, or neither.
#[derive(Clone, Debug)]
pub struct Edge {
    pub from: u32,
    pub to: u32,
    pub length: Mm,
    pub walk: Walk,
    /// The OSM way it's along.
    pub way: i64,
    /// Whether points may be linked to it (`permissions::linkable`).
    pub linkable: bool,
    /// Its `(latitude, longitude)`s, from `from` to `to`, in `Graph::points`.
    pub geometry: Range<u32>,
}

#[derive(Debug, Default)]
pub struct Graph {
    /// Each vertex's `(latitude, longitude)`.
    pub vertices: Vec<(f64, f64)>,
    pub edges: Vec<Edge>,
    /// Every edge's geometry, one after another.
    pub points: Vec<(f64, f64)>,
    /// `(to, length, edge)` of each walkable edge out of each vertex, from `out_start[v]`.
    pub(crate) out: Vec<(u32, Mm, u32)>,
    pub(crate) out_start: Vec<u32>,
    pub(crate) index: Index,
}

/// The great-circle distance between two `(latitude, longitude)`s, in meters, as R5 measures it.
pub fn distance_m((lat0, lon0): (f64, f64), (lat1, lon1): (f64, f64)) -> f64 {
    let (theta0, theta1) = (lat0.to_radians(), lat1.to_radians());
    let half_dlat = (theta1 - theta0) / 2.0;
    let half_dlon = (lon1.to_radians() - lon0.to_radians()) / 2.0;
    let under = half_dlat.sin().powi(2) + theta0.cos() * theta1.cos() * half_dlon.sin().powi(2);
    2.0 * EARTH_RADIUS_M * under.sqrt().asin()
}

impl Graph {
    /// The network `osm`'s ways make,
    /// split into edges at intersections, impassable nodes, and their ends.
    pub fn build(osm: &Osm) -> Self {
        Self::build_pruning(osm, MIN_PIECE)
    }

    fn build_pruning(osm: &Osm, min_piece: usize) -> Self {
        let mut graph = Self::default();
        let mut vertex_of: HashMap<i64, u32> = HashMap::default();
        for way in &osm.ways {
            let walk = permissions::walk(&way.tags);
            if !walk.forward && !walk.backward {
                continue;
            }
            let linkable = permissions::linkable(&way.tags);
            let mut begin = 0;
            for n in 1..way.nodes.len() {
                let node = way.nodes[n];
                // Like R5, a way stops at a node the data lacks.
                if !osm.nodes.contains_key(&node) {
                    break;
                }
                let last = n == way.nodes.len() - 1;
                if osm.intersections.contains(&node) || last || osm.impassable.contains(&node) {
                    let nodes = &way.nodes[begin..=n];
                    graph.add_edge(osm, &mut vertex_of, way.id, nodes, walk, linkable);
                    begin = n;
                }
            }
        }
        graph.remove_islands(min_piece);
        graph.link();
        graph
    }

    fn add_edge(
        &mut self,
        osm: &Osm,
        vertex_of: &mut HashMap<i64, u32>,
        way: i64,
        nodes: &[i64],
        walk: Walk,
        linkable: bool,
    ) {
        if nodes.iter().any(|id| !osm.nodes.contains_key(id)) {
            return;
        }
        // An impassable node, like a locked gate, is a new vertex at each edge that reaches it,
        // so no walk passes through it, as R5 does (`StreetLayer.getVertexIndexForOsmNode`).
        let mut vertex = |id: i64, vertices: &mut Vec<(f64, f64)>| {
            let mut add = || {
                vertices.push(osm.nodes[&id]);
                (vertices.len() - 1) as u32
            };
            if osm.impassable.contains(&id) {
                add()
            } else {
                *vertex_of.entry(id).or_insert_with(add)
            }
        };
        let from = vertex(nodes[0], &mut self.vertices);
        let to = vertex(nodes[nodes.len() - 1], &mut self.vertices);
        let start = self.points.len() as u32;
        self.points.extend(nodes.iter().map(|id| osm.nodes[id]));
        let geometry = start..self.points.len() as u32;
        let length_m: f64 = self.points[start as usize..]
            .windows(2)
            .map(|p| distance_m(p[0], p[1]))
            .sum();
        // Truncated to whole millimeters, as R5 does.
        let length = (length_m * 1000.0) as Mm;
        self.edges.push(Edge {
            from,
            to,
            length,
            walk,
            way,
            linkable,
            geometry,
        });
    }

    /// Takes walking from strongly connected pieces with fewer than `min_piece` vertices,
    /// along every edge touching them, as R5's `TarjanIslandPruner` does.
    fn remove_islands(&mut self, min_piece: usize) {
        let n = self.vertices.len();
        let mut out = vec![Vec::new(); n];
        for e in &self.edges {
            if e.walk.forward {
                out[e.from as usize].push(e.to);
            }
            if e.walk.backward {
                out[e.to as usize].push(e.from);
            }
        }
        let piece = strong_components(&out);
        let mut sizes = vec![0usize; n];
        for &p in &piece {
            sizes[p as usize] += 1;
        }
        let small = |v: u32| sizes[piece[v as usize] as usize] < min_piece;
        for e in &mut self.edges {
            if small(e.from) || small(e.to) {
                e.walk = Walk {
                    forward: false,
                    backward: false,
                };
            }
        }
    }

    /// Builds the adjacency searches walk and the index snapping finds edges by.
    fn link(&mut self) {
        let n = self.vertices.len();
        let mut out = vec![Vec::new(); n];
        for (i, e) in self.edges.iter().enumerate() {
            if e.walk.forward {
                out[e.from as usize].push((e.to, e.length, i as u32));
            }
            if e.walk.backward {
                out[e.to as usize].push((e.from, e.length, i as u32));
            }
        }
        self.out_start = Vec::with_capacity(n + 1);
        self.out = Vec::new();
        for edges in out {
            self.out_start.push(self.out.len() as u32);
            self.out.extend(edges);
        }
        self.out_start.push(self.out.len() as u32);
        self.index = Index::build(self);
    }

    /// The walkable edges out of `v`, as `(to, length, edge)`.
    pub fn out(&self, v: u32) -> &[(u32, Mm, u32)] {
        &self.out[self.out_start[v as usize] as usize..self.out_start[v as usize + 1] as usize]
    }

    /// `e`'s `(latitude, longitude)`s.
    pub fn geometry(&self, e: u32) -> &[(f64, f64)] {
        let g = &self.edges[e as usize].geometry;
        &self.points[g.start as usize..g.end as usize]
    }

    /// Where `(lat, lon)` links to the network, as R5 links points:
    /// the nearest linkable edge walkable both ways, within 300 m, or failing that, 1600 m.
    pub fn snap(&self, lat: f64, lon: f64) -> Option<Split> {
        self.index
            .nearest(self, lat, lon, 300.0)
            .or_else(|| self.index.nearest(self, lat, lon, 1600.0))
    }
}

/// Each vertex's strongly connected component, by Tarjan's algorithm, without recursion.
fn strong_components(out: &[Vec<u32>]) -> Vec<u32> {
    const UNSEEN: u32 = u32::MAX;
    let n = out.len();
    let mut index = vec![UNSEEN; n];
    let mut low = vec![0u32; n];
    let mut on_stack = vec![false; n];
    let mut stack = Vec::new();
    let mut component = vec![UNSEEN; n];
    let mut components = 0;
    let mut next = 0;
    // `(vertex, next of its edges to follow)`.
    let mut calls: Vec<(u32, usize)> = Vec::new();
    for root in 0..n as u32 {
        if index[root as usize] != UNSEEN {
            continue;
        }
        calls.push((root, 0));
        while let Some(&(v, i)) = calls.last() {
            let vu = v as usize;
            if index[vu] == UNSEEN {
                index[vu] = next;
                low[vu] = next;
                next += 1;
                stack.push(v);
                on_stack[vu] = true;
            }
            if let Some(&w) = out[vu].get(i) {
                if let Some(call) = calls.last_mut() {
                    call.1 += 1;
                }
                let wu = w as usize;
                if index[wu] == UNSEEN {
                    calls.push((w, 0));
                } else if on_stack[wu] {
                    low[vu] = low[vu].min(index[wu]);
                }
                continue;
            }
            calls.pop();
            if let Some(&(parent, _)) = calls.last() {
                low[parent as usize] = low[parent as usize].min(low[vu]);
            }
            if low[vu] == index[vu] {
                while let Some(w) = stack.pop() {
                    on_stack[w as usize] = false;
                    component[w as usize] = components;
                    if w == v {
                        break;
                    }
                }
                components += 1;
            }
        }
    }
    component
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::Search;
    use crate::osm::Way;

    #[test]
    fn components() {
        // 0 <-> 1 -> 2 <-> 3, and 4 alone.
        let out = vec![vec![1], vec![0, 2], vec![3], vec![2], vec![]];
        let c = strong_components(&out);
        assert_eq!(c[0], c[1]);
        assert_eq!(c[2], c[3]);
        assert_ne!(c[0], c[2]);
        assert_ne!(c[4], c[0]);
        assert_ne!(c[4], c[2]);
    }

    /// Way 1 west to east through nodes 1, 2, 3, 0.001 degrees of longitude apart,
    /// and way 2 north from node 2 to 4, a tunnel, so not linkable.
    /// Node 5 is a pond's: on no way.
    fn osm() -> Osm {
        let tags = |pairs: &[(&str, &str)]| {
            pairs
                .iter()
                .map(|&(k, v)| (k.to_owned(), v.to_owned()))
                .collect()
        };
        let mut osm = Osm::default();
        for (id, at) in [
            (1, (40.7, -74.002)),
            (2, (40.7, -74.001)),
            (3, (40.7, -74.0)),
            (4, (40.701, -74.001)),
        ] {
            osm.nodes.insert(id, at);
        }
        osm.ways.push(Way {
            id: 1,
            nodes: vec![1, 2, 3],
            tags: tags(&[("highway", "residential")]),
        });
        osm.ways.push(Way {
            id: 2,
            nodes: vec![2, 4],
            tags: tags(&[("highway", "footway"), ("tunnel", "yes")]),
        });
        osm.intersections.insert(2);
        osm
    }

    #[test]
    fn edges_split_at_intersections() {
        let g = Graph::build_pruning(&osm(), 0);
        assert_eq!(g.vertices.len(), 4);
        assert_eq!(g.edges.len(), 3);
        // About 84 m a thousandth of a degree east at this latitude.
        let e = &g.edges[0];
        let expected = distance_m((40.7, -74.002), (40.7, -74.001));
        assert_eq!(e.length, (expected * 1000.0) as Mm);
        assert!((84_000..85_000).contains(&e.length), "{}", e.length);
    }

    #[test]
    fn impassable_nodes_join_nothing() {
        let mut osm = osm();
        osm.impassable.insert(2);
        let g = Graph::build_pruning(&osm, 0);
        // Node 2 is a vertex for each of its three edges.
        assert_eq!(g.vertices.len(), 6);
        let (a, b) = (
            g.snap(40.7, -74.0015).unwrap(),
            g.snap(40.7, -74.0005).unwrap(),
        );
        let mut search = Search::new(&g);
        search.run(&a, 1_000_000);
        assert_eq!(search.to(&b), None);
    }

    #[test]
    fn small_pieces_lose_walking() {
        let g = Graph::build_pruning(&osm(), 5);
        assert!(g.edges.iter().all(|e| !e.walk.forward && !e.walk.backward));
        assert!(g.snap(40.7, -74.0015).is_none());
    }

    #[test]
    fn snap_and_search() {
        let g = Graph::build_pruning(&osm(), 0);
        // Just south of the middle of the first edge, not the tunnel's.
        let a = g.snap(40.6999, -74.0015).unwrap();
        assert_eq!(a.edge, 0);
        // Halfway, measured flat as R5 measures along an edge,
        // which is a few centimeters off its length measured round.
        assert_eq!(a.d0 + a.d1, g.edges[0].length);
        assert!(a.d0.abs_diff(a.d1) < 50, "{a:?}");
        assert!((11_000..11_200).contains(&a.to_edge), "{a:?}");
        // Near the tunnel's top, it still links to the street.
        assert_ne!(g.snap(40.7009, -74.001).unwrap().edge, 2);
        // East of node 3, at the end of the second edge.
        let b = g.snap(40.7, -73.9995).unwrap();
        assert_eq!(b.edge, 1);
        assert!(b.d1 < 50, "{b:?}");
        let mut search = Search::new(&g);
        search.run(&a, 1_000_000);
        let to_b = search.to(&b).unwrap();
        let by_either_end = (g.edges[1].length + b.d1).min(b.d0);
        assert_eq!(to_b, a.to_edge + a.d1 + by_either_end + b.to_edge);
        // Along its own edge, not around by its ends.
        let c = g.snap(40.7001, -74.0012).unwrap();
        assert_eq!(c.edge, 0);
        assert_eq!(search.to(&c), a.along(&c));
        // Not within a limit shorter than the walk.
        search.run(&a, 50_000);
        assert_eq!(search.to(&b), None);
    }

    #[test]
    fn distances_as_r5_measures() {
        // A degree of latitude on R5's sphere.
        let m = distance_m((40.0, -74.0), (41.0, -74.0));
        assert!((m - EARTH_RADIUS_M.to_radians()).abs() < 1e-6, "{m}");
    }
}
