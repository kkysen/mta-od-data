//! Walking speeds inside stations, set in `raptor/assign.json5`:
//! on the level, and up and down stairs and escalators along their slopes.

use serde::Deserialize;

/// Walking speeds in a station, in miles an hour,
/// on stairs and escalators along their slopes.
#[derive(Clone, Copy, Debug, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct Speeds {
    pub walk_mph: f64,
    pub stairs_up_mph: f64,
    pub stairs_down_mph: f64,
    pub escalator_up_mph: f64,
    pub escalator_down_mph: f64,
}

impl Default for Speeds {
    /// Guesses the user agreed to: walking 3 mph, as on the street,
    /// as Anita's model's 1.2 m/s also allowed for stairs;
    /// stairs slower up than down; an escalator's 1.1 mph,
    /// with some riders walking up or down it.
    fn default() -> Self {
        Self {
            walk_mph: 3.0,
            stairs_up_mph: 1.1,
            stairs_down_mph: 1.6,
            escalator_up_mph: 1.3,
            escalator_down_mph: 1.6,
        }
    }
}

pub const METRES_PER_MILE: f64 = 1609.344;

/// Miles an hour in metres a second.
pub fn m_per_s(mph: f64) -> f64 {
    mph * METRES_PER_MILE / 3600.0
}

/// A level's height where nothing measures it, in metres:
/// the median of the flights LiDAR maps measure, 3.1 to 3.4 m platform to mezzanine,
/// as the user's count at 125 St, 3.2 m.
/// Taller climbs, as by long escalators and the stairs beside them, span more levels.
pub const LEVEL_RISE_M: f64 = 3.3;
/// A flight of stairs a level, along its slope, at 30 degrees.
pub const FLIGHT_M: f64 = 2.0 * LEVEL_RISE_M;

impl Speeds {
    /// Seconds to walk `metres` on the level.
    pub fn walk_secs(&self, metres: f64) -> f64 {
        metres / m_per_s(self.walk_mph)
    }

    /// Seconds up `up` flights of stairs and down `down`, a level each.
    pub fn flights_secs(&self, up: u8, down: u8) -> f64 {
        FLIGHT_M
            * (f64::from(up) / m_per_s(self.stairs_up_mph)
                + f64::from(down) / m_per_s(self.stairs_down_mph))
    }

    /// Seconds over `levels` flights of stairs, which way unknown:
    /// halfway between up and down.
    pub fn levels_secs(&self, levels: u8) -> f64 {
        (self.flights_secs(levels, 0) + self.flights_secs(0, levels)) / 2.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn flights() {
        let s = Speeds::default();
        // 6.6 m along the slope, at 1.1 mph up and 1.6 mph down.
        assert_eq!(s.flights_secs(1, 1).round(), 23.0);
        assert_eq!(s.levels_secs(2).round(), 23.0);
    }
}
