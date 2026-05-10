// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_localization:srv/ToLLArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "robot_localization/srv/to_ll_array.hpp"


#ifndef ROBOT_LOCALIZATION__SRV__DETAIL__TO_LL_ARRAY__TRAITS_HPP_
#define ROBOT_LOCALIZATION__SRV__DETAIL__TO_LL_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_localization/srv/detail/to_ll_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'map_points'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace robot_localization
{

namespace srv
{

inline void to_flow_style_yaml(
  const ToLLArray_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: map_points
  {
    if (msg.map_points.size() == 0) {
      out << "map_points: []";
    } else {
      out << "map_points: [";
      size_t pending_items = msg.map_points.size();
      for (auto item : msg.map_points) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ToLLArray_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: map_points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.map_points.size() == 0) {
      out << "map_points: []\n";
    } else {
      out << "map_points:\n";
      for (auto item : msg.map_points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ToLLArray_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace robot_localization

namespace rosidl_generator_traits
{

[[deprecated("use robot_localization::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_localization::srv::ToLLArray_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_localization::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_localization::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_localization::srv::ToLLArray_Request & msg)
{
  return robot_localization::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_localization::srv::ToLLArray_Request>()
{
  return "robot_localization::srv::ToLLArray_Request";
}

template<>
inline const char * name<robot_localization::srv::ToLLArray_Request>()
{
  return "robot_localization/srv/ToLLArray_Request";
}

template<>
struct has_fixed_size<robot_localization::srv::ToLLArray_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_localization::srv::ToLLArray_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_localization::srv::ToLLArray_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'll_points'
#include "geographic_msgs/msg/detail/geo_point__traits.hpp"

namespace robot_localization
{

namespace srv
{

inline void to_flow_style_yaml(
  const ToLLArray_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: ll_points
  {
    if (msg.ll_points.size() == 0) {
      out << "ll_points: []";
    } else {
      out << "ll_points: [";
      size_t pending_items = msg.ll_points.size();
      for (auto item : msg.ll_points) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ToLLArray_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: ll_points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.ll_points.size() == 0) {
      out << "ll_points: []\n";
    } else {
      out << "ll_points:\n";
      for (auto item : msg.ll_points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ToLLArray_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace robot_localization

namespace rosidl_generator_traits
{

[[deprecated("use robot_localization::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_localization::srv::ToLLArray_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_localization::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_localization::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_localization::srv::ToLLArray_Response & msg)
{
  return robot_localization::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_localization::srv::ToLLArray_Response>()
{
  return "robot_localization::srv::ToLLArray_Response";
}

template<>
inline const char * name<robot_localization::srv::ToLLArray_Response>()
{
  return "robot_localization/srv/ToLLArray_Response";
}

template<>
struct has_fixed_size<robot_localization::srv::ToLLArray_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_localization::srv::ToLLArray_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_localization::srv::ToLLArray_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace robot_localization
{

namespace srv
{

inline void to_flow_style_yaml(
  const ToLLArray_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ToLLArray_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ToLLArray_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace robot_localization

namespace rosidl_generator_traits
{

[[deprecated("use robot_localization::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_localization::srv::ToLLArray_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_localization::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_localization::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_localization::srv::ToLLArray_Event & msg)
{
  return robot_localization::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_localization::srv::ToLLArray_Event>()
{
  return "robot_localization::srv::ToLLArray_Event";
}

template<>
inline const char * name<robot_localization::srv::ToLLArray_Event>()
{
  return "robot_localization/srv/ToLLArray_Event";
}

template<>
struct has_fixed_size<robot_localization::srv::ToLLArray_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_localization::srv::ToLLArray_Event>
  : std::integral_constant<bool, has_bounded_size<robot_localization::srv::ToLLArray_Request>::value && has_bounded_size<robot_localization::srv::ToLLArray_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<robot_localization::srv::ToLLArray_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<robot_localization::srv::ToLLArray>()
{
  return "robot_localization::srv::ToLLArray";
}

template<>
inline const char * name<robot_localization::srv::ToLLArray>()
{
  return "robot_localization/srv/ToLLArray";
}

template<>
struct has_fixed_size<robot_localization::srv::ToLLArray>
  : std::integral_constant<
    bool,
    has_fixed_size<robot_localization::srv::ToLLArray_Request>::value &&
    has_fixed_size<robot_localization::srv::ToLLArray_Response>::value
  >
{
};

template<>
struct has_bounded_size<robot_localization::srv::ToLLArray>
  : std::integral_constant<
    bool,
    has_bounded_size<robot_localization::srv::ToLLArray_Request>::value &&
    has_bounded_size<robot_localization::srv::ToLLArray_Response>::value
  >
{
};

template<>
struct is_service<robot_localization::srv::ToLLArray>
  : std::true_type
{
};

template<>
struct is_service_request<robot_localization::srv::ToLLArray_Request>
  : std::true_type
{
};

template<>
struct is_service_response<robot_localization::srv::ToLLArray_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_LOCALIZATION__SRV__DETAIL__TO_LL_ARRAY__TRAITS_HPP_
