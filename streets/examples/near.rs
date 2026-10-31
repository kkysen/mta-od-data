//! The ways near a point, whether one may walk them and link to them, nearest first:
//! `cargo run --release --example near -- <.osm.pbf> <lat> <lon> <meters>`.

use std::path::PathBuf;

use streets::Graph;
use streets::graph::distance_m;
use streets::osm::Osm;
use streets::permissions;

fn main() -> anyhow::Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let osm = Osm::read(&PathBuf::from(&args[0]))?;
    let (lat, lon, radius): (f64, f64, f64) =
        (args[1].parse()?, args[2].parse()?, args[3].parse()?);
    let graph = Graph::build(&osm);
    let mut near: Vec<(f64, i64)> = Vec::new();
    for e in 0..graph.edges.len() as u32 {
        // Near enough by any of its points, which is close enough for a listing.
        let d = graph
            .geometry(e)
            .iter()
            .map(|&p| distance_m(p, (lat, lon)))
            .fold(f64::INFINITY, f64::min);
        if d <= radius {
            near.push((d, graph.edges[e as usize].way));
        }
    }
    near.sort_by(|a, b| a.0.total_cmp(&b.0));
    near.dedup_by_key(|n| n.1);
    for (d, id) in near {
        let way = osm.ways.iter().find(|w| w.id == id).expect("a way");
        let walk = graph
            .edges
            .iter()
            .filter(|e| e.way == id)
            .map(|e| (e.walk.forward, e.walk.backward))
            .collect::<Vec<_>>();
        let tags: Vec<String> = [
            "highway", "name", "footway", "access", "foot", "tunnel", "bridge", "sidewalk",
        ]
        .iter()
        .filter_map(|k| way.tags.get(k).map(|v| format!("{k}={v}")))
        .collect();
        println!(
            "{d:>5.0} m way {id} walk(rules)={:?} walk(after islands)={walk:?} linkable={} {}",
            permissions::walk(&way.tags),
            permissions::linkable(&way.tags),
            tags.join(" ")
        );
    }
    Ok(())
}
