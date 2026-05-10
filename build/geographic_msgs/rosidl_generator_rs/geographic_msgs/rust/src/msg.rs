#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to geographic_msgs__msg__BoundingBox
/// Geographic map bounding box. 
///
/// The two GeoPoints denote diagonally opposite corners of the box.
///
/// If min_pt.latitude is NaN, the bounding box is "global", matching
/// any valid latitude, longitude and altitude.
///
/// If min_pt.altitude is NaN, the bounding box is two-dimensional and
/// matches any altitude within the specified latitude and longitude
/// range.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BoundingBox {
    /// lowest and most Southwestern corner
    pub min_pt: super::msg::GeoPoint,

    /// highest and most Northeastern corner
    pub max_pt: super::msg::GeoPoint,

}



impl Default for BoundingBox {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::BoundingBox::default())
  }
}

impl rosidl_runtime_rs::Message for BoundingBox {
  type RmwMsg = super::msg::rmw::BoundingBox;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        min_pt: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.min_pt)).into_owned(),
        max_pt: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.max_pt)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        min_pt: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.min_pt)).into_owned(),
        max_pt: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.max_pt)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      min_pt: super::msg::GeoPoint::from_rmw_message(msg.min_pt),
      max_pt: super::msg::GeoPoint::from_rmw_message(msg.max_pt),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeographicMapChanges
/// A list of geographic map changes.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeographicMapChanges {
    /// stamp specifies time of change
    /// frame_id (normally /map)
    pub header: std_msgs::msg::Header,

    /// new and changed points and features
    pub diffs: super::msg::GeographicMap,

    /// deleted map components
    pub deletes: Vec<unique_identifier_msgs::msg::UUID>,

}



impl Default for GeographicMapChanges {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeographicMapChanges::default())
  }
}

