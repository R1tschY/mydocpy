# -*- coding=utf-8 -*-
#
# Copyright 2017 Richard Liebscher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
from collections import namedtuple
from enum import Enum

from typing import MutableSequence, Optional, Sequence, Text

from mydocpy.source import SourceLocation


class VarType(Enum):
    PARAM, VAR, CVAR, IVAR, RETURN = range(5)


TypeInformation = namedtuple(
    'TypeInformation',
    ['var_type', 'name', 'expr', 'source_loc']
)


class DocString(object):
    content = None  # type: Text
    obj_loc = None  # type: SourceLocation
    doc_loc = None  # type: SourceLocation
    type_info = None  # type: MutableSequence[TypeInformation]

    def __init__(self, content=None, obj_loc=None, source_loc=None,
                 type_info=None):
        self.content = content
        self.obj_loc = obj_loc
        self.doc_loc = source_loc
        self.type_info = type_info

    def guess_indent(self):
        # type: () -> Text
        lastnl = self.content.rfind("\n")
        if lastnl == -1:
            return "   "  # TODO: use editor config and indent of outer scope

        start = lastnl + 1
        s = self.content[start:]
        length = len(s) - len(s.lstrip())
        return self.content[start:start+length]

    @classmethod
    def from_node(cls, obj_node, doc_node):
        # type: (ast.stmt, ast.Str) -> DocString
        return cls(
            doc_node.s,
            SourceLocation.from_node(obj_node),
            SourceLocation.from_node(doc_node)
        )

    def __repr__(self):
        return (
            "DocString(content={}, obj_loc={}, doc_loc={}, "
            "type_information={})".format(
                repr(self.content), repr(self.obj_loc), repr(self.doc_loc),
                repr(self.type_info)
            )
        )

    def _keys(self):
        return (self.content, self.obj_loc, self.doc_loc, self.type_info)

    def __eq__(self, other):
        return type(self) == type(other) and self._keys() == other._keys()


class FuncType(Enum):
    FREE, INSTANCE, CLASS, STATIC = range(4)


class FunctionDocString(DocString):
    args = None  # type: Sequence[Text]
    vaarg = None  # type: Optional[Text]
    kwarg = None  # type: Optional[Text]
    func_type = None  # type: Optional[FuncType]

    def __init__(self, content=None, source_loc=None,
                 type_info=None, params=None, vararg=None, kwarg=None,
                 func_type=None
                 ):
        super(FunctionDocString, self).__init__(content, source_loc, type_info)
        self.args = params
        self.vaarg = vararg
        self.kwarg = kwarg
        self.func_type = func_type

    def __repr__(self):
        return (
            "FunctionDocString(content={}, source_location={}, "
            "type_information={}, args={}, vaarg={}, kwarg={}, "
            "func_type={})".format(
                repr(self.content), repr(self.doc_loc),
                repr(self.type_info), repr(self.args), repr(self.vaarg),
                repr(self.kwarg), repr(self.func_type)
            )
        )

    def _keys(self):
        return (self.content, self.doc_loc, self.type_info, self.args,
                self.func_type)


class ClassDocString(DocString):

    def __repr__(self):
        return (
            "ClassDocString(content={}, obj_loc={}, doc_loc={}, "
            "type_information={})".format(
                repr(self.content), repr(self.obj_loc), repr(self.doc_loc),
                repr(self.type_info)
            )
        )

