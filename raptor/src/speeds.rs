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

impl Speeds {
    /// Seconds to walk `metres` on the level.
    pub fn walk_secs(&self, metres: f64) -> f64 {
        metres / m_per_s(self.walk_mph)
    }
}
