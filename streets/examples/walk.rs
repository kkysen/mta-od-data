//! The shortest walk between two points, and the ways it takes:
//! `cargo run --release --example walk -- <.osm.pbf> <lat> <lon> <lat> <lon>`.

use std::path::PathBuf;

use rustc_hash::FxHashMap as HashMap;
use streets::osm::{Osm, Way};
use streets::{Graph, Search, Split};

fn describe(ways: &HashMap<i64, &Way>, way: i64) -> String {
    let tags = &ways[&way].tags;
    let tag = |k| tags.get(k).map(|v| format!(" {k}={v}")).unwrap_or_default();
    format!(
        "way {way}{}{}{}{}{}{}",
        tag("highway"),
        tag("name"),
        tag("footway"),
        tag("access"),
        tag("foot"),
        tag("tunnel")
    )
}

fn main() -> anyhow::Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let path = PathBuf::from(&args[0]);
    let coord = |i: usize| args[i].parse::<f64>();
    let osm = Osm::read(&path)?;
    let ways: HashMap<i64, &Way> = osm.ways.iter().map(|w| (w.id, w)).collect();
    let graph = Graph::build(&osm);
    let snap = |lat, lon| -> anyhow::Result<Split> {
        let s = graph
            .snap(lat, lon)
            .ok_or_else(|| anyhow::anyhow!("{lat},{lon} links to no street"))?;
        let e = &graph.edges[s.edge as usize];
        println!(
            "{lat},{lon} links {:.0} m off {}, {:.0} m from one end",
            f64::from(s.to_edge) / 1000.0,
            describe(&ways, e.way),
            f64::from(s.d0) / 1000.0
        );
        Ok(s)
    };
    let (from, to) = (snap(coord(1)?, coord(2)?)?, snap(coord(3)?, coord(4)?)?);
    let mut search = Search::new(&graph);
    search.run(&from, 20_000_000);
    let Some(mm) = search.to(&to) else {
        println!("unreachable within 20 km");
        return Ok(());
    };
    println!("{:.0} m:", f64::from(mm) / 1000.0);
    let mut last = None;
    let mut length = 0;
    let edges = search.path(&to).unwrap_or_default();
    for (i, &e) in edges.iter().enumerate() {
        let edge = &graph.edges[e as usize];
        length += edge.length;
        let next = edges.get(i + 1).map(|&n| graph.edges[n as usize].way);
        if next != Some(edge.way) && last != Some((edge.way, length)) {
            let (lat, lon) = graph.vertices[edge.to as usize];
            println!(
                "  {:>6.0} m on {} (to {lat:.6},{lon:.6})",
                f64::from(length) / 1000.0,
                describe(&ways, edge.way)
            );
            last = Some((edge.way, length));
            length = 0;
        }
    }
    Ok(())
}
