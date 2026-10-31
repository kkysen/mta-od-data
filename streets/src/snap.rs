//! Linking a point to the nearest edge, as R5 7.5.1's `Split.find` does:
//! measured flat, with longitude scaled by the cosine of the point's latitude.

use rustc_hash::FxHashMap as HashMap;

use crate::{Graph, Mm};

/// Meters in a degree of latitude, as R5 links with.
const M_PER_DEGREE: f64 = 111_111.111;

/// The size of the index's cells, in degrees.
const CELL: f64 = 0.002;

/// Where a point links to an edge.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Split {
    pub edge: u32,
    /// The edge's ends.
    pub v0: u32,
    pub v1: u32,
    /// Along the edge, from `v0` and from `v1`.
    pub d0: Mm,
    pub d1: Mm,
    /// From the point to the edge.
    pub to_edge: Mm,
}

impl Split {
    /// The edge's ends, and how far each is from the point.
    pub fn ends(&self) -> [(u32, Mm); 2] {
        [
            (self.v0, self.to_edge + self.d0),
            (self.v1, self.to_edge + self.d1),
        ]
    }

    /// Straight along the edge from this point to `other`'s, if they're on the same one.
    pub fn along(&self, other: &Split) -> Option<Mm> {
        (self.edge == other.edge).then(|| self.to_edge + self.d0.abs_diff(other.d0) + other.to_edge)
    }
}

/// The edges points may link to, by the cells of a grid they pass through.
#[derive(Debug, Default)]
pub(crate) struct Index {
    cells: HashMap<(i32, i32), Vec<u32>>,
}

fn cell(lat: f64, lon: f64) -> (i32, i32) {
    ((lat / CELL).floor() as i32, (lon / CELL).floor() as i32)
}

impl Index {
    /// Indexes the edges points may link to: linkable, and walkable both ways.
    pub(crate) fn build(graph: &Graph) -> Self {
        let mut cells: HashMap<(i32, i32), Vec<u32>> = HashMap::default();
        for (e, edge) in graph.edges.iter().enumerate() {
            if !(edge.linkable && edge.walk.forward && edge.walk.backward) {
                continue;
            }
            for segment in graph.geometry(e as u32).windows(2) {
                let ((lat0, lon0), (lat1, lon1)) = (segment[0], segment[1]);
                let (y0, x0) = cell(lat0.min(lat1), lon0.min(lon1));
                let (y1, x1) = cell(lat0.max(lat1), lon0.max(lon1));
                for y in y0..=y1 {
                    for x in x0..=x1 {
                        let edges = cells.entry((y, x)).or_default();
                        if edges.last() != Some(&(e as u32)) {
                            edges.push(e as u32);
                        }
                    }
                }
            }
        }
        Self { cells }
    }

    /// The nearest indexed edge to `(lat, lon)` within `radius_m`, on the lowest-numbered edge of any tie.
    pub(crate) fn nearest(
        &self,
        graph: &Graph,
        lat: f64,
        lon: f64,
        radius_m: f64,
    ) -> Option<Split> {
        let cos_lat = lat.to_radians().cos();
        let radius_lat = radius_m / M_PER_DEGREE;
        let radius_lon = radius_lat / cos_lat;
        let (y0, x0) = cell(lat - radius_lat, lon - radius_lon);
        let (y1, x1) = cell(lat + radius_lat, lon + radius_lon);
        let mut candidates: Vec<u32> = (y0..=y1)
            .flat_map(|y| (x0..=x1).map(move |x| (y, x)))
            .filter_map(|c| self.cells.get(&c))
            .flatten()
            .copied()
            .collect();
        candidates.sort_unstable();
        candidates.dedup();
        // Flat, in degrees of latitude.
        let flat = |(la, lo): (f64, f64)| ((lo - lon) * cos_lat, la - lat);
        // `(squared distance, edge, segment, fraction along it)`.
        let mut best: Option<(f64, u32, usize, f64)> = None;
        for e in candidates {
            for (seg, s) in graph.geometry(e).windows(2).enumerate() {
                let ((x0, y0), (x1, y1)) = (flat(s[0]), flat(s[1]));
                let (dx, dy) = (x1 - x0, y1 - y0);
                let length2 = dx * dx + dy * dy;
                let frac = if length2 == 0.0 {
                    0.0
                } else {
                    (-(x0 * dx + y0 * dy) / length2).clamp(0.0, 1.0)
                };
                let (x, y) = (x0 + frac * dx, y0 + frac * dy);
                let d2 = x * x + y * y;
                if d2 < radius_lat * radius_lat && best.is_none_or(|(b, ..)| d2 < b) {
                    best = Some((d2, e, seg, frac));
                }
            }
        }
        let (d2, e, seg, frac) = best?;
        let edge = &graph.edges[e as usize];
        let before: f64 = graph.geometry(e)[..=seg + 1]
            .windows(2)
            .enumerate()
            .map(|(i, s)| {
                let ((x0, y0), (x1, y1)) = (flat(s[0]), flat(s[1]));
                let length = ((x1 - x0).powi(2) + (y1 - y0).powi(2)).sqrt();
                if i == seg { length * frac } else { length }
            })
            .sum();
        let d0 = ((before * M_PER_DEGREE * 1000.0) as Mm).min(edge.length);
        Some(Split {
            edge: e,
            v0: edge.from,
            v1: edge.to,
            d0,
            d1: edge.length - d0,
            to_edge: (d2.sqrt() * M_PER_DEGREE * 1000.0) as Mm,
        })
    }
}
