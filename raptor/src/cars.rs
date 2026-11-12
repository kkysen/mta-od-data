//! Where on the train riders changing trains are, set in `raptor/assign.json5`,
//! so how far along the platform they walk to the stairs or escalator,
//! as each walk's paths leave from their own spots along it
//! (`raptor/lidar_walks.csv` and `raptor/osm_walks.csv`'s `along_m`).
//!
//! Riders are a mix: some plan their car, so they're in a bell curve
//! around the foot of the quickest path's stairs or escalator;
//! the rest are anywhere along the train, which fills the platform.
//! From each spot, a rider takes whichever path is quickest from there,
//! and a transfer takes the average over all of them,
//! with no need to track which car each rider is in.

use serde::Deserialize;

use crate::speeds::Speeds;

#[derive(Clone, Copy, Debug, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct Cars {
    /// The share of riders who plan their car.
    pub plan_share: f64,
    /// How far those riders spread around the path's foot, a standard deviation,
    /// in metres.
    pub plan_sigma_m: f64,
}

impl Default for Cars {
    /// Placeholders: half plan their car, within about a car, 60 ft, of the stairs.
    fn default() -> Self {
        Self {
            plan_share: 0.5,
            plan_sigma_m: 18.0,
        }
    }
}

/// One way off a platform: its foot `along` metres along it,
/// and `secs` from there on.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Path {
    pub along: f64,
    pub secs: f64,
}

/// Riders' spots along a train, for the average.
const STEP_M: f64 = 1.0;

impl Cars {
    /// The average time off a platform `platform_m` long by the quickest of `paths`
    /// from each rider's spot along it, walking there at `speeds`.
    pub fn expected_secs(&self, platform_m: f64, paths: &[Path], speeds: &Speeds) -> f64 {
        let Some(best) = paths.iter().min_by(|a, b| a.secs.total_cmp(&b.secs)) else {
            return f64::INFINITY;
        };
        let spots = (platform_m / STEP_M).ceil().max(1.0) as usize;
        let (mut planned, mut weight, mut anywhere) = (0.0, 0.0, 0.0);
        for i in 0..spots {
            let x = (i as f64 + 0.5) * platform_m / spots as f64;
            let secs = paths
                .iter()
                .map(|p| speeds.walk_secs((x - p.along).abs()) + p.secs)
                .fold(f64::INFINITY, f64::min);
            let w = (-0.5 * ((x - best.along) / self.plan_sigma_m).powi(2)).exp();
            planned += w * secs;
            weight += w;
            anywhere += secs;
        }
        self.plan_share * planned / weight + (1.0 - self.plan_share) * anywhere / spots as f64
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn spread_riders_walk_to_the_stairs() {
        let speeds = Speeds::default();
        let cars = Cars {
            plan_share: 0.0,
            plan_sigma_m: 18.0,
        };
        // Stairs at one end of a 100 m platform: 50 m on average, 37s at 3 mph.
        let end = [Path {
            along: 0.0,
            secs: 10.0,
        }];
        assert_eq!(cars.expected_secs(100.0, &end, &speeds).round(), 47.0);
        // Stairs at each end, the nearer from each spot: 25 m on average.
        let ends = [
            end[0],
            Path {
                along: 100.0,
                secs: 10.0,
            },
        ];
        assert_eq!(cars.expected_secs(100.0, &ends, &speeds).round(), 29.0);
    }

    #[test]
    fn planners_stand_by_the_quickest_path() {
        let speeds = Speeds::default();
        let cars = Cars {
            plan_share: 1.0,
            plan_sigma_m: 0.1,
        };
        let paths = [
            Path {
                along: 0.0,
                secs: 30.0,
            },
            Path {
                along: 60.0,
                secs: 10.0,
            },
        ];
        assert_eq!(cars.expected_secs(100.0, &paths, &speeds).round(), 10.0);
    }
}
