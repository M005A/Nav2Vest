#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeographicMap_Request() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__GetGeographicMap_Request__init(msg: *mut GetGeographicMap_Request) -> bool;
    fn geographic_msgs__srv__GetGeographicMap_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetGeographicMap_Request>, size: usize) -> bool;
    fn geographic_msgs__srv__GetGeographicMap_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetGeographicMap_Request>);
    fn geographic_msgs__srv__GetGeographicMap_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetGeographicMap_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetGeographicMap_Request>) -> bool;
}

// Corresponds to geographic_msgs__srv__GetGeographicMap_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeographicMap_Request {
    /// where to read map data
    pub url: rosidl_runtime_rs::String,

    /// Bounding box for the desired map.  If all zeros, provide all data
    /// available from the specified URL.
    pub bounds: super::super::msg::rmw::BoundingBox,

}



impl Default for GetGeographicMap_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__GetGeographicMap_Request__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__GetGeographicMap_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetGeographicMap_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeographicMap_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeographicMap_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeographicMap_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetGeographicMap_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetGeographicMap_Request where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/GetGeographicMap_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeographicMap_Request() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeographicMap_Response() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__GetGeographicMap_Response__init(msg: *mut GetGeographicMap_Response) -> bool;
    fn geographic_msgs__srv__GetGeographicMap_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetGeographicMap_Response>, size: usize) -> bool;
    fn geographic_msgs__srv__GetGeographicMap_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetGeographicMap_Response>);
    fn geographic_msgs__srv__GetGeographicMap_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetGeographicMap_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetGeographicMap_Response>) -> bool;
}

// Corresponds to geographic_msgs__srv__GetGeographicMap_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeographicMap_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: rosidl_runtime_rs::String,

    /// The requested map, its bounds may differ from the requested bounds.
    pub map: super::super::msg::rmw::GeographicMap,

}



impl Default for GetGeographicMap_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__GetGeographicMap_Response__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__GetGeographicMap_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetGeographicMap_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeographicMap_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeographicMap_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeographicMap_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetGeographicMap_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetGeographicMap_Response where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/GetGeographicMap_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeographicMap_Response() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeoPath_Request() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__GetGeoPath_Request__init(msg: *mut GetGeoPath_Request) -> bool;
    fn geographic_msgs__srv__GetGeoPath_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetGeoPath_Request>, size: usize) -> bool;
    fn geographic_msgs__srv__GetGeoPath_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetGeoPath_Request>);
    fn geographic_msgs__srv__GetGeoPath_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetGeoPath_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetGeoPath_Request>) -> bool;
}

// Corresponds to geographic_msgs__srv__GetGeoPath_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeoPath_Request {
    /// starting point
    pub start: super::super::msg::rmw::GeoPoint,

    /// goal point
    pub goal: super::super::msg::rmw::GeoPoint,

}



impl Default for GetGeoPath_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__GetGeoPath_Request__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__GetGeoPath_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetGeoPath_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeoPath_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeoPath_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeoPath_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetGeoPath_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetGeoPath_Request where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/GetGeoPath_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeoPath_Request() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeoPath_Response() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__GetGeoPath_Response__init(msg: *mut GetGeoPath_Response) -> bool;
    fn geographic_msgs__srv__GetGeoPath_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetGeoPath_Response>, size: usize) -> bool;
    fn geographic_msgs__srv__GetGeoPath_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetGeoPath_Response>);
    fn geographic_msgs__srv__GetGeoPath_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetGeoPath_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetGeoPath_Response>) -> bool;
}

// Corresponds to geographic_msgs__srv__GetGeoPath_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeoPath_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: rosidl_runtime_rs::String,

    /// path to follow
    pub plan: super::super::msg::rmw::GeoPath,

    /// the uuid of the RouteNetwork
    pub network: unique_identifier_msgs::msg::rmw::UUID,

    /// the uuid of the starting RouteSegment
    pub start_seg: unique_identifier_msgs::msg::rmw::UUID,

    /// the uuid of the ending RouteSegment
    pub goal_seg: unique_identifier_msgs::msg::rmw::UUID,

    /// the length of the plan
    pub distance: f64,

}



impl Default for GetGeoPath_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__GetGeoPath_Response__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__GetGeoPath_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetGeoPath_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeoPath_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeoPath_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetGeoPath_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetGeoPath_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetGeoPath_Response where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/GetGeoPath_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetGeoPath_Response() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetRoutePlan_Request() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__GetRoutePlan_Request__init(msg: *mut GetRoutePlan_Request) -> bool;
    fn geographic_msgs__srv__GetRoutePlan_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetRoutePlan_Request>, size: usize) -> bool;
    fn geographic_msgs__srv__GetRoutePlan_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetRoutePlan_Request>);
    fn geographic_msgs__srv__GetRoutePlan_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetRoutePlan_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetRoutePlan_Request>) -> bool;
}

// Corresponds to geographic_msgs__srv__GetRoutePlan_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRoutePlan_Request {
    /// route network to use
    pub network: unique_identifier_msgs::msg::rmw::UUID,

    /// starting way point
    pub start: unique_identifier_msgs::msg::rmw::UUID,

    /// goal way point
    pub goal: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for GetRoutePlan_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__GetRoutePlan_Request__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__GetRoutePlan_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetRoutePlan_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetRoutePlan_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetRoutePlan_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetRoutePlan_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetRoutePlan_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetRoutePlan_Request where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/GetRoutePlan_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetRoutePlan_Request() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetRoutePlan_Response() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__GetRoutePlan_Response__init(msg: *mut GetRoutePlan_Response) -> bool;
    fn geographic_msgs__srv__GetRoutePlan_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetRoutePlan_Response>, size: usize) -> bool;
    fn geographic_msgs__srv__GetRoutePlan_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetRoutePlan_Response>);
    fn geographic_msgs__srv__GetRoutePlan_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetRoutePlan_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetRoutePlan_Response>) -> bool;
}

