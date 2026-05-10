// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_localization:srv/FromLLArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "robot_localization/srv/from_ll_array.hpp"


#ifndef ROBOT_LOCALIZATION__SRV__DETAIL__FROM_LL_ARRAY__STRUCT_HPP_
#define ROBOT_LOCALIZATION__SRV__DETAIL__FROM_LL_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'll_points'
#include "geographic_msgs/msg/detail/geo_point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robot_localization__srv__FromLLArray_Request __attribute__((deprecated))
#else
# define DEPRECATED__robot_localization__srv__FromLLArray_Request __declspec(deprecated)
#endif

namespace robot_localization
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FromLLArray_Request_
{
  using Type = FromLLArray_Request_<ContainerAllocator>;

  explicit FromLLArray_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit FromLLArray_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _ll_points_type =
    std::vector<geographic_msgs::msg::GeoPoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geographic_msgs::msg::GeoPoint_<ContainerAllocator>>>;
  _ll_points_type ll_points;

  // setters for named parameter idiom
  Type & set__ll_points(
    const std::vector<geographic_msgs::msg::GeoPoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geographic_msgs::msg::GeoPoint_<ContainerAllocator>>> & _arg)
  {
    this->ll_points = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_localization::srv::FromLLArray_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_localization::srv::FromLLArray_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_localization__srv__FromLLArray_Request
    std::shared_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_localization__srv__FromLLArray_Request
    std::shared_ptr<robot_localization::srv::FromLLArray_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FromLLArray_Request_ & other) const
  {
    if (this->ll_points != other.ll_points) {
      return false;
    }
    return true;
  }
  bool operator!=(const FromLLArray_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FromLLArray_Request_

// alias to use template instance with default allocator
using FromLLArray_Request =
  robot_localization::srv::FromLLArray_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_localization


// Include directives for member types
// Member 'map_points'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robot_localization__srv__FromLLArray_Response __attribute__((deprecated))
#else
# define DEPRECATED__robot_localization__srv__FromLLArray_Response __declspec(deprecated)
#endif

namespace robot_localization
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FromLLArray_Response_
{
  using Type = FromLLArray_Response_<ContainerAllocator>;

  explicit FromLLArray_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit FromLLArray_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _map_points_type =
    std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>>;
  _map_points_type map_points;

  // setters for named parameter idiom
  Type & set__map_points(
    const std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>> & _arg)
  {
    this->map_points = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_localization::srv::FromLLArray_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_localization::srv::FromLLArray_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_localization__srv__FromLLArray_Response
    std::shared_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_localization__srv__FromLLArray_Response
    std::shared_ptr<robot_localization::srv::FromLLArray_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FromLLArray_Response_ & other) const
  {
    if (this->map_points != other.map_points) {
      return false;
    }
    return true;
  }
  bool operator!=(const FromLLArray_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FromLLArray_Response_

// alias to use template instance with default allocator
using FromLLArray_Response =
  robot_localization::srv::FromLLArray_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_localization


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robot_localization__srv__FromLLArray_Event __attribute__((deprecated))
#else
# define DEPRECATED__robot_localization__srv__FromLLArray_Event __declspec(deprecated)
#endif

namespace robot_localization
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FromLLArray_Event_
{
  using Type = FromLLArray_Event_<ContainerAllocator>;

  explicit FromLLArray_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit FromLLArray_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<robot_localization::srv::FromLLArray_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<robot_localization::srv::FromLLArray_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_localization::srv::FromLLArray_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_localization::srv::FromLLArray_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_localization::srv::FromLLArray_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_localization::srv::FromLLArray_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_localization__srv__FromLLArray_Event
    std::shared_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_localization__srv__FromLLArray_Event
    std::shared_ptr<robot_localization::srv::FromLLArray_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FromLLArray_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const FromLLArray_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FromLLArray_Event_

// alias to use template instance with default allocator
using FromLLArray_Event =
  robot_localization::srv::FromLLArray_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_localization

namespace robot_localization
{

namespace srv
{

struct FromLLArray
{
  using Request = robot_localization::srv::FromLLArray_Request;
  using Response = robot_localization::srv::FromLLArray_Response;
  using Event = robot_localization::srv::FromLLArray_Event;
};

}  // namespace srv

}  // namespace robot_localization

#endif  // ROBOT_LOCALIZATION__SRV__DETAIL__FROM_LL_ARRAY__STRUCT_HPP_
