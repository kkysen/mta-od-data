//! Shortest walks from a point or stop to every vertex within a distance.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

use crate::{Graph, Mm, Split};

const UNREACHED: Mm = Mm::MAX;
const NO_EDGE: u32 = u32::MAX;

/// A search's distances to vertices, kept between searches,
/// so that one per thread does every search on it without reallocating.
pub struct Search<'a> {
    graph: &'a Graph,
    dist: Vec<Mm>,
    /// The edge each reached vertex was last reached along, `NO_EDGE` for a start.
    via: Vec<u32>,
    reached: Vec<u32>,
    heap: BinaryHeap<Reverse<(Mm, u32)>>,
    /// The latest search's start, if from a point, for reaching points on its own edge.
    from: Option<Split>,
}

impl<'a> Search<'a> {
    pub fn new(graph: &'a Graph) -> Self {
        Self {
            graph,
            dist: vec![UNREACHED; graph.vertices.len()],
            via: vec![NO_EDGE; graph.vertices.len()],
            reached: Vec::new(),
            heap: BinaryHeap::new(),
            from: None,
        }
    }

    /// Searches from `from` to every vertex within `limit`.
    pub fn run(&mut self, from: &Split, limit: Mm) {
        self.from = Some(*from);
        self.search(&from.ends(), limit);
    }

    /// Searches from vertices at the given distances to every vertex within `limit`.
    pub fn run_from_vertices(&mut self, sources: &[(u32, Mm)], limit: Mm) {
        self.from = None;
        self.search(sources, limit);
    }

    fn search(&mut self, sources: &[(u32, Mm)], limit: Mm) {
        for &v in &self.reached {
            self.dist[v as usize] = UNREACHED;
        }
        self.reached.clear();
        self.heap.clear();
        for &(v, d) in sources {
            self.lower(v, d, limit, NO_EDGE);
        }
        while let Some(Reverse((d, v))) = self.heap.pop() {
            if d > self.dist[v as usize] {
                continue;
            }
            for &(to, length, edge) in self.graph.out(v) {
                self.lower(to, d.saturating_add(length), limit, edge);
            }
        }
    }

    fn lower(&mut self, v: u32, d: Mm, limit: Mm, via: u32) {
        let current = &mut self.dist[v as usize];
        if d > limit || d >= *current {
            return;
        }
        if *current == UNREACHED {
            self.reached.push(v);
        }
        *current = d;
        self.via[v as usize] = via;
        self.heap.push(Reverse((d, v)));
    }

    /// Every vertex the latest search reached, and how far.
    pub fn reached(&self) -> impl Iterator<Item = (u32, Mm)> + '_ {
        self.reached.iter().map(|&v| (v, self.dist[v as usize]))
    }

    /// How far the latest search reached `to`, by either end of its edge,
    /// or along its edge if the search started on the same one.
    pub fn to(&self, to: &Split) -> Option<Mm> {
        let by_ends = to
            .ends()
            .iter()
            .map(|&(v, d)| self.dist[v as usize].saturating_add(d))
            .min()
            .filter(|&d| d < UNREACHED);
        let along = self.from.and_then(|from| from.along(to));
        by_ends.into_iter().chain(along).min()
    }

    /// The edges of the latest search's shortest walk to `to`, from its start,
    /// not counting `to`'s own edge; empty if along the edge the search started on.
    pub fn path(&self, to: &Split) -> Option<Vec<u32>> {
        let best = self.to(to)?;
        if self.from.and_then(|from| from.along(to)) == Some(best) {
            return Some(Vec::new());
        }
        let (mut v, _) = to
            .ends()
            .into_iter()
            .find(|&(v, d)| self.dist[v as usize].saturating_add(d) == best)?;
        let mut edges = Vec::new();
        while self.via[v as usize] != NO_EDGE {
            let e = self.via[v as usize];
            edges.push(e);
            let edge = &self.graph.edges[e as usize];
            v = if edge.to == v { edge.from } else { edge.to };
        }
        edges.reverse();
        Some(edges)
    }
}
