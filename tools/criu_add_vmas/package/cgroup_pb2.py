# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cgroup.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cgroup.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x63group.proto\"6\n\x0c\x63group_perms\x12\x0c\n\x04mode\x18\x01 \x02(\r\x12\x0b\n\x03uid\x18\x02 \x02(\r\x12\x0b\n\x03gid\x18\x03 \x02(\r\"N\n\x11\x63group_prop_entry\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\t\x12\x1c\n\x05perms\x18\x03 \x01(\x0b\x32\r.cgroup_perms\"\x93\x01\n\x10\x63group_dir_entry\x12\x10\n\x08\x64ir_name\x18\x01 \x02(\t\x12#\n\x08\x63hildren\x18\x02 \x03(\x0b\x32\x11.cgroup_dir_entry\x12&\n\nproperties\x18\x03 \x03(\x0b\x32\x12.cgroup_prop_entry\x12 \n\tdir_perms\x18\x04 \x01(\x0b\x32\r.cgroup_perms\"F\n\x13\x63g_controller_entry\x12\x0e\n\x06\x63names\x18\x01 \x03(\t\x12\x1f\n\x04\x64irs\x18\x02 \x03(\x0b\x32\x11.cgroup_dir_entry\"B\n\x0f\x63g_member_entry\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04path\x18\x02 \x02(\t\x12\x13\n\x0b\x63gns_prefix\x18\x03 \x01(\r\":\n\x0c\x63g_set_entry\x12\n\n\x02id\x18\x01 \x02(\r\x12\x1e\n\x04\x63tls\x18\x02 \x03(\x0b\x32\x10.cg_member_entry\"V\n\x0c\x63group_entry\x12\x1b\n\x04sets\x18\x01 \x03(\x0b\x32\r.cg_set_entry\x12)\n\x0b\x63ontrollers\x18\x02 \x03(\x0b\x32\x14.cg_controller_entry'
)




_CGROUP_PERMS = _descriptor.Descriptor(
  name='cgroup_perms',
  full_name='cgroup_perms',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mode', full_name='cgroup_perms.mode', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uid', full_name='cgroup_perms.uid', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gid', full_name='cgroup_perms.gid', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=16,
  serialized_end=70,
)


_CGROUP_PROP_ENTRY = _descriptor.Descriptor(
  name='cgroup_prop_entry',
  full_name='cgroup_prop_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='cgroup_prop_entry.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='cgroup_prop_entry.value', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='perms', full_name='cgroup_prop_entry.perms', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=72,
  serialized_end=150,
)


_CGROUP_DIR_ENTRY = _descriptor.Descriptor(
  name='cgroup_dir_entry',
  full_name='cgroup_dir_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dir_name', full_name='cgroup_dir_entry.dir_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='children', full_name='cgroup_dir_entry.children', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='properties', full_name='cgroup_dir_entry.properties', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dir_perms', full_name='cgroup_dir_entry.dir_perms', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=153,
  serialized_end=300,
)


_CG_CONTROLLER_ENTRY = _descriptor.Descriptor(
  name='cg_controller_entry',
  full_name='cg_controller_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cnames', full_name='cg_controller_entry.cnames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dirs', full_name='cg_controller_entry.dirs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=302,
  serialized_end=372,
)


_CG_MEMBER_ENTRY = _descriptor.Descriptor(
  name='cg_member_entry',
  full_name='cg_member_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='cg_member_entry.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path', full_name='cg_member_entry.path', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cgns_prefix', full_name='cg_member_entry.cgns_prefix', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=374,
  serialized_end=440,
)


_CG_SET_ENTRY = _descriptor.Descriptor(
  name='cg_set_entry',
  full_name='cg_set_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='cg_set_entry.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ctls', full_name='cg_set_entry.ctls', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=442,
  serialized_end=500,
)


_CGROUP_ENTRY = _descriptor.Descriptor(
  name='cgroup_entry',
  full_name='cgroup_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sets', full_name='cgroup_entry.sets', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='controllers', full_name='cgroup_entry.controllers', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=502,
  serialized_end=588,
)

