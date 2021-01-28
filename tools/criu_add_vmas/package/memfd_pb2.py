# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: memfd.proto
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
  name='memfd.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bmemfd.proto\x1a\nopts.proto\x1a\nfown.proto\"y\n\x10memfd_file_entry\x12\n\n\x02id\x18\x01 \x02(\r\x12\x1f\n\x05\x66lags\x18\x02 \x02(\rB\x10\xd2?\r\x1a\x0brfile.flags\x12\x0b\n\x03pos\x18\x03 \x02(\x04\x12\x19\n\x04\x66own\x18\x04 \x02(\x0b\x32\x0b.fown_entry\x12\x10\n\x08inode_id\x18\x05 \x02(\r\"\x8b\x01\n\x11memfd_inode_entry\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0b\n\x03uid\x18\x02 \x02(\r\x12\x0b\n\x03gid\x18\x03 \x02(\r\x12\x0c\n\x04size\x18\x04 \x02(\x04\x12\r\n\x05shmid\x18\x05 \x02(\r\x12\x1f\n\x05seals\x18\x06 \x02(\rB\x10\xd2?\r\x1a\x0bseals.flags\x12\x10\n\x08inode_id\x18\x07 \x02(\x04'
  ,
  dependencies=[opts__pb2.DESCRIPTOR,fown__pb2.DESCRIPTOR,])




_MEMFD_FILE_ENTRY = _descriptor.Descriptor(
  name='memfd_file_entry',
  full_name='memfd_file_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='memfd_file_entry.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='memfd_file_entry.flags', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\322?\r\032\013rfile.flags', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pos', full_name='memfd_file_entry.pos', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fown', full_name='memfd_file_entry.fown', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inode_id', full_name='memfd_file_entry.inode_id', index=4,
      number=5, type=13, cpp_type=3, label=2,
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
  serialized_start=39,
  serialized_end=160,
)


_MEMFD_INODE_ENTRY = _descriptor.Descriptor(
  name='memfd_inode_entry',
  full_name='memfd_inode_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='memfd_inode_entry.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uid', full_name='memfd_inode_entry.uid', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gid', full_name='memfd_inode_entry.gid', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='memfd_inode_entry.size', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shmid', full_name='memfd_inode_entry.shmid', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seals', full_name='memfd_inode_entry.seals', index=5,
      number=6, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\322?\r\032\013seals.flags', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inode_id', full_name='memfd_inode_entry.inode_id', index=6,
      number=7, type=4, cpp_type=4, label=2,
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
  serialized_start=163,
  serialized_end=302,
)

_MEMFD_FILE_ENTRY.fields_by_name['fown'].message_type = fown__pb2._FOWN_ENTRY
DESCRIPTOR.message_types_by_name['memfd_file_entry'] = _MEMFD_FILE_ENTRY
DESCRIPTOR.message_types_by_name['memfd_inode_entry'] = _MEMFD_INODE_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

memfd_file_entry = _reflection.GeneratedProtocolMessageType('memfd_file_entry', (_message.Message,), {
  'DESCRIPTOR' : _MEMFD_FILE_ENTRY,
  '__module__' : 'memfd_pb2'
  # @@protoc_insertion_point(class_scope:memfd_file_entry)
  })
_sym_db.RegisterMessage(memfd_file_entry)

memfd_inode_entry = _reflection.GeneratedProtocolMessageType('memfd_inode_entry', (_message.Message,), {
  'DESCRIPTOR' : _MEMFD_INODE_ENTRY,
  '__module__' : 'memfd_pb2'
  # @@protoc_insertion_point(class_scope:memfd_inode_entry)
  })
_sym_db.RegisterMessage(memfd_inode_entry)


_MEMFD_FILE_ENTRY.fields_by_name['flags']._options = None
_MEMFD_INODE_ENTRY.fields_by_name['seals']._options = None
# @@protoc_insertion_point(module_scope)