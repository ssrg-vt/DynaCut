# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ipc-sem.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ipc_desc_pb2 as ipc__desc__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ipc-sem.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ripc-sem.proto\x1a\x0eipc-desc.proto\"=\n\ripc_sem_entry\x12\x1d\n\x04\x64\x65sc\x18\x01 \x02(\x0b\x32\x0f.ipc_desc_entry\x12\r\n\x05nsems\x18\x02 \x02(\r'
  ,
  dependencies=[ipc__desc__pb2.DESCRIPTOR,])




_IPC_SEM_ENTRY = _descriptor.Descriptor(
  name='ipc_sem_entry',
  full_name='ipc_sem_entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='desc', full_name='ipc_sem_entry.desc', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nsems', full_name='ipc_sem_entry.nsems', index=1,
      number=2, type=13, cpp_type=3, label=2,
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
  serialized_start=33,
  serialized_end=94,
)

_IPC_SEM_ENTRY.fields_by_name['desc'].message_type = ipc__desc__pb2._IPC_DESC_ENTRY
DESCRIPTOR.message_types_by_name['ipc_sem_entry'] = _IPC_SEM_ENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ipc_sem_entry = _reflection.GeneratedProtocolMessageType('ipc_sem_entry', (_message.Message,), {
  'DESCRIPTOR' : _IPC_SEM_ENTRY,
  '__module__' : 'ipc_sem_pb2'
  # @@protoc_insertion_point(class_scope:ipc_sem_entry)
  })
_sym_db.RegisterMessage(ipc_sem_entry)


# @@protoc_insertion_point(module_scope)
