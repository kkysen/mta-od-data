//! Passages inside the fare gates between complexes the MTA lists apart
//! (`raptor/passages.json5`), like the 42 St Connection
//! between 42 St-Bryant Pk/5 Av and Times Sq-42 St,
//! which neither the station data nor `transfers.txt` joins.
//!
//! A passage runs from one stop's platform to another's,
//! timed as a complex's other walks between platforms are under OSM transfers:
//! the straight-line distance between their stops at the walking speed (`Speeds`),
//! plus a flight of stairs a level between them.
//! Every stop of either complex walks to every stop of the other through it,
//! by its complex's own walks to and from the passage's ends,
//! as RAPTOR takes one footpath a change.
//! It's open while its route runs at its far end,
//! from its first departure to its last arrival there on the date,
//! and walked only when started then.

use std::collections::HashMap;

use anyhow::{Context, Result};
use serde::Deserialize;

use crate::gtfs::Secs;
use crate::od::{ComplexId, Complexes};
use crate::speeds::Speeds;
use crate::timetable::{StopIdx, Timetable, distance_m};

#[derive(Clone, Debug, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct Passage {
    pub name: String,
    /// The two complexes it joins, in the order `ridership` names them together.
    pub complexes: [ComplexId; 2],
    /// The stations at either end, by GTFS stop ID.
    pub from: String,
    pub to: String,
    /// Levels of stairs between them.
    pub levels: u8,
    /// The route whose trains at `to` it's open while they run.
    pub open_with_route: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct File {
    passages: Vec<Passage>,
}

/// `raptor/passages.json5`'s passages, built in, so every run walks the same ones.
pub fn load() -> Result<Vec<Passage>> {
    let file: File =
        json5::from_str(include_str!("../passages.json5")).context("parsing passages.json5")?;
    Ok(file.passages)
}

impl Timetable {
    /// Walks between `complexes` through each of `passages`,
    /// climbing `secs_per_level` a level, while each is open.
    /// A passage whose route doesn't run at its far end on this date is closed all day,
    /// and one with an end the timetable doesn't serve is left out.
    pub fn use_passages(
        &mut self,
        passages: &[Passage],
        complexes: &Complexes,
        secs_per_level: Secs,
        speeds: &Speeds,
    ) {
        for p in passages {
            let (from, to) = (
                self.stops_at(&p.from).to_vec(),
                self.stops_at(&p.to).to_vec(),
            );
            let Some(hours) = self.route_hours(&p.open_with_route, &to) else {
                continue;
            };
            let climb = secs_per_level * Secs::from(p.levels);
            // Through the passage between each end's stops, by their platforms' positions.
            let mut through: Vec<(StopIdx, StopIdx, Secs)> = Vec::new();
            for &f in &from {
                for &t in &to {
                    let (Some(a), Some(b)) =
                        (self.stops[f as usize].coords, self.stops[t as usize].coords)
                    else {
                        continue;
                    };
                    through.push((f, t, climb + speeds.walk_secs(distance_m(a, b)) as Secs));
                }
            }
            let stops = |c: ComplexId| complexes.stops.get(&c).map_or(&[][..], Vec::as_slice);
            // `from`'s complex first.
            let [mut ours, mut theirs] = p.complexes.map(stops);
            if from.iter().any(|f| theirs.contains(f)) {
                (ours, theirs) = (theirs, ours);
            }
            let mut walks: HashMap<(StopIdx, StopIdx), Secs> = HashMap::new();
            for &a in ours {
                for &b in theirs {
                    for &(f, t, secs) in &through {
                        let there = self.walk(a, f).zip(self.walk(t, b));
                        let back = self.walk(b, t).zip(self.walk(f, a));
                        for (key, legs) in [((a, b), there), ((b, a), back)] {
                            let Some((x, y)) = legs else { continue };
                            let walk = walks.entry(key).or_insert(Secs::MAX);
                            *walk = (*walk).min(x + secs + y);
                        }
                    }
                }
            }
            for ((a, b), walk) in walks {
                let paths = &mut self.footpaths[a as usize];
                match paths.iter_mut().find(|(s, _)| *s == b) {
                    Some((_, t)) => *t = (*t).min(walk),
                    None => paths.push((b, walk)),
                }
                self.footpath_hours.insert((a, b), hours);
                let from = a as usize;
                if self.has_hours.len() <= from {
                    self.has_hours.resize(self.stops.len(), false);
                }
                self.has_hours[from] = true;
            }
        }
    }

    /// How long walking from `a` to `b` takes within a complex: 0 if they're one stop.
    fn walk(&self, a: StopIdx, b: StopIdx) -> Option<Secs> {
        if a == b {
            return Some(0);
        }
        self.footpaths[a as usize]
            .iter()
            .find(|&&(s, _)| s == b)
            .map(|&(_, walk)| walk)
    }

    /// From `route`'s first departure at any of `stops` to its last arrival there.
    fn route_hours(&self, route: &str, stops: &[StopIdx]) -> Option<(Secs, Secs)> {
        let mut hours: Option<(Secs, Secs)> = None;
        for p in self.patterns.iter().filter(|p| p.route_id == route) {
            for (pos, s) in p.stops.iter().enumerate() {
                if !stops.contains(s) {
                    continue;
                }
                // Not the previous or next date's, shifted into this one's.
                for t in p.trips.iter().filter(|t| t.day == 0) {
                    let (arrive, depart) = t.times[pos];
                    let (open, close) = hours.get_or_insert((depart, arrive));
                    *open = (*open).min(depart);
                    *close = (*close).max(arrive);
                }
            }
        }
        hours
    }

    /// Whether the footpath from `from` to `to` is open to start walking at `t`.
    pub fn walk_open(&self, from: StopIdx, to: StopIdx, t: Secs) -> bool {
        if !self.has_hours.get(from as usize).copied().unwrap_or(false) {
            return true;
        }
        self.footpath_hours
            .get(&(from, to))
            .is_none_or(|&(open, close)| (open..=close).contains(&t))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn passages_parse() {
        let passages = load().unwrap();
        assert_eq!(passages[0].complexes, [611, 609]);
    }
}
