//! What `Graph::build` makes of an `.osm.pbf`: `cargo run --release --example stats -- <path>`.

use std::path::PathBuf;
use std::time::Instant;

use streets::Graph;
use streets::osm::Osm;

fn main() -> anyhow::Result<()> {
    let path = PathBuf::from(std::env::args().nth(1).expect("an .osm.pbf"));
    let start = Instant::now();
    let osm = Osm::read(&path)?;
    println!(
        "read {} nodes, {} routable ways, {} intersections in {:.1?}",
        osm.nodes.len(),
        osm.ways.len(),
        osm.intersections.len(),
        start.elapsed()
    );
    let start = Instant::now();
    let graph = Graph::build(&osm);
    let walkable = graph
        .edges
        .iter()
        .filter(|e| e.walk.forward || e.walk.backward)
        .count();
    println!(
        "built {} vertices, {} edges ({walkable} walkable) in {:.1?}",
        graph.vertices.len(),
        graph.edges.len(),
        start.elapsed()
    );
    Ok(())
}
