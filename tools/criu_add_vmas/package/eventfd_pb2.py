# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eventfd.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import fown_pb2 as fown__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='eventfd.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\reventfd.proto\x1a\nfown.proto\"[\n\x12\x65ventfd_file_entry\x12\n\n\x02id\x18\x01 \x02(\r\x12\r\n\x05\x66lags\x18\x02 \x02(\r\x12\x19\n\x04\x66own\x18\x03 \x02(\x0b\x32\x0b.fown_entry\x12\x0f\n\x07\x63ounter\x18\x04 \x02(\x04'
  ,
  dependencies=[fown__pb2.DESCRIPTOR,])




_EVENTFD_FILE_ENTRY = _descriptor.Descriptor(
  name='eventfd_file_entry',
  full_name='eventfd_file_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='eventfd_file_entry.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='eventfd_file_entry.flags', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fown', full_name='eventfd_file_entry.fown', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='counter', full_name='eventfd_file_entry.counter', index=3,
      number=4, type=4, cpp_type=4, label=2,
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
  serialized_end=120,
)

_EVENTFD_FILE_ENTRY.fields_by_name['fown'].message_type = fown__pb2._FOWN_ENTRY
DESCRIPTOR.message_types_by_name['eventfd_file_entry'] = _EVENTFD_FILE_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

eventfd_file_entry = _reflection.GeneratedProtocolMessageType('eventfd_file_entry', (_message.Message,), {
  'DESCRIPTOR' : _EVENTFD_FILE_ENTRY,
  '__module__' : 'eventfd_pb2'
  # @@protoc_insertion_point(class_scope:eventfd_file_entry)
  })
_sym_db.RegisterMessage(eventfd_file_entry)


# @@protoc_insertion_point(module_scope)
