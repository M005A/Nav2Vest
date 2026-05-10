#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__BoundingBox() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__BoundingBox__init(msg: *mut BoundingBox) -> bool;
    fn geographic_msgs__msg__BoundingBox__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<BoundingBox>, size: usize) -> bool;
    fn geographic_msgs__msg__BoundingBox__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<BoundingBox>);
    fn geographic_msgs__msg__BoundingBox__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<BoundingBox>, out_seq: *mut rosidl_runtime_rs::Sequence<BoundingBox>) -> bool;
}

// Corresponds to geographic_msgs__msg__BoundingBox
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

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

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BoundingBox {
    /// lowest and most Southwestern corner
    pub min_pt: super::super::msg::rmw::GeoPoint,

    /// highest and most Northeastern corner
    pub max_pt: super::super::msg::rmw::GeoPoint,

}



impl Default for BoundingBox {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__BoundingBox__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__BoundingBox__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for BoundingBox {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__BoundingBox__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__BoundingBox__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__BoundingBox__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for BoundingBox {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for BoundingBox where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/BoundingBox";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__BoundingBox() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeographicMapChanges() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeographicMapChanges__init(msg: *mut GeographicMapChanges) -> bool;
    fn geographic_msgs__msg__GeographicMapChanges__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeographicMapChanges>, size: usize) -> bool;
    fn geographic_msgs__msg__GeographicMapChanges__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeographicMapChanges>);
    fn geographic_msgs__msg__GeographicMapChanges__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeographicMapChanges>, out_seq: *mut rosidl_runtime_rs::Sequence<GeographicMapChanges>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeographicMapChanges
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// A list of geographic map changes.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeographicMapChanges {
    /// stamp specifies time of change
    /// frame_id (normally /map)
    pub header: std_msgs::msg::rmw::Header,

    /// new and changed points and features
    pub diffs: super::super::msg::rmw::GeographicMap,

    /// deleted map components
    pub deletes: rosidl_runtime_rs::Sequence<unique_identifier_msgs::msg::rmw::UUID>,

}