impl rosidl_runtime_rs::Message for GeographicMapChanges {
  type RmwMsg = super::msg::rmw::GeographicMapChanges;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        diffs: super::msg::GeographicMap::into_rmw_message(std::borrow::Cow::Owned(msg.diffs)).into_owned(),
        deletes: msg.deletes
          .into_iter()
          .map(|elem| unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        diffs: super::msg::GeographicMap::into_rmw_message(std::borrow::Cow::Borrowed(&msg.diffs)).into_owned(),
        deletes: msg.deletes
          .iter()
          .map(|elem| unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      diffs: super::msg::GeographicMap::from_rmw_message(msg.diffs),
      deletes: msg.deletes
          .into_iter()
          .map(unique_identifier_msgs::msg::UUID::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeographicMap
/// Geographic map for a specified region.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeographicMap {
    /// stamp specifies time
    /// frame_id (normally /map)
    pub header: std_msgs::msg::Header,

    /// identifier for this map
    pub id: unique_identifier_msgs::msg::UUID,

    /// 2D bounding box containing map
    pub bounds: super::msg::BoundingBox,

    /// way-points
    pub points: Vec<super::msg::WayPoint>,

    /// map features
    pub features: Vec<super::msg::MapFeature>,

    /// map properties
    pub props: Vec<super::msg::KeyValue>,

}



impl Default for GeographicMap {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeographicMap::default())
  }
}

impl rosidl_runtime_rs::Message for GeographicMap {
  type RmwMsg = super::msg::rmw::GeographicMap;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.id)).into_owned(),
        bounds: super::msg::BoundingBox::into_rmw_message(std::borrow::Cow::Owned(msg.bounds)).into_owned(),
        points: msg.points
          .into_iter()
          .map(|elem| super::msg::WayPoint::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        features: msg.features
          .into_iter()
          .map(|elem| super::msg::MapFeature::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        props: msg.props
          .into_iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.id)).into_owned(),
        bounds: super::msg::BoundingBox::into_rmw_message(std::borrow::Cow::Borrowed(&msg.bounds)).into_owned(),
        points: msg.points
          .iter()
          .map(|elem| super::msg::WayPoint::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        features: msg.features
          .iter()
          .map(|elem| super::msg::MapFeature::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        props: msg.props
          .iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.id),
      bounds: super::msg::BoundingBox::from_rmw_message(msg.bounds),
      points: msg.points
          .into_iter()
          .map(super::msg::WayPoint::from_rmw_message)
          .collect(),
      features: msg.features
          .into_iter()
          .map(super::msg::MapFeature::from_rmw_message)
          .collect(),
      props: msg.props
          .into_iter()
          .map(super::msg::KeyValue::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPath

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPath {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub poses: Vec<super::msg::GeoPoseStamped>,

}



impl Default for GeoPath {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPath::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPath {
  type RmwMsg = super::msg::rmw::GeoPath;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        poses: msg.poses
          .into_iter()
          .map(|elem| super::msg::GeoPoseStamped::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        poses: msg.poses
          .iter()
          .map(|elem| super::msg::GeoPoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      poses: msg.poses
          .into_iter()
          .map(super::msg::GeoPoseStamped::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPoint
/// Geographic point, using the WGS 84 reference ellipsoid.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoint {
    /// Latitude. Positive is north of equator; negative is south
    /// (-90.0 <= latitude <= +90.0).
    pub latitude: f64,

    /// Longitude. Positive is east of prime meridian; negative is
    /// west (-180.0 <= longitude <= +180.0). At the poles, latitude is -90.0 or
    /// +90.0, and longitude is irrelevant, but must be in range.
    pub longitude: f64,

    /// Altitude. Positive is above the WGS 84 ellipsoid (NaN if unspecified).
    pub altitude: f64,

}



impl Default for GeoPoint {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPoint::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPoint {
  type RmwMsg = super::msg::rmw::GeoPoint;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        latitude: msg.latitude,
        longitude: msg.longitude,
        altitude: msg.altitude,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      latitude: msg.latitude,
      longitude: msg.longitude,
      altitude: msg.altitude,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      latitude: msg.latitude,
      longitude: msg.longitude,
      altitude: msg.altitude,
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPointStamped

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPointStamped {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: super::msg::GeoPoint,

}



impl Default for GeoPointStamped {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPointStamped::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPointStamped {
  type RmwMsg = super::msg::rmw::GeoPointStamped;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        position: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.position)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        position: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.position)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      position: super::msg::GeoPoint::from_rmw_message(msg.position),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPose
/// Geographic pose, using the WGS 84 reference ellipsoid.
///
/// Orientation uses the East-North-Up (ENU) frame of reference.
/// (But, what about singularities at the poles?)

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: super::msg::GeoPoint,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation: geometry_msgs::msg::Quaternion,

}



impl Default for GeoPose {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPose::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPose {
  type RmwMsg = super::msg::rmw::GeoPose;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.position)).into_owned(),
        orientation: geometry_msgs::msg::Quaternion::into_rmw_message(std::borrow::Cow::Owned(msg.orientation)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.position)).into_owned(),
        orientation: geometry_msgs::msg::Quaternion::into_rmw_message(std::borrow::Cow::Borrowed(&msg.orientation)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      position: super::msg::GeoPoint::from_rmw_message(msg.position),
      orientation: geometry_msgs::msg::Quaternion::from_rmw_message(msg.orientation),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPoseStamped

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoseStamped {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: super::msg::GeoPose,

}



impl Default for GeoPoseStamped {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPoseStamped::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPoseStamped {
  type RmwMsg = super::msg::rmw::GeoPoseStamped;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        pose: super::msg::GeoPose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        pose: super::msg::GeoPose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      pose: super::msg::GeoPose::from_rmw_message(msg.pose),
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPoseWithCovariance
/// Geographic pose, using the WGS 84 reference ellipsoid.
///
/// Orientation uses the East-North-Up (ENU) frame of reference.
/// (But, what about singularities at the poles?)

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoseWithCovariance {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: super::msg::GeoPose,

    /// Row-major representation of the 6x6 covariance matrix
    /// The orientation parameters use a fixed-axis representation.
    /// In order, the parameters are:
    /// (Lat, Lon, Alt, rotation about E (East) axis, rotation about N (North) axis, rotation about U (Up) axis)
    #[cfg_attr(feature = "serde", serde(with = "serde_big_array::BigArray"))]
    pub covariance: [f64; 36],

}



impl Default for GeoPoseWithCovariance {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPoseWithCovariance::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPoseWithCovariance {
  type RmwMsg = super::msg::rmw::GeoPoseWithCovariance;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: super::msg::GeoPose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        covariance: msg.covariance,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: super::msg::GeoPose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        covariance: msg.covariance,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pose: super::msg::GeoPose::from_rmw_message(msg.pose),
      covariance: msg.covariance,
    }
  }
}


// Corresponds to geographic_msgs__msg__GeoPoseWithCovarianceStamped

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoseWithCovarianceStamped {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: super::msg::GeoPoseWithCovariance,

}



impl Default for GeoPoseWithCovarianceStamped {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GeoPoseWithCovarianceStamped::default())
  }
}

impl rosidl_runtime_rs::Message for GeoPoseWithCovarianceStamped {
  type RmwMsg = super::msg::rmw::GeoPoseWithCovarianceStamped;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        pose: super::msg::GeoPoseWithCovariance::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        pose: super::msg::GeoPoseWithCovariance::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      pose: super::msg::GeoPoseWithCovariance::from_rmw_message(msg.pose),
    }
  }
}


// Corresponds to geographic_msgs__msg__KeyValue
/// Geographic map tag (key, value) pair
///
/// This is equivalent to diagnostic_msgs/KeyValue, repeated here to
/// avoid introducing a trivial stack dependency.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeyValue {
    /// tag label
    pub key: std::string::String,

    /// corresponding value
    pub value: std::string::String,

}



impl Default for KeyValue {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::KeyValue::default())
  }
}

impl rosidl_runtime_rs::Message for KeyValue {
  type RmwMsg = super::msg::rmw::KeyValue;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        key: msg.key.as_str().into(),
        value: msg.value.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        key: msg.key.as_str().into(),
        value: msg.value.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      key: msg.key.to_string(),
      value: msg.value.to_string(),
    }
  }
}


