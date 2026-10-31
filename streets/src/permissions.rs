//! Which ways are streets, and which way along them one may walk,
//! as R5 7.5.1 decides: `StreetLayer.isWayRoutable`, `StreetLayer.isImpassable`,
//! `TypeOfEdgeLabeler`'s linkable edges, and
//! `USTraversalPermissionLabeler`'s pedestrian permissions.

use crate::osm::Tags;

/// Whether R5 makes edges of a way: streets and paths, and platforms.
pub fn routable(tags: &Tags) -> bool {
    let highway = tags.get("highway");
    let street = highway.is_some_and(|h| !matches!(h, "services" | "rest_area" | "raceway"));
    let platform = tags.is("public_transport", "platform")
        || (tags.is("railway", "platform") && !tags.is("usage", "tourism"));
    let exists = |value: Option<&str>| {
        !matches!(
            value,
            Some("construction" | "abandoned" | "removed" | "proposed" | "propossed" | "unbuilt")
        ) && !tags.has("construction")
            && !tags.has("proposed")
    };
    (street || platform) && exists(highway) && tags.get("cycleway").is_none_or(|c| exists(Some(c)))
}

/// Whether a point (a stop, an origin, or a destination) may be linked to a way:
/// not a tunnel, covered, or a motorway.
pub fn linkable(tags: &Tags) -> bool {
    !(tags.is("tunnel", "yes") || tags.is("covered", "yes") || tags.is("highway", "motorway"))
}

/// Whether a node splits a way into edges where it can't be passed.
pub fn impassable(tags: &Tags) -> bool {
    if tags.is_empty() {
        return false;
    }
    if tags.is("entrance", "emergency") {
        return true;
    }
    let null_or_no = |key| tags.get(key).is_none_or(|v| v == "no");
    tags.is("access", "no") && null_or_no("foot") && null_or_no("bicycle")
}

/// Whether one may walk a way from its first node to its last, and back.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Walk {
    pub forward: bool,
    pub backward: bool,
}

/// A permission, from a tag's value.
#[derive(Clone, Copy, Debug, PartialEq)]
enum Label {
    Yes,
    No,
    /// `destination`, `private`, and the like: R5 doesn't route through these on foot.
    NoThruTraffic,
    Limited,
    /// Unset, or a value R5 doesn't know: the parent's label applies.
    Unknown,
}

impl Label {
    fn from_tag(value: &str) -> Self {
        // Some are like `designated;yes`.
        let value = value
            .split(';')
            .next()
            .unwrap_or_default()
            .trim()
            .to_lowercase();
        match value.as_str() {
            "yes" | "1" | "true" | "official" | "unknown" | "public" | "permissive"
            | "designated" | "lane" | "track" | "shared_lane" | "share_busway" | "crossing" => {
                Self::Yes
            }
            "no" | "0" | "false" | "license" | "restricted" | "prohibited" | "emergency"
            | "use_sidepath" | "dismount" => Self::No,
            "destination" | "customers" | "delivery" | "forestry" | "agricultural"
            | "residents" | "resident" | "customer" | "private" => Self::NoThruTraffic,
            "limited" => Self::Limited,
            _ => Self::Unknown,
        }
    }
}

/// `(access, foot)` before a way's own tags, by its `highway` (or platform) tag:
/// R5's defaults, with the US's foot on cycleways and bridleways.
fn defaults(tags: &Tags) -> (Label, Label) {
    use Label::{No, Unknown, Yes};
    let key = match tags.get("highway") {
        Some(h) => h.trim().to_lowercase(),
        None if tags.is("railway", "platform") || tags.is("public_transport", "platform") => {
            "platform".to_owned()
        }
        None => "road".to_owned(),
    };
    match key.as_str() {
        "motorway" => (Yes, No),
        "pedestrian" | "path" | "bridleway" | "cycleway" | "footway" | "steps" | "platform"
        | "corridor" => (No, Yes),
        // `trunk` through `track`, and any other `highway`, as `road`.
        _ => (Yes, Unknown),
    }
}

