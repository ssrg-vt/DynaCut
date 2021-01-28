# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: inventory.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import core_pb2 as core__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='inventory.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0finventory.proto\x1a\ncore.proto\"\xe7\x01\n\x0finventory_entry\x12\x13\n\x0bimg_version\x18\x01 \x02(\r\x12\x15\n\rfdinfo_per_id\x18\x02 \x01(\x08\x12&\n\x08root_ids\x18\x03 \x01(\x0b\x32\x14.task_kobj_ids_entry\x12\x11\n\tns_per_id\x18\x04 \x01(\x08\x12\x13\n\x0broot_cg_set\x18\x05 \x01(\r\x12\x19\n\x07lsmtype\x18\x06 \x01(\x0e\x32\x08.lsmtype\x12\x13\n\x0b\x64ump_uptime\x18\x08 \x01(\x04\x12\x15\n\rpre_dump_mode\x18\t \x01(\r\x12\x11\n\ttcp_close\x18\n \x01(\x08*0\n\x07lsmtype\x12\n\n\x06NO_LSM\x10\x00\x12\x0b\n\x07SELINUX\x10\x01\x12\x0c\n\x08\x41PPARMOR\x10\x02'
  ,
  dependencies=[core__pb2.DESCRIPTOR,])

_LSMTYPE = _descriptor.EnumDescriptor(
  name='lsmtype',
  full_name='lsmtype',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_LSM', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SELINUX', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='APPARMOR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=265,
  serialized_end=313,
)
_sym_db.RegisterEnumDescriptor(_LSMTYPE)

lsmtype = enum_type_wrapper.EnumTypeWrapper(_LSMTYPE)
NO_LSM = 0
SELINUX = 1
APPARMOR = 2



_INVENTORY_ENTRY = _descriptor.Descriptor(
  name='inventory_entry',
  full_name='inventory_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='img_version', full_name='inventory_entry.img_version', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fdinfo_per_id', full_name='inventory_entry.fdinfo_per_id', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='root_ids', full_name='inventory_entry.root_ids', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ns_per_id', full_name='inventory_entry.ns_per_id', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='root_cg_set', full_name='inventory_entry.root_cg_set', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lsmtype', full_name='inventory_entry.lsmtype', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dump_uptime', full_name='inventory_entry.dump_uptime', index=6,
      number=8, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pre_dump_mode', full_name='inventory_entry.pre_dump_mode', index=7,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tcp_close', full_name='inventory_entry.tcp_close', index=8,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=263,
)

_INVENTORY_ENTRY.fields_by_name['root_ids'].message_type = core__pb2._TASK_KOBJ_IDS_ENTRY
_INVENTORY_ENTRY.fields_by_name['lsmtype'].enum_type = _LSMTYPE
DESCRIPTOR.message_types_by_name['inventory_entry'] = _INVENTORY_ENTRY
DESCRIPTOR.enum_types_by_name['lsmtype'] = _LSMTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

inventory_entry = _reflection.GeneratedProtocolMessageType('inventory_entry', (_message.Message,), {
  'DESCRIPTOR' : _INVENTORY_ENTRY,
  '__module__' : 'inventory_pb2'
  # @@protoc_insertion_point(class_scope:inventory_entry)
  })
_sym_db.RegisterMessage(inventory_entry)


# @@protoc_insertion_point(module_scope)