// Corresponds to geographic_msgs__srv__GetRoutePlan_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRoutePlan_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: rosidl_runtime_rs::String,

    /// path to follow
    pub plan: super::super::msg::rmw::RoutePath,

}



impl Default for GetRoutePlan_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__GetRoutePlan_Response__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__GetRoutePlan_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetRoutePlan_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetRoutePlan_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetRoutePlan_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__GetRoutePlan_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetRoutePlan_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetRoutePlan_Response where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/GetRoutePlan_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__GetRoutePlan_Response() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__UpdateGeographicMap_Request() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__UpdateGeographicMap_Request__init(msg: *mut UpdateGeographicMap_Request) -> bool;
    fn geographic_msgs__srv__UpdateGeographicMap_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<UpdateGeographicMap_Request>, size: usize) -> bool;
    fn geographic_msgs__srv__UpdateGeographicMap_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<UpdateGeographicMap_Request>);
    fn geographic_msgs__srv__UpdateGeographicMap_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<UpdateGeographicMap_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<UpdateGeographicMap_Request>) -> bool;
}

// Corresponds to geographic_msgs__srv__UpdateGeographicMap_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGeographicMap_Request {
    /// Changes to geographic map.
    pub updates: super::super::msg::rmw::GeographicMapChanges,

}



impl Default for UpdateGeographicMap_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__UpdateGeographicMap_Request__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__UpdateGeographicMap_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for UpdateGeographicMap_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__UpdateGeographicMap_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__UpdateGeographicMap_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__UpdateGeographicMap_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for UpdateGeographicMap_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for UpdateGeographicMap_Request where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/UpdateGeographicMap_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__UpdateGeographicMap_Request() }
  }
}


#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__UpdateGeographicMap_Response() -> *const std::ffi::c_void;
}

#[link(name = "geographic_msgs__rosidl_generator_c")]
extern "C" {
    fn geographic_msgs__srv__UpdateGeographicMap_Response__init(msg: *mut UpdateGeographicMap_Response) -> bool;
    fn geographic_msgs__srv__UpdateGeographicMap_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<UpdateGeographicMap_Response>, size: usize) -> bool;
    fn geographic_msgs__srv__UpdateGeographicMap_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<UpdateGeographicMap_Response>);
    fn geographic_msgs__srv__UpdateGeographicMap_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<UpdateGeographicMap_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<UpdateGeographicMap_Response>) -> bool;
}

// Corresponds to geographic_msgs__srv__UpdateGeographicMap_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGeographicMap_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: rosidl_runtime_rs::String,

}



impl Default for UpdateGeographicMap_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !geographic_msgs__srv__UpdateGeographicMap_Response__init(&mut msg as *mut _) {
        panic!("Call to geographic_msgs__srv__UpdateGeographicMap_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for UpdateGeographicMap_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__UpdateGeographicMap_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__UpdateGeographicMap_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { geographic_msgs__srv__UpdateGeographicMap_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for UpdateGeographicMap_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for UpdateGeographicMap_Response where Self: Sized {
  const TYPE_NAME: &'static str = "geographic_msgs/srv/UpdateGeographicMap_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__geographic_msgs__srv__UpdateGeographicMap_Response() }
  }
}






#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__GetGeographicMap() -> *const std::ffi::c_void;
}

// Corresponds to geographic_msgs__srv__GetGeographicMap
#[allow(missing_docs, non_camel_case_types)]
pub struct GetGeographicMap;

impl rosidl_runtime_rs::Service for GetGeographicMap {
    type Request = GetGeographicMap_Request;
    type Response = GetGeographicMap_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__GetGeographicMap() }
    }
}




#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__GetGeoPath() -> *const std::ffi::c_void;
}

// Corresponds to geographic_msgs__srv__GetGeoPath
#[allow(missing_docs, non_camel_case_types)]
pub struct GetGeoPath;

impl rosidl_runtime_rs::Service for GetGeoPath {
    type Request = GetGeoPath_Request;
    type Response = GetGeoPath_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__GetGeoPath() }
    }
}




#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__GetRoutePlan() -> *const std::ffi::c_void;
}

// Corresponds to geographic_msgs__srv__GetRoutePlan
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRoutePlan;

impl rosidl_runtime_rs::Service for GetRoutePlan {
    type Request = GetRoutePlan_Request;
    type Response = GetRoutePlan_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__GetRoutePlan() }
    }
}




#[link(name = "geographic_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__UpdateGeographicMap() -> *const std::ffi::c_void;
}

// Corresponds to geographic_msgs__srv__UpdateGeographicMap
#[allow(missing_docs, non_camel_case_types)]
pub struct UpdateGeographicMap;

impl rosidl_runtime_rs::Service for UpdateGeographicMap {
    type Request = UpdateGeographicMap_Request;
    type Response = UpdateGeographicMap_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__geographic_msgs__srv__UpdateGeographicMap() }
    }
}