impl Default for GeographicMapChanges {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeographicMapChanges__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeographicMapChanges__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeographicMapChanges {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeographicMapChanges__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeographicMapChanges__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeographicMapChanges__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeographicMapChanges {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeographicMapChanges where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeographicMapChanges";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeographicMapChanges() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeographicMap() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeographicMap__init(msg: *mut GeographicMap) -> bool;
    fn geographic_msgs__msg__GeographicMap__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeographicMap>, size: usize) -> bool;
    fn geographic_msgs__msg__GeographicMap__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeographicMap>);
    fn geographic_msgs__msg__GeographicMap__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeographicMap>, out_seq: *mut rosidl_runtime_rs::Sequence<GeographicMap>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeographicMap
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic map for a specified region.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeographicMap {
    /// stamp specifies time
    /// frame_id (normally /map)
    pub header: std_msgs::msg::rmw::Header,

    /// identifier for this map
    pub id: unique_identifier_msgs::msg::rmw::UUID,

    /// 2D bounding box containing map
    pub bounds: super::super::msg::rmw::BoundingBox,

    /// way-points
    pub points: rosidl_runtime_rs::Sequence<super::super::msg::rmw::WayPoint>,

    /// map features
    pub features: rosidl_runtime_rs::Sequence<super::super::msg::rmw::MapFeature>,

    /// map properties
    pub props: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyValue>,

}



impl Default for GeographicMap {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeographicMap__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeographicMap__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeographicMap {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeographicMap__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeographicMap__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeographicMap__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeographicMap {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeographicMap where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeographicMap";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeographicMap() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPath() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPath__init(msg: *mut GeoPath) -> bool;
    fn geographic_msgs__msg__GeoPath__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPath>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPath__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPath>);
    fn geographic_msgs__msg__GeoPath__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPath>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPath>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPath
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPath {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub poses: rosidl_runtime_rs::Sequence<super::super::msg::rmw::GeoPoseStamped>,

}



impl Default for GeoPath {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPath__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPath__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPath {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPath__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPath__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPath__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPath {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPath where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPath";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPath() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoint() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPoint__init(msg: *mut GeoPoint) -> bool;
    fn geographic_msgs__msg__GeoPoint__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPoint>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPoint__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPoint>);
    fn geographic_msgs__msg__GeoPoint__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPoint>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPoint>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPoint
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic point, using the WGS 84 reference ellipsoid.

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPoint__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPoint__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPoint {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoint__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoint__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoint__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPoint {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPoint where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPoint";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoint() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPointStamped() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPointStamped__init(msg: *mut GeoPointStamped) -> bool;
    fn geographic_msgs__msg__GeoPointStamped__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPointStamped>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPointStamped__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPointStamped>);
    fn geographic_msgs__msg__GeoPointStamped__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPointStamped>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPointStamped>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPointStamped
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPointStamped {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: super::super::msg::rmw::GeoPoint,

}



impl Default for GeoPointStamped {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPointStamped__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPointStamped__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPointStamped {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPointStamped__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPointStamped__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPointStamped__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPointStamped {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPointStamped where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPointStamped";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPointStamped() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPose() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPose__init(msg: *mut GeoPose) -> bool;
    fn geographic_msgs__msg__GeoPose__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPose>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPose__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPose>);
    fn geographic_msgs__msg__GeoPose__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPose>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPose>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPose
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic pose, using the WGS 84 reference ellipsoid.
///
/// Orientation uses the East-North-Up (ENU) frame of reference.
/// (But, what about singularities at the poles?)

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: super::super::msg::rmw::GeoPoint,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation: geometry_msgs::msg::rmw::Quaternion,

}



impl Default for GeoPose {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPose__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPose__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPose {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPose__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPose__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPose__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPose {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPose where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPose";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPose() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoseStamped() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPoseStamped__init(msg: *mut GeoPoseStamped) -> bool;
    fn geographic_msgs__msg__GeoPoseStamped__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPoseStamped>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPoseStamped__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPoseStamped>);
    fn geographic_msgs__msg__GeoPoseStamped__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPoseStamped>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPoseStamped>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPoseStamped
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoseStamped {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: super::super::msg::rmw::GeoPose,

}



impl Default for GeoPoseStamped {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPoseStamped__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPoseStamped__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPoseStamped {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseStamped__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseStamped__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseStamped__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPoseStamped {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPoseStamped where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPoseStamped";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoseStamped() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoseWithCovariance() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPoseWithCovariance__init(msg: *mut GeoPoseWithCovariance) -> bool;
    fn geographic_msgs__msg__GeoPoseWithCovariance__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPoseWithCovariance>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPoseWithCovariance__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPoseWithCovariance>);
    fn geographic_msgs__msg__GeoPoseWithCovariance__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPoseWithCovariance>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPoseWithCovariance>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPoseWithCovariance
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic pose, using the WGS 84 reference ellipsoid.
///
/// Orientation uses the East-North-Up (ENU) frame of reference.
/// (But, what about singularities at the poles?)

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoseWithCovariance {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: super::super::msg::rmw::GeoPose,

    /// Row-major representation of the 6x6 covariance matrix
    /// The orientation parameters use a fixed-axis representation.
    /// In order, the parameters are:
    /// (Lat, Lon, Alt, rotation about E (East) axis, rotation about N (North) axis, rotation about U (Up) axis)
    #[cfg_attr(feature = "serde", serde(with = "serde_big_array::BigArray"))]
    pub covariance: [f64; 36],

}



impl Default for GeoPoseWithCovariance {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPoseWithCovariance__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPoseWithCovariance__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPoseWithCovariance {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseWithCovariance__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseWithCovariance__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseWithCovariance__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPoseWithCovariance {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPoseWithCovariance where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPoseWithCovariance";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoseWithCovariance() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoseWithCovarianceStamped() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__GeoPoseWithCovarianceStamped__init(msg: *mut GeoPoseWithCovarianceStamped) -> bool;
    fn geographic_msgs__msg__GeoPoseWithCovarianceStamped__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GeoPoseWithCovarianceStamped>, size: usize) -> bool;
    fn geographic_msgs__msg__GeoPoseWithCovarianceStamped__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GeoPoseWithCovarianceStamped>);
    fn geographic_msgs__msg__GeoPoseWithCovarianceStamped__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GeoPoseWithCovarianceStamped>, out_seq: *mut rosidl_runtime_rs::Sequence<GeoPoseWithCovarianceStamped>) -> bool;
}

// Corresponds to geographic_msgs__msg__GeoPoseWithCovarianceStamped
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GeoPoseWithCovarianceStamped {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: super::super::msg::rmw::GeoPoseWithCovariance,

}



impl Default for GeoPoseWithCovarianceStamped {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__GeoPoseWithCovarianceStamped__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__GeoPoseWithCovarianceStamped__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GeoPoseWithCovarianceStamped {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseWithCovarianceStamped__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseWithCovarianceStamped__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__GeoPoseWithCovarianceStamped__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GeoPoseWithCovarianceStamped {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GeoPoseWithCovarianceStamped where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/GeoPoseWithCovarianceStamped";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__GeoPoseWithCovarianceStamped() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__KeyValue() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__KeyValue__init(msg: *mut KeyValue) -> bool;
    fn geographic_msgs__msg__KeyValue__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeyValue>, size: usize) -> bool;
    fn geographic_msgs__msg__KeyValue__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeyValue>);
    fn geographic_msgs__msg__KeyValue__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeyValue>, out_seq: *mut rosidl_runtime_rs::Sequence<KeyValue>) -> bool;
}

// Corresponds to geographic_msgs__msg__KeyValue
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic map tag (key, value) pair
///
/// This is equivalent to diagnostic_msgs/KeyValue, repeated here to
/// avoid introducing a trivial stack dependency.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeyValue {
    /// tag label
    pub key: rosidl_runtime_rs::String,

    /// corresponding value
    pub value: rosidl_runtime_rs::String,

}



impl Default for KeyValue {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__KeyValue__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__KeyValue__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeyValue {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__KeyValue__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__KeyValue__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__KeyValue__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeyValue {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeyValue where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/KeyValue";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__KeyValue() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__MapFeature() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__MapFeature__init(msg: *mut MapFeature) -> bool;
    fn geographic_msgs__msg__MapFeature__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MapFeature>, size: usize) -> bool;
    fn geographic_msgs__msg__MapFeature__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MapFeature>);
    fn geographic_msgs__msg__MapFeature__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MapFeature>, out_seq: *mut rosidl_runtime_rs::Sequence<MapFeature>) -> bool;
}

// Corresponds to geographic_msgs__msg__MapFeature
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic map feature.
///
/// A list of WayPoint IDs for features like streets, highways, hiking
/// trails, the outlines of buildings and parking lots in sequential
/// order.
///
/// Feature lists may also contain other feature lists as members.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MapFeature {
    /// Unique feature identifier
    pub id: unique_identifier_msgs::msg::rmw::UUID,

    /// Sequence of feature components
    pub components: rosidl_runtime_rs::Sequence<unique_identifier_msgs::msg::rmw::UUID>,

    /// Key/value properties for this feature
    pub props: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyValue>,

}



impl Default for MapFeature {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__MapFeature__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__MapFeature__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MapFeature {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__MapFeature__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__MapFeature__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__MapFeature__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MapFeature {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MapFeature where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/MapFeature";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__MapFeature() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__RouteNetwork() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__RouteNetwork__init(msg: *mut RouteNetwork) -> bool;
    fn geographic_msgs__msg__RouteNetwork__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RouteNetwork>, size: usize) -> bool;
    fn geographic_msgs__msg__RouteNetwork__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RouteNetwork>);
    fn geographic_msgs__msg__RouteNetwork__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RouteNetwork>, out_seq: *mut rosidl_runtime_rs::Sequence<RouteNetwork>) -> bool;
}

// Corresponds to geographic_msgs__msg__RouteNetwork
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Geographic map route network.
///
/// A directed graph of WayPoint nodes and RouteSegment edges.  This
/// information is extracted from the more-detailed contents of a
/// GeographicMap.  A RouteNetwork contains only the way points and
/// route segments of interest for path planning.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RouteNetwork {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// This route network identifier
    pub id: unique_identifier_msgs::msg::rmw::UUID,

