# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pstree.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pstree.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cpstree.proto\"U\n\x0cpstree_entry\x12\x0b\n\x03pid\x18\x01 \x02(\r\x12\x0c\n\x04ppid\x18\x02 \x02(\r\x12\x0c\n\x04pgid\x18\x03 \x02(\r\x12\x0b\n\x03sid\x18\x04 \x02(\r\x12\x0f\n\x07threads\x18\x05 \x03(\r'
)




_PSTREE_ENTRY = _descriptor.Descriptor(
  name='pstree_entry',
  full_name='pstree_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pid', full_name='pstree_entry.pid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ppid', full_name='pstree_entry.ppid', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pgid', full_name='pstree_entry.pgid', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sid', full_name='pstree_entry.sid', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='threads', full_name='pstree_entry.threads', index=4,
      number=5, type=13, cpp_type=3, label=3,
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
  serialized_start=16,
  serialized_end=101,
)

DESCRIPTOR.message_types_by_name['pstree_entry'] = _PSTREE_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

pstree_entry = _reflection.GeneratedProtocolMessageType('pstree_entry', (_message.Message,), {
  'DESCRIPTOR' : _PSTREE_ENTRY,
  '__module__' : 'pstree_pb2'
  # @@protoc_insertion_point(class_scope:pstree_entry)
  })
_sym_db.RegisterMessage(pstree_entry)


# @@protoc_insertion_point(module_scope)