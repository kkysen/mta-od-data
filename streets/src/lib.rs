//! Walking on OpenStreetMap's streets, as R5 7.5.1 walks them,
//! for walks to stops, from them, and between them.
//!
//! Distances are in millimeters, not seconds,
//! so that walks are timed at whatever speed afterwards, by dividing.
//! R5 times walking from a point (not a stop) in whole seconds per edge, rounded up,
//! so its walks from origins run a little longer than these, by up to a second an edge.

pub mod graph;
pub mod osm;
pub mod permissions;
pub mod search;
pub mod snap;

pub use graph::Graph;
pub use search::Search;
pub use snap::Split;

/// A distance, in millimeters.
pub type Mm = u32;