    /// 2D bounding box for network
    pub bounds: super::super::msg::rmw::BoundingBox,

    /// Way points in this network
    pub points: rosidl_runtime_rs::Sequence<super::super::msg::rmw::WayPoint>,

    /// Directed edges of this network
    pub segments: rosidl_runtime_rs::Sequence<super::super::msg::rmw::RouteSegment>,

    /// Network key/value properties
    pub props: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyValue>,

}



impl Default for RouteNetwork {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__RouteNetwork__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__RouteNetwork__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RouteNetwork {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RouteNetwork__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RouteNetwork__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RouteNetwork__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RouteNetwork {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RouteNetwork where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/RouteNetwork";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__RouteNetwork() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__RoutePath() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__RoutePath__init(msg: *mut RoutePath) -> bool;
    fn geographic_msgs__msg__RoutePath__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RoutePath>, size: usize) -> bool;
    fn geographic_msgs__msg__RoutePath__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RoutePath>);
    fn geographic_msgs__msg__RoutePath__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RoutePath>, out_seq: *mut rosidl_runtime_rs::Sequence<RoutePath>) -> bool;
}

// Corresponds to geographic_msgs__msg__RoutePath
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Path through a route network.
///
/// A path is a sequence of RouteSegment edges.  This information is
/// extracted from a RouteNetwork graph.  A RoutePath lists the route
/// segments needed to reach some chosen goal.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RoutePath {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Route network containing this path
    pub network: unique_identifier_msgs::msg::rmw::UUID,

