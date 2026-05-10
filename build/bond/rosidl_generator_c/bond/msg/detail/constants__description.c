// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from bond:msg/Constants.idl
// generated code does not contain a copyright notice

#include "bond/msg/detail/constants__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_bond
const rosidl_type_hash_t *
bond__msg__Constants__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x34, 0x78, 0x74, 0xac, 0x7a, 0x49, 0xaf, 0x69,
      0xeb, 0x31, 0x3f, 0xc9, 0x11, 0xd7, 0x2c, 0xd5,
      0x91, 0x52, 0xa5, 0xa1, 0x57, 0xb6, 0x57, 0x7c,
      0xaf, 0xad, 0x31, 0xad, 0x43, 0xa8, 0xd6, 0x3e,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char bond__msg__Constants__TYPE_NAME[] = "bond/msg/Constants";

// Define type names, field names, and default values
static char bond__msg__Constants__FIELD_NAME__structure_needs_at_least_one_member[] = "structure_needs_at_least_one_member";

static rosidl_runtime_c__type_description__Field bond__msg__Constants__FIELDS[] = {
  {
    {bond__msg__Constants__FIELD_NAME__structure_needs_at_least_one_member, 35, 35},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
bond__msg__Constants__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {bond__msg__Constants__TYPE_NAME, 18, 18},
      {bond__msg__Constants__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 DEAD_PUBLISH_PERIOD = 0.05\n"
  "float32 DEFAULT_CONNECT_TIMEOUT = 10.0\n"
  "float32 DEFAULT_HEARTBEAT_TIMEOUT = 4.0\n"
  "float32 DEFAULT_DISCONNECT_TIMEOUT = 2.0\n"
  "float32 DEFAULT_HEARTBEAT_PERIOD = 1.0\n"
  "\n"
  "string DISABLE_HEARTBEAT_TIMEOUT_PARAM=/bond_disable_heartbeat_timeout";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
bond__msg__Constants__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {bond__msg__Constants__TYPE_NAME, 18, 18},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 266, 266},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
bond__msg__Constants__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *bond__msg__Constants__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
