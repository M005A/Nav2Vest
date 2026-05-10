// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_localization:srv/FromLLArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "robot_localization/srv/from_ll_array.hpp"


#ifndef ROBOT_LOCALIZATION__SRV__DETAIL__FROM_LL_ARRAY__BUILDER_HPP_
#define ROBOT_LOCALIZATION__SRV__DETAIL__FROM_LL_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_localization/srv/detail/from_ll_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_localization
{

namespace srv
{

namespace builder
{

class Init_FromLLArray_Request_ll_points
{
public:
  Init_FromLLArray_Request_ll_points()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_localization::srv::FromLLArray_Request ll_points(::robot_localization::srv::FromLLArray_Request::_ll_points_type arg)
  {
    msg_.ll_points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_localization::srv::FromLLArray_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_localization::srv::FromLLArray_Request>()
{
  return robot_localization::srv::builder::Init_FromLLArray_Request_ll_points();
}

}  // namespace robot_localization


namespace robot_localization
{

namespace srv
{

namespace builder
{

class Init_FromLLArray_Response_map_points
{
public:
  Init_FromLLArray_Response_map_points()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_localization::srv::FromLLArray_Response map_points(::robot_localization::srv::FromLLArray_Response::_map_points_type arg)
  {
    msg_.map_points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_localization::srv::FromLLArray_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_localization::srv::FromLLArray_Response>()
{
  return robot_localization::srv::builder::Init_FromLLArray_Response_map_points();
}

}  // namespace robot_localization


namespace robot_localization
{

namespace srv
{

namespace builder
{

class Init_FromLLArray_Event_response
{
public:
  explicit Init_FromLLArray_Event_response(::robot_localization::srv::FromLLArray_Event & msg)
  : msg_(msg)
  {}
  ::robot_localization::srv::FromLLArray_Event response(::robot_localization::srv::FromLLArray_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_localization::srv::FromLLArray_Event msg_;
};

class Init_FromLLArray_Event_request
{
public:
  explicit Init_FromLLArray_Event_request(::robot_localization::srv::FromLLArray_Event & msg)
  : msg_(msg)
  {}
  Init_FromLLArray_Event_response request(::robot_localization::srv::FromLLArray_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_FromLLArray_Event_response(msg_);
  }

private:
  ::robot_localization::srv::FromLLArray_Event msg_;
};

class Init_FromLLArray_Event_info
{
public:
  Init_FromLLArray_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FromLLArray_Event_request info(::robot_localization::srv::FromLLArray_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_FromLLArray_Event_request(msg_);
  }

private:
  ::robot_localization::srv::FromLLArray_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_localization::srv::FromLLArray_Event>()
{
  return robot_localization::srv::builder::Init_FromLLArray_Event_info();
}

}  // namespace robot_localization

#endif  // ROBOT_LOCALIZATION__SRV__DETAIL__FROM_LL_ARRAY__BUILDER_HPP_
