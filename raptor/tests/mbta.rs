//! Pathways transfers on the MBTA's GTFS, which has `pathways.txt`:
//! `tests/data/mbta-downtown`, cut by `mta-od-data fetch-mbta`,
//! and the whole pinned version, if fetched, by `cargo test -- --ignored`.

use std::collections::HashMap;
use std::path::Path;

use jiff::civil::Date;
use raptor::gtfs::{Feed, Secs};
use raptor::pathways::{MAX_WALK, Walk, walks};
use raptor::raptor::Router;
use raptor::timetable::Timetable;

const FIXTURE: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/tests/data/mbta-downtown");
const FULL: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../data/mbta-gtfs/20261020.zip"
);
const PENALTY: Secs = 600;

fn day() -> Date {
    Date::new(2026, 10, 28).unwrap()
}

fn fixture() -> Feed {
    let names = [
        "stops.txt",
        "trips.txt",
        "stop_times.txt",
        "calendar.txt",
        "calendar_dates.txt",
        "pathways.txt",
        "transfers.txt",
    ];
    let texts: Vec<String> = names
        .iter()
        .map(|n| std::fs::read_to_string(Path::new(FIXTURE).join(n)).unwrap())
        .collect();
    let mut files: HashMap<&str, &str> = names
        .iter()
        .copied()
        .zip(texts.iter().map(String::as_str))
        .collect();
    Feed::load(&mut files).unwrap()
}

fn walk(tt: &Timetable, walks: &[Walk], from: &str, to: &str) -> Option<(Secs, u8)> {
    let (from, to) = (tt.stop(from).unwrap(), tt.stop(to).unwrap());
    walks
        .iter()
        .find(|w| (w.from, w.to) == (from, to))
        .map(|w| (w.secs, w.exits))
}

#[test]
fn downtown_walks() {
    let feed = fixture();
    let tt = Timetable::build(&feed, day()).unwrap();
    let (walks, report) = walks(&feed, &tt, PENALTY, MAX_WALK);
    assert_eq!(report.boarding_areas, 0);

    // Park St's Red Line island, either side, and its westbound Green Line berths.
    assert_eq!(walk(&tt, &walks, "70075", "70076"), Some((0, 0)));
    assert_eq!(walk(&tt, &walks, "70076", "70075"), Some((0, 0)));
    assert_eq!(walk(&tt, &walks, "70196", "70197"), Some((0, 0)));
    // Red Line to Green, up the stairs.
    let (red_to_green, out) = walk(&tt, &walks, "70076", "70196").unwrap();
    assert!(
        (30..=120).contains(&red_to_green) && out == 0,
        "{red_to_green}"
    );
    // To Downtown Crossing's Red Line through the Winter St concourse, staying in.
    let (concourse, out) = walk(&tt, &walks, "70196", "70077").unwrap();
    assert!((180..=420).contains(&concourse) && out == 0, "{concourse}");
    // North Station's Orange and Green Lines share the paid area,
    // as every subway platform here shares one with the others it reaches
    // (its commuter rail, behind gates of its own, has no trips in the fixture).
    assert_eq!(walk(&tt, &walks, "70026", "70205").map(|w| w.1), Some(0));
    assert!(walks.iter().all(|w| w.exits == 0));
}

#[test]
fn government_center_to_downtown_crossing() {
    let feed = fixture();
    let mut tt = Timetable::build(&feed, day()).unwrap();
    let (walks, report) = walks(&feed, &tt, PENALTY, MAX_WALK);
    tt.use_pathways(&walks, &report.covered);
    let router = Router::new(&tt);
    let from: Vec<_> = tt.stops_at("place-gover").to_vec();
    let to: Vec<_> = tt.stops_at("place-dwnxg").to_vec();
    let eight = 8 * 3600;
    let (_, journeys) = router.query(&from, eight).journeys(&to);
    // A Green Line train to Park St, and the Red Line or the concourse on.
    let first = journeys.iter().map(|j| j.arrive).min().unwrap();
    assert!(first - eight <= 20 * 60, "{}", first - eight);
}

#[test]
#[ignore = "needs the full feed, from `mta-od-data fetch-mbta`"]
fn whole_feed() {
    let feed = Feed::open(Path::new(FULL)).unwrap();
    let mut tt = Timetable::build(&feed, day()).unwrap();
    let (walks, report) = walks(&feed, &tt, PENALTY, MAX_WALK);
    assert_eq!(
        (
            report.pathways,
            report.stops,
            report.walks,
            report.level_walks,
            report.exit_walks
        ),
        (9309, 321, 1344, 517, 18)
    );
    // Shortest walks are closed: none beats going by way of a third stop.
    let at: HashMap<(u32, u32), &Walk> = walks.iter().map(|w| ((w.from, w.to), w)).collect();
    for a in &walks {
        for b in walks.iter().filter(|b| b.from == a.to && b.to != a.from) {
            if let Some(c) = at.get(&(a.from, b.to))
                && a.exits == 0
                && b.exits == 0
                && c.exits == 0
                && a.secs > 0
                && b.secs > 0
                && c.secs > 0
            {
                assert!(c.secs <= a.secs + b.secs, "{a:?} {b:?} {c:?}");
            }
        }
    }
    // Between two of a station's stops with pathways, every footpath is a walk.
    tt.use_pathways(&walks, &report.covered);
    for &a in &report.covered {
        for &(b, secs) in &tt.footpaths[a as usize] {
            if report.covered.contains(&b) && tt.same_station(a, b) {
                assert_eq!(at.get(&(a, b)).map(|w| w.secs), Some(secs), "{a} {b}");
            }
        }
    }
}