_CGROUP_PROP_ENTRY.fields_by_name['perms'].message_type = _CGROUP_PERMS
_CGROUP_DIR_ENTRY.fields_by_name['children'].message_type = _CGROUP_DIR_ENTRY
_CGROUP_DIR_ENTRY.fields_by_name['properties'].message_type = _CGROUP_PROP_ENTRY
_CGROUP_DIR_ENTRY.fields_by_name['dir_perms'].message_type = _CGROUP_PERMS
_CG_CONTROLLER_ENTRY.fields_by_name['dirs'].message_type = _CGROUP_DIR_ENTRY
_CG_SET_ENTRY.fields_by_name['ctls'].message_type = _CG_MEMBER_ENTRY
_CGROUP_ENTRY.fields_by_name['sets'].message_type = _CG_SET_ENTRY
_CGROUP_ENTRY.fields_by_name['controllers'].message_type = _CG_CONTROLLER_ENTRY
DESCRIPTOR.message_types_by_name['cgroup_perms'] = _CGROUP_PERMS
DESCRIPTOR.message_types_by_name['cgroup_prop_entry'] = _CGROUP_PROP_ENTRY
DESCRIPTOR.message_types_by_name['cgroup_dir_entry'] = _CGROUP_DIR_ENTRY
DESCRIPTOR.message_types_by_name['cg_controller_entry'] = _CG_CONTROLLER_ENTRY
DESCRIPTOR.message_types_by_name['cg_member_entry'] = _CG_MEMBER_ENTRY
DESCRIPTOR.message_types_by_name['cg_set_entry'] = _CG_SET_ENTRY
DESCRIPTOR.message_types_by_name['cgroup_entry'] = _CGROUP_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

cgroup_perms = _reflection.GeneratedProtocolMessageType('cgroup_perms', (_message.Message,), {
  'DESCRIPTOR' : _CGROUP_PERMS,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cgroup_perms)
  })
_sym_db.RegisterMessage(cgroup_perms)

cgroup_prop_entry = _reflection.GeneratedProtocolMessageType('cgroup_prop_entry', (_message.Message,), {
  'DESCRIPTOR' : _CGROUP_PROP_ENTRY,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cgroup_prop_entry)
  })
_sym_db.RegisterMessage(cgroup_prop_entry)

cgroup_dir_entry = _reflection.GeneratedProtocolMessageType('cgroup_dir_entry', (_message.Message,), {
  'DESCRIPTOR' : _CGROUP_DIR_ENTRY,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cgroup_dir_entry)
  })
_sym_db.RegisterMessage(cgroup_dir_entry)

cg_controller_entry = _reflection.GeneratedProtocolMessageType('cg_controller_entry', (_message.Message,), {
  'DESCRIPTOR' : _CG_CONTROLLER_ENTRY,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cg_controller_entry)
  })
_sym_db.RegisterMessage(cg_controller_entry)

cg_member_entry = _reflection.GeneratedProtocolMessageType('cg_member_entry', (_message.Message,), {
  'DESCRIPTOR' : _CG_MEMBER_ENTRY,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cg_member_entry)
  })
_sym_db.RegisterMessage(cg_member_entry)

cg_set_entry = _reflection.GeneratedProtocolMessageType('cg_set_entry', (_message.Message,), {
  'DESCRIPTOR' : _CG_SET_ENTRY,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cg_set_entry)
  })
_sym_db.RegisterMessage(cg_set_entry)

cgroup_entry = _reflection.GeneratedProtocolMessageType('cgroup_entry', (_message.Message,), {
  'DESCRIPTOR' : _CGROUP_ENTRY,
  '__module__' : 'cgroup_pb2'
  # @@protoc_insertion_point(class_scope:cgroup_entry)
  })
_sym_db.RegisterMessage(cgroup_entry)


# @@protoc_insertion_point(module_scope)