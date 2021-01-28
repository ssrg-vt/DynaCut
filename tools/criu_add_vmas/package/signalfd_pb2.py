# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: signalfd.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import opts_pb2 as opts__pb2
import fown_pb2 as fown__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='signalfd.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0esignalfd.proto\x1a\nopts.proto\x1a\nfown.proto\"e\n\x0esignalfd_entry\x12\n\n\x02id\x18\x01 \x02(\r\x12\x14\n\x05\x66lags\x18\x02 \x02(\rB\x05\xd2?\x02\x08\x01\x12\x19\n\x04\x66own\x18\x03 \x02(\x0b\x32\x0b.fown_entry\x12\x16\n\x07sigmask\x18\x04 \x02(\x04\x42\x05\xd2?\x02\x08\x01'
  ,
  dependencies=[opts__pb2.DESCRIPTOR,fown__pb2.DESCRIPTOR,])




_SIGNALFD_ENTRY = _descriptor.Descriptor(
  name='signalfd_entry',
  full_name='signalfd_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='signalfd_entry.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='signalfd_entry.flags', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\322?\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fown', full_name='signalfd_entry.fown', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sigmask', full_name='signalfd_entry.sigmask', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\322?\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=42,
  serialized_end=143,
)

_SIGNALFD_ENTRY.fields_by_name['fown'].message_type = fown__pb2._FOWN_ENTRY
DESCRIPTOR.message_types_by_name['signalfd_entry'] = _SIGNALFD_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

signalfd_entry = _reflection.GeneratedProtocolMessageType('signalfd_entry', (_message.Message,), {
  'DESCRIPTOR' : _SIGNALFD_ENTRY,
  '__module__' : 'signalfd_pb2'
  # @@protoc_insertion_point(class_scope:signalfd_entry)
  })
_sym_db.RegisterMessage(signalfd_entry)


_SIGNALFD_ENTRY.fields_by_name['flags']._options = None
_SIGNALFD_ENTRY.fields_by_name['sigmask']._options = None
# @@protoc_insertion_point(module_scope)