    /// Sequence of RouteSegment IDs
    pub segments: rosidl_runtime_rs::Sequence<unique_identifier_msgs::msg::rmw::UUID>,

    /// Key/value properties
    pub props: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyValue>,

}



impl Default for RoutePath {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__RoutePath__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__RoutePath__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RoutePath {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RoutePath__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RoutePath__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RoutePath__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RoutePath {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RoutePath where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/RoutePath";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__RoutePath() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__RouteSegment() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__RouteSegment__init(msg: *mut RouteSegment) -> bool;
    fn geographic_msgs__msg__RouteSegment__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RouteSegment>, size: usize) -> bool;
    fn geographic_msgs__msg__RouteSegment__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RouteSegment>);
    fn geographic_msgs__msg__RouteSegment__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RouteSegment>, out_seq: *mut rosidl_runtime_rs::Sequence<RouteSegment>) -> bool;
}

// Corresponds to geographic_msgs__msg__RouteSegment
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Route network segment.
///
/// This is one directed edge of a RouteNetwork graph. It represents a
/// known path from one way point to another.  If the path is two-way,
/// there will be another RouteSegment with "start" and "end" reversed.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RouteSegment {
    /// Unique identifier for this segment
    pub id: unique_identifier_msgs::msg::rmw::UUID,

    /// beginning way point of segment
    pub start: unique_identifier_msgs::msg::rmw::UUID,

    /// ending way point of segment
    pub end: unique_identifier_msgs::msg::rmw::UUID,

    /// segment properties
    pub props: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyValue>,

}



impl Default for RouteSegment {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__RouteSegment__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__RouteSegment__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RouteSegment {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RouteSegment__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RouteSegment__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__RouteSegment__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RouteSegment {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RouteSegment where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/RouteSegment";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__RouteSegment() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__WayPoint() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__msg__WayPoint__init(msg: *mut WayPoint) -> bool;
    fn geographic_msgs__msg__WayPoint__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WayPoint>, size: usize) -> bool;
    fn geographic_msgs__msg__WayPoint__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WayPoint>);
    fn geographic_msgs__msg__WayPoint__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WayPoint>, out_seq: *mut rosidl_runtime_rs::Sequence<WayPoint>) -> bool;
}

// Corresponds to geographic_msgs__msg__WayPoint
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Way-point element for a geographic map.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WayPoint {
    /// Unique way-point identifier
    pub id: unique_identifier_msgs::msg::rmw::UUID,

    /// Position relative to WGS 84 ellipsoid
    pub position: super::super::msg::rmw::GeoPoint,

    /// Key/value properties for this point
    pub props: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeyValue>,

}



impl Default for WayPoint {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__msg__WayPoint__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__msg__WayPoint__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WayPoint {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__WayPoint__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__WayPoint__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__msg__WayPoint__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WayPoint {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WayPoint where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/msg/WayPoint";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__msg__WayPoint() }
  }
}


