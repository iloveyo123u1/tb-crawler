# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='comments.proto',
  package='com.langtaojin.guang.taobao',
  serialized_pb='\n\x0e\x63omments.proto\x12\x1b\x63om.langtaojin.guang.taobao\"\xa0\x01\n\x08\x63omments\x12\x0c\n\x04user\x18\x01 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x02(\t\x12\x0c\n\x04time\x18\x03 \x02(\r\x12\x0e\n\x06result\x18\x04 \x02(\r\x12\x0e\n\x06rateid\x18\x05 \x01(\x04\x12\x0e\n\x06userid\x18\x06 \x01(\x04\x12\x10\n\x08userrank\x18\x07 \x01(\r\x12\x14\n\x0cuserviplevel\x18\x08 \x01(\r\x12\x0f\n\x07tradeid\x18\t \x01(\x04')




_COMMENTS = descriptor.Descriptor(
  name='comments',
  full_name='com.langtaojin.guang.taobao.comments',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='user', full_name='com.langtaojin.guang.taobao.comments.user', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content', full_name='com.langtaojin.guang.taobao.comments.content', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='time', full_name='com.langtaojin.guang.taobao.comments.time', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='result', full_name='com.langtaojin.guang.taobao.comments.result', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rateid', full_name='com.langtaojin.guang.taobao.comments.rateid', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userid', full_name='com.langtaojin.guang.taobao.comments.userid', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userrank', full_name='com.langtaojin.guang.taobao.comments.userrank', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='userviplevel', full_name='com.langtaojin.guang.taobao.comments.userviplevel', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tradeid', full_name='com.langtaojin.guang.taobao.comments.tradeid', index=8,
      number=9, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=48,
  serialized_end=208,
)



class comments(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COMMENTS
  
  # @@protoc_insertion_point(class_scope:com.langtaojin.guang.taobao.comments)

# @@protoc_insertion_point(module_scope)