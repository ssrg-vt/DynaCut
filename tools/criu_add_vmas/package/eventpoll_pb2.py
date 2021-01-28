# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eventpoll.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import fown_pb2 as fown__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='eventpoll.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x65ventpoll.proto\x1a\nfown.proto\"u\n\x13\x65ventpoll_tfd_entry\x12\n\n\x02id\x18\x01 \x02(\r\x12\x0b\n\x03tfd\x18\x02 \x02(\r\x12\x0e\n\x06\x65vents\x18\x03 \x02(\r\x12\x0c\n\x04\x64\x61ta\x18\x04 \x02(\x04\x12\x0b\n\x03\x64\x65v\x18\x05 \x01(\r\x12\r\n\x05inode\x18\x06 \x01(\x04\x12\x0b\n\x03pos\x18\x07 \x01(\x04\"o\n\x14\x65ventpoll_file_entry\x12\n\n\x02id\x18\x01 \x02(\r\x12\r\n\x05\x66lags\x18\x02 \x02(\r\x12\x19\n\x04\x66own\x18\x03 \x02(\x0b\x32\x0b.fown_entry\x12!\n\x03tfd\x18\x04 \x03(\x0b\x32\x14.eventpoll_tfd_entry'
  ,
  dependencies=[fown__pb2.DESCRIPTOR,])




_EVENTPOLL_TFD_ENTRY = _descriptor.Descriptor(
  name='eventpoll_tfd_entry',
  full_name='eventpoll_tfd_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='eventpoll_tfd_entry.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tfd', full_name='eventpoll_tfd_entry.tfd', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='events', full_name='eventpoll_tfd_entry.events', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='eventpoll_tfd_entry.data', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dev', full_name='eventpoll_tfd_entry.dev', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inode', full_name='eventpoll_tfd_entry.inode', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pos', full_name='eventpoll_tfd_entry.pos', index=6,
      number=7, type=4, cpp_type=4, label=1,
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
  serialized_start=31,
  serialized_end=148,
)


_EVENTPOLL_FILE_ENTRY = _descriptor.Descriptor(
  name='eventpoll_file_entry',
  full_name='eventpoll_file_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='eventpoll_file_entry.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='eventpoll_file_entry.flags', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fown', full_name='eventpoll_file_entry.fown', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tfd', full_name='eventpoll_file_entry.tfd', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=150,
  serialized_end=261,
)

_EVENTPOLL_FILE_ENTRY.fields_by_name['fown'].message_type = fown__pb2._FOWN_ENTRY
_EVENTPOLL_FILE_ENTRY.fields_by_name['tfd'].message_type = _EVENTPOLL_TFD_ENTRY
DESCRIPTOR.message_types_by_name['eventpoll_tfd_entry'] = _EVENTPOLL_TFD_ENTRY
DESCRIPTOR.message_types_by_name['eventpoll_file_entry'] = _EVENTPOLL_FILE_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

eventpoll_tfd_entry = _reflection.GeneratedProtocolMessageType('eventpoll_tfd_entry', (_message.Message,), {
  'DESCRIPTOR' : _EVENTPOLL_TFD_ENTRY,
  '__module__' : 'eventpoll_pb2'
  # @@protoc_insertion_point(class_scope:eventpoll_tfd_entry)
  })
_sym_db.RegisterMessage(eventpoll_tfd_entry)

eventpoll_file_entry = _reflection.GeneratedProtocolMessageType('eventpoll_file_entry', (_message.Message,), {
  'DESCRIPTOR' : _EVENTPOLL_FILE_ENTRY,
  '__module__' : 'eventpoll_pb2'
  # @@protoc_insertion_point(class_scope:eventpoll_file_entry)
  })
_sym_db.RegisterMessage(eventpoll_file_entry)


# @@protoc_insertion_point(module_scope)
