# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file-lock.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='file-lock.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x66ile-lock.proto\"b\n\x0f\x66ile_lock_entry\x12\x0c\n\x04\x66lag\x18\x01 \x02(\r\x12\x0c\n\x04type\x18\x02 \x02(\r\x12\x0b\n\x03pid\x18\x03 \x02(\x05\x12\n\n\x02\x66\x64\x18\x04 \x02(\x05\x12\r\n\x05start\x18\x05 \x02(\x03\x12\x0b\n\x03len\x18\x06 \x02(\x03'
)




_FILE_LOCK_ENTRY = _descriptor.Descriptor(
  name='file_lock_entry',
  full_name='file_lock_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='flag', full_name='file_lock_entry.flag', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='file_lock_entry.type', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pid', full_name='file_lock_entry.pid', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fd', full_name='file_lock_entry.fd', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start', full_name='file_lock_entry.start', index=4,
      number=5, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='len', full_name='file_lock_entry.len', index=5,
      number=6, type=3, cpp_type=2, label=2,
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
  serialized_start=19,
  serialized_end=117,
)

DESCRIPTOR.message_types_by_name['file_lock_entry'] = _FILE_LOCK_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

file_lock_entry = _reflection.GeneratedProtocolMessageType('file_lock_entry', (_message.Message,), {
  'DESCRIPTOR' : _FILE_LOCK_ENTRY,
  '__module__' : 'file_lock_pb2'
  # @@protoc_insertion_point(class_scope:file_lock_entry)
  })
_sym_db.RegisterMessage(file_lock_entry)


# @@protoc_insertion_point(module_scope)
