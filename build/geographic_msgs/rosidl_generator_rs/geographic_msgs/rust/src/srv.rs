#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to geographic_msgs__srv__GetGeographicMap_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeographicMap_Request {
    /// where to read map data
    pub url: std::string::String,

    /// Bounding box for the desired map.  If all zeros, provide all data
    /// available from the specified URL.
    pub bounds: super::msg::BoundingBox,

}



impl Default for GetGeographicMap_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetGeographicMap_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetGeographicMap_Request {
  type RmwMsg = super::srv::rmw::GetGeographicMap_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        url: msg.url.as_str().into(),
        bounds: super::msg::BoundingBox::into_rmw_message(std::borrow::Cow::Owned(msg.bounds)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        url: msg.url.as_str().into(),
        bounds: super::msg::BoundingBox::into_rmw_message(std::borrow::Cow::Borrowed(&msg.bounds)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      url: msg.url.to_string(),
      bounds: super::msg::BoundingBox::from_rmw_message(msg.bounds),
    }
  }
}


// Corresponds to geographic_msgs__srv__GetGeographicMap_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeographicMap_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: std::string::String,

    /// The requested map, its bounds may differ from the requested bounds.
    pub map: super::msg::GeographicMap,

}



impl Default for GetGeographicMap_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetGeographicMap_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetGeographicMap_Response {
  type RmwMsg = super::srv::rmw::GetGeographicMap_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status: msg.status.as_str().into(),
        map: super::msg::GeographicMap::into_rmw_message(std::borrow::Cow::Owned(msg.map)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status: msg.status.as_str().into(),
        map: super::msg::GeographicMap::into_rmw_message(std::borrow::Cow::Borrowed(&msg.map)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status: msg.status.to_string(),
      map: super::msg::GeographicMap::from_rmw_message(msg.map),
    }
  }
}


// Corresponds to geographic_msgs__srv__GetGeoPath_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeoPath_Request {
    /// starting point
    pub start: super::msg::GeoPoint,

    /// goal point
    pub goal: super::msg::GeoPoint,

}



impl Default for GetGeoPath_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetGeoPath_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetGeoPath_Request {
  type RmwMsg = super::srv::rmw::GetGeoPath_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        start: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.start)).into_owned(),
        goal: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        start: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start)).into_owned(),
        goal: super::msg::GeoPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      start: super::msg::GeoPoint::from_rmw_message(msg.start),
      goal: super::msg::GeoPoint::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to geographic_msgs__srv__GetGeoPath_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetGeoPath_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: std::string::String,

    /// path to follow
    pub plan: super::msg::GeoPath,

    /// the uuid of the RouteNetwork
    pub network: unique_identifier_msgs::msg::UUID,

    /// the uuid of the starting RouteSegment
    pub start_seg: unique_identifier_msgs::msg::UUID,

    /// the uuid of the ending RouteSegment
    pub goal_seg: unique_identifier_msgs::msg::UUID,

    /// the length of the plan
    pub distance: f64,

}



impl Default for GetGeoPath_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetGeoPath_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetGeoPath_Response {
  type RmwMsg = super::srv::rmw::GetGeoPath_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status: msg.status.as_str().into(),
        plan: super::msg::GeoPath::into_rmw_message(std::borrow::Cow::Owned(msg.plan)).into_owned(),
        network: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.network)).into_owned(),
        start_seg: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.start_seg)).into_owned(),
        goal_seg: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_seg)).into_owned(),
        distance: msg.distance,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status: msg.status.as_str().into(),
        plan: super::msg::GeoPath::into_rmw_message(std::borrow::Cow::Borrowed(&msg.plan)).into_owned(),
        network: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.network)).into_owned(),
        start_seg: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start_seg)).into_owned(),
        goal_seg: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_seg)).into_owned(),
      distance: msg.distance,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status: msg.status.to_string(),
      plan: super::msg::GeoPath::from_rmw_message(msg.plan),
      network: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.network),
      start_seg: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.start_seg),
      goal_seg: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_seg),
      distance: msg.distance,
    }
  }
}


// Corresponds to geographic_msgs__srv__GetRoutePlan_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRoutePlan_Request {
    /// route network to use
    pub network: unique_identifier_msgs::msg::UUID,

    /// starting way point
    pub start: unique_identifier_msgs::msg::UUID,

    /// goal way point
    pub goal: unique_identifier_msgs::msg::UUID,

}



impl Default for GetRoutePlan_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRoutePlan_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRoutePlan_Request {
  type RmwMsg = super::srv::rmw::GetRoutePlan_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        network: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.network)).into_owned(),
        start: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.start)).into_owned(),
        goal: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        network: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.network)).into_owned(),
        start: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start)).into_owned(),
        goal: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      network: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.network),
      start: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.start),
      goal: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to geographic_msgs__srv__GetRoutePlan_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRoutePlan_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: std::string::String,

    /// path to follow
    pub plan: super::msg::RoutePath,

}



impl Default for GetRoutePlan_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRoutePlan_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRoutePlan_Response {
  type RmwMsg = super::srv::rmw::GetRoutePlan_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status: msg.status.as_str().into(),
        plan: super::msg::RoutePath::into_rmw_message(std::borrow::Cow::Owned(msg.plan)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status: msg.status.as_str().into(),
        plan: super::msg::RoutePath::into_rmw_message(std::borrow::Cow::Borrowed(&msg.plan)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status: msg.status.to_string(),
      plan: super::msg::RoutePath::from_rmw_message(msg.plan),
    }
  }
}


// Corresponds to geographic_msgs__srv__UpdateGeographicMap_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGeographicMap_Request {
    /// Changes to geographic map.
    pub updates: super::msg::GeographicMapChanges,

}



impl Default for UpdateGeographicMap_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::UpdateGeographicMap_Request::default())
  }
}

impl rosidl_runtime_rs::Message for UpdateGeographicMap_Request {
  type RmwMsg = super::srv::rmw::UpdateGeographicMap_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        updates: super::msg::GeographicMapChanges::into_rmw_message(std::borrow::Cow::Owned(msg.updates)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        updates: super::msg::GeographicMapChanges::into_rmw_message(std::borrow::Cow::Borrowed(&msg.updates)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      updates: super::msg::GeographicMapChanges::from_rmw_message(msg.updates),
    }
  }
}


// Corresponds to geographic_msgs__srv__UpdateGeographicMap_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGeographicMap_Response {
    /// true if the call succeeded
    pub success: bool,

    /// more details
    pub status: std::string::String,

}



impl Default for UpdateGeographicMap_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::UpdateGeographicMap_Response::default())
  }
}

impl rosidl_runtime_rs::Message for UpdateGeographicMap_Response {
  type RmwMsg = super::srv::rmw::UpdateGeographicMap_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status: msg.status.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status: msg.status.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status: msg.status.to_string(),
    }
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