// Corresponds to geographic_msgs__msg__MapFeature
/// Geographic map feature.
///
/// A list of WayPoint IDs for features like streets, highways, hiking
/// trails, the outlines of buildings and parking lots in sequential
/// order.
///
/// Feature lists may also contain other feature lists as members.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MapFeature {
    /// Unique feature identifier
    pub id: unique_identifier_msgs::msg::UUID,

    /// Sequence of feature components
    pub components: Vec<unique_identifier_msgs::msg::UUID>,

    /// Key/value properties for this feature
    pub props: Vec<super::msg::KeyValue>,

}



impl Default for MapFeature {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MapFeature::default())
  }
}

impl rosidl_runtime_rs::Message for MapFeature {
  type RmwMsg = super::msg::rmw::MapFeature;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.id)).into_owned(),
        components: msg.components
          .into_iter()
          .map(|elem| unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        props: msg.props
          .into_iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.id)).into_owned(),
        components: msg.components
          .iter()
          .map(|elem| unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        props: msg.props
          .iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.id),
      components: msg.components
          .into_iter()
          .map(unique_identifier_msgs::msg::UUID::from_rmw_message)
          .collect(),
      props: msg.props
          .into_iter()
          .map(super::msg::KeyValue::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__RouteNetwork
/// Geographic map route network.
///
/// A directed graph of WayPoint nodes and RouteSegment edges.  This
/// information is extracted from the more-detailed contents of a
/// GeographicMap.  A RouteNetwork contains only the way points and
/// route segments of interest for path planning.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RouteNetwork {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// This route network identifier
    pub id: unique_identifier_msgs::msg::UUID,

    /// 2D bounding box for network
    pub bounds: super::msg::BoundingBox,

    /// Way points in this network
    pub points: Vec<super::msg::WayPoint>,

    /// Directed edges of this network
    pub segments: Vec<super::msg::RouteSegment>,

    /// Network key/value properties
    pub props: Vec<super::msg::KeyValue>,

}



impl Default for RouteNetwork {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RouteNetwork::default())
  }
}

