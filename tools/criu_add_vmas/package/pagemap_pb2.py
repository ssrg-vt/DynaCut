# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pagemap.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import opts_pb2 as opts__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pagemap.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rpagemap.proto\x1a\nopts.proto\" \n\x0cpagemap_head\x12\x10\n\x08pages_id\x18\x01 \x02(\r\"j\n\rpagemap_entry\x12\x14\n\x05vaddr\x18\x01 \x02(\x04\x42\x05\xd2?\x02\x08\x01\x12\x10\n\x08nr_pages\x18\x02 \x02(\r\x12\x11\n\tin_parent\x18\x03 \x01(\x08\x12\x1e\n\x05\x66lags\x18\x04 \x01(\rB\x0f\xd2?\x0c\x1a\npmap.flags'
  ,
  dependencies=[opts__pb2.DESCRIPTOR,])




_PAGEMAP_HEAD = _descriptor.Descriptor(
  name='pagemap_head',
  full_name='pagemap_head',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pages_id', full_name='pagemap_head.pages_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
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
  serialized_start=29,
  serialized_end=61,
)


_PAGEMAP_ENTRY = _descriptor.Descriptor(
  name='pagemap_entry',
  full_name='pagemap_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='vaddr', full_name='pagemap_entry.vaddr', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\322?\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nr_pages', full_name='pagemap_entry.nr_pages', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='in_parent', full_name='pagemap_entry.in_parent', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='pagemap_entry.flags', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\322?\014\032\npmap.flags', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=63,
  serialized_end=169,
)

DESCRIPTOR.message_types_by_name['pagemap_head'] = _PAGEMAP_HEAD
DESCRIPTOR.message_types_by_name['pagemap_entry'] = _PAGEMAP_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

pagemap_head = _reflection.GeneratedProtocolMessageType('pagemap_head', (_message.Message,), {
  'DESCRIPTOR' : _PAGEMAP_HEAD,
  '__module__' : 'pagemap_pb2'
  # @@protoc_insertion_point(class_scope:pagemap_head)
  })
_sym_db.RegisterMessage(pagemap_head)

pagemap_entry = _reflection.GeneratedProtocolMessageType('pagemap_entry', (_message.Message,), {
  'DESCRIPTOR' : _PAGEMAP_ENTRY,
  '__module__' : 'pagemap_pb2'
  # @@protoc_insertion_point(class_scope:pagemap_entry)
  })
_sym_db.RegisterMessage(pagemap_entry)


_PAGEMAP_ENTRY.fields_by_name['vaddr']._options = None
_PAGEMAP_ENTRY.fields_by_name['flags']._options = None
# @@protoc_insertion_point(module_scope)