/// Which way along a way one may walk.
pub fn walk(tags: &Tags) -> Walk {
    let (mut access, mut foot) = defaults(tags);
    let apply = |label: &mut Label, value: Label| {
        if value != Label::Unknown {
            *label = value;
        }
    };
    if let Some(v) = tags.get("access") {
        apply(&mut access, Label::from_tag(v));
    }
    if let Some(v) = tags.get("foot") {
        apply(&mut foot, Label::from_tag(v));
    }
    if let Some(v) = tags.get("sidewalk")
        && matches!(v.to_lowercase().as_str(), "both" | "left" | "right")
    {
        apply(&mut foot, Label::Yes);
    }
    let allowed = if foot == Label::Unknown { access } else { foot } == Label::Yes;
    // Walkers ignore `oneway`, but not `oneway:foot`.
    let (forward, backward) = match tags.get("oneway:foot").map(|v| v.trim().to_lowercase()) {
        Some(v) if matches!(v.as_str(), "yes" | "true" | "1") => (true, false),
        Some(v) if matches!(v.as_str(), "-1" | "reverse") => (false, true),
        _ => (true, true),
    };
    Walk {
        forward: allowed && forward,
        backward: allowed && backward,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tags(pairs: &[(&str, &str)]) -> Tags {
        Tags::from_iter(pairs.iter().map(|&(k, v)| (k.to_owned(), v.to_owned())))
    }

    fn walkable(pairs: &[(&str, &str)]) -> bool {
        walk(&tags(pairs))
            == Walk {
                forward: true,
                backward: true,
            }
    }

    #[test]
    fn streets_but_not_motorways() {
        assert!(walkable(&[("highway", "residential")]));
        assert!(walkable(&[("highway", "footway")]));
        assert!(walkable(&[("highway", "cycleway")]));
        assert!(walkable(&[("highway", "motorway_link")]));
        assert!(!walkable(&[("highway", "motorway")]));
        assert!(walkable(&[("railway", "platform")]));
    }

    #[test]
    fn foot_outranks_access_and_sidewalks_outrank_foot() {
        assert!(!walkable(&[("highway", "residential"), ("access", "no")]));
        assert!(walkable(&[
            ("highway", "residential"),
            ("access", "no"),
            ("foot", "yes")
        ]));
        assert!(!walkable(&[("highway", "trunk"), ("foot", "no")]));
        assert!(walkable(&[
            ("highway", "trunk"),
            ("foot", "no"),
            ("sidewalk", "both")
        ]));
        assert!(!walkable(&[("highway", "service"), ("access", "private")]));
        assert!(walkable(&[
            ("highway", "footway"),
            ("foot", "designated;yes")
        ]));
    }

    #[test]
    fn only_oneway_foot_is_one_way_on_foot() {
        let w = |pairs| walk(&tags(pairs));
        assert_eq!(
            w(&[("highway", "primary"), ("oneway", "yes")]),
            Walk {
                forward: true,
                backward: true
            }
        );
        assert_eq!(
            w(&[("highway", "footway"), ("oneway:foot", "yes")]),
            Walk {
                forward: true,
                backward: false
            }
        );
        assert_eq!(
            w(&[("highway", "footway"), ("oneway:foot", "-1")]),
            Walk {
                forward: false,
                backward: true
            }
        );
    }

    #[test]
    fn routable_ways() {
        assert!(routable(&tags(&[("highway", "residential")])));
        assert!(!routable(&tags(&[("highway", "construction")])));
        assert!(!routable(&tags(&[
            ("highway", "footway"),
            ("proposed", "footway")
        ])));
        assert!(!routable(&tags(&[("highway", "rest_area")])));
        assert!(routable(&tags(&[("public_transport", "platform")])));
        assert!(!routable(&tags(&[
            ("railway", "platform"),
            ("usage", "tourism")
        ])));
        assert!(!routable(&tags(&[("building", "yes")])));
    }

    #[test]
    fn linking_and_passing() {
        assert!(!linkable(&tags(&[
            ("highway", "footway"),
            ("tunnel", "yes")
        ])));
        assert!(linkable(&tags(&[
            ("highway", "footway"),
            ("bridge", "yes")
        ])));
        assert!(impassable(&tags(&[("access", "no")])));
        assert!(!impassable(&tags(&[("access", "no"), ("foot", "yes")])));
        assert!(!impassable(&tags(&[("barrier", "gate")])));
    }
}
