// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from geographic_msgs:msg/GeoPath.idl
// generated code does not contain a copyright notice
#include "geographic_msgs/msg/detail/geo_path__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "geographic_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "geographic_msgs/msg/detail/geo_path__struct.h"
#include "geographic_msgs/msg/detail/geo_path__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "geographic_msgs/msg/detail/geo_pose_stamped__functions.h"  // poses
#include "std_msgs/msg/detail/header__functions.h"  // header

// forward declare type support functions

bool cdr_serialize_geographic_msgs__msg__GeoPoseStamped(
  const geographic_msgs__msg__GeoPoseStamped * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_geographic_msgs__msg__GeoPoseStamped(
  eprosima::fastcdr::Cdr & cdr,
  geographic_msgs__msg__GeoPoseStamped * ros_message);

size_t get_serialized_size_geographic_msgs__msg__GeoPoseStamped(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_geographic_msgs__msg__GeoPoseStamped(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_geographic_msgs__msg__GeoPoseStamped(
  const geographic_msgs__msg__GeoPoseStamped * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_geographic_msgs__msg__GeoPoseStamped(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_geographic_msgs__msg__GeoPoseStamped(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geographic_msgs, msg, GeoPoseStamped)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
bool cdr_serialize_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
bool cdr_deserialize_std_msgs__msg__Header(
  eprosima::fastcdr::Cdr & cdr,
  std_msgs__msg__Header * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
size_t get_serialized_size_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
size_t max_serialized_size_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
bool cdr_serialize_key_std_msgs__msg__Header(
  const std_msgs__msg__Header * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
size_t get_serialized_size_key_std_msgs__msg__Header(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
size_t max_serialized_size_key_std_msgs__msg__Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_geographic_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, std_msgs, msg, Header)();


using _GeoPath__ros_msg_type = geographic_msgs__msg__GeoPath;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
bool cdr_serialize_geographic_msgs__msg__GeoPath(
  const geographic_msgs__msg__GeoPath * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: header
  {
    cdr_serialize_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  // Field name: poses
  {
    size_t size = ros_message->poses.size;
    auto array_ptr = ros_message->poses.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_geographic_msgs__msg__GeoPoseStamped(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
bool cdr_deserialize_geographic_msgs__msg__GeoPath(
  eprosima::fastcdr::Cdr & cdr,
  geographic_msgs__msg__GeoPath * ros_message)
{
  // Field name: header
  {
    cdr_deserialize_std_msgs__msg__Header(cdr, &ros_message->header);
  }

  // Field name: poses
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->poses.data) {
      geographic_msgs__msg__GeoPoseStamped__Sequence__fini(&ros_message->poses);
    }
    if (!geographic_msgs__msg__GeoPoseStamped__Sequence__init(&ros_message->poses, size)) {
      fprintf(stderr, "failed to create array for field 'poses'");
      return false;
    }
    auto array_ptr = ros_message->poses.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_geographic_msgs__msg__GeoPoseStamped(cdr, &array_ptr[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
size_t get_serialized_size_geographic_msgs__msg__GeoPath(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GeoPath__ros_msg_type * ros_message = static_cast<const _GeoPath__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: header
  current_alignment += get_serialized_size_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  // Field name: poses
  {
    size_t array_size = ros_message->poses.size;
    auto array_ptr = ros_message->poses.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_geographic_msgs__msg__GeoPoseStamped(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
size_t max_serialized_size_geographic_msgs__msg__GeoPath(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: poses
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geographic_msgs__msg__GeoPoseStamped(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = geographic_msgs__msg__GeoPath;
    is_plain =
      (
      offsetof(DataType, poses) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
bool cdr_serialize_key_geographic_msgs__msg__GeoPath(
  const geographic_msgs__msg__GeoPath * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: header
  {
    cdr_serialize_key_std_msgs__msg__Header(
      &ros_message->header, cdr);
  }

  // Field name: poses
  {
    size_t size = ros_message->poses.size;
    auto array_ptr = ros_message->poses.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_key_geographic_msgs__msg__GeoPoseStamped(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
size_t get_serialized_size_key_geographic_msgs__msg__GeoPath(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GeoPath__ros_msg_type * ros_message = static_cast<const _GeoPath__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: header
  current_alignment += get_serialized_size_key_std_msgs__msg__Header(
    &(ros_message->header), current_alignment);

  // Field name: poses
  {
    size_t array_size = ros_message->poses.size;
    auto array_ptr = ros_message->poses.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_key_geographic_msgs__msg__GeoPoseStamped(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_geographic_msgs
size_t max_serialized_size_key_geographic_msgs__msg__GeoPath(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_std_msgs__msg__Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: poses
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_geographic_msgs__msg__GeoPoseStamped(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = geographic_msgs__msg__GeoPath;
    is_plain =
      (
      offsetof(DataType, poses) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _GeoPath__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const geographic_msgs__msg__GeoPath * ros_message = static_cast<const geographic_msgs__msg__GeoPath *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_geographic_msgs__msg__GeoPath(ros_message, cdr);
}

static bool _GeoPath__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  geographic_msgs__msg__GeoPath * ros_message = static_cast<geographic_msgs__msg__GeoPath *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_geographic_msgs__msg__GeoPath(cdr, ros_message);
}

static uint32_t _GeoPath__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_geographic_msgs__msg__GeoPath(
      untyped_ros_message, 0));
}

static size_t _GeoPath__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_geographic_msgs__msg__GeoPath(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_GeoPath = {
  "geographic_msgs::msg",
  "GeoPath",
  _GeoPath__cdr_serialize,
  _GeoPath__cdr_deserialize,
  _GeoPath__get_serialized_size,
  _GeoPath__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _GeoPath__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_GeoPath,
  get_message_typesupport_handle_function,
  &geographic_msgs__msg__GeoPath__get_type_hash,
  &geographic_msgs__msg__GeoPath__get_type_description,
  &geographic_msgs__msg__GeoPath__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geographic_msgs, msg, GeoPath)() {
  return &_GeoPath__type_support;
}

#if defined(__cplusplus)
}
#endif