impl rosidl_runtime_rs::Message for RouteNetwork {
  type RmwMsg = super::msg::rmw::RouteNetwork;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.id)).into_owned(),
        bounds: super::msg::BoundingBox::into_rmw_message(std::borrow::Cow::Owned(msg.bounds)).into_owned(),
        points: msg.points
          .into_iter()
          .map(|elem| super::msg::WayPoint::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        segments: msg.segments
          .into_iter()
          .map(|elem| super::msg::RouteSegment::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        props: msg.props
          .into_iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.id)).into_owned(),
        bounds: super::msg::BoundingBox::into_rmw_message(std::borrow::Cow::Borrowed(&msg.bounds)).into_owned(),
        points: msg.points
          .iter()
          .map(|elem| super::msg::WayPoint::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        segments: msg.segments
          .iter()
          .map(|elem| super::msg::RouteSegment::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        props: msg.props
          .iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.id),
      bounds: super::msg::BoundingBox::from_rmw_message(msg.bounds),
      points: msg.points
          .into_iter()
          .map(super::msg::WayPoint::from_rmw_message)
          .collect(),
      segments: msg.segments
          .into_iter()
          .map(super::msg::RouteSegment::from_rmw_message)
          .collect(),
      props: msg.props
          .into_iter()
          .map(super::msg::KeyValue::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__RoutePath
/// Path through a route network.
///
/// A path is a sequence of RouteSegment edges.  This information is
/// extracted from a RouteNetwork graph.  A RoutePath lists the route
/// segments needed to reach some chosen goal.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RoutePath {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// Route network containing this path
    pub network: unique_identifier_msgs::msg::UUID,

    /// Sequence of RouteSegment IDs
    pub segments: Vec<unique_identifier_msgs::msg::UUID>,

    /// Key/value properties
    pub props: Vec<super::msg::KeyValue>,

}



impl Default for RoutePath {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RoutePath::default())
  }
}

impl rosidl_runtime_rs::Message for RoutePath {
  type RmwMsg = super::msg::rmw::RoutePath;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        network: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.network)).into_owned(),
        segments: msg.segments
          .into_iter()
          .map(|elem| unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        props: msg.props
          .into_iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        network: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.network)).into_owned(),
        segments: msg.segments
          .iter()
          .map(|elem| unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        props: msg.props
          .iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      network: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.network),
      segments: msg.segments
          .into_iter()
          .map(unique_identifier_msgs::msg::UUID::from_rmw_message)
          .collect(),
      props: msg.props
          .into_iter()
          .map(super::msg::KeyValue::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__RouteSegment
/// Route network segment.
///
/// This is one directed edge of a RouteNetwork graph. It represents a
/// known path from one way point to another.  If the path is two-way,
/// there will be another RouteSegment with "start" and "end" reversed.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RouteSegment {
    /// Unique identifier for this segment
    pub id: unique_identifier_msgs::msg::UUID,

    /// beginning way point of segment
    pub start: unique_identifier_msgs::msg::UUID,

    /// ending way point of segment
    pub end: unique_identifier_msgs::msg::UUID,

    /// segment properties
    pub props: Vec<super::msg::KeyValue>,

}



impl Default for RouteSegment {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RouteSegment::default())
  }
}

impl rosidl_runtime_rs::Message for RouteSegment {
  type RmwMsg = super::msg::rmw::RouteSegment;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.id)).into_owned(),
        start: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.start)).into_owned(),
        end: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.end)).into_owned(),
        props: msg.props
          .into_iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.id)).into_owned(),
        start: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start)).into_owned(),
        end: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.end)).into_owned(),
        props: msg.props
          .iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.id),
      start: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.start),
      end: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.end),
      props: msg.props
          .into_iter()
          .map(super::msg::KeyValue::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to geographic_msgs__msg__WayPoint
/// Way-point element for a geographic map.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WayPoint {
    /// Unique way-point identifier
    pub id: unique_identifier_msgs::msg::UUID,

    /// Position relative to WGS 84 ellipsoid
    pub position: super::msg::GeoPoint,

    /// Key/value properties for this point
    pub props: Vec<super::msg::KeyValue>,

}



impl Default for WayPoint {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::WayPoint::default())
  }
}

impl rosidl_runtime_rs::Message for WayPoint {
  type RmwMsg = super::msg::rmw::WayPoint;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.id)).into_owned(),
        position: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.position)).into_owned(),
        props: msg.props
          .into_iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.id)).into_owned(),
        position: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.position)).into_owned(),
        props: msg.props
          .iter()
          .map(|elem| super::msg::KeyValue::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.id),
      position: super::msg::GeoPoint::from_rmw_message(msg.position),
      props: msg.props
          .into_iter()
          .map(super::msg::KeyValue::from_rmw_message)
          .collect(),
    }
  }
}


