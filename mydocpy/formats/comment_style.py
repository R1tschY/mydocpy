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

from enum import Enum

from typing import MutableSequence, Sequence

from mydocpy.docstrings import ClassDocString, DocString, FuncType, \
    FunctionDocString, VarType
from mydocpy.formats import Registry
from mydocpy.replacements import SourceReplacement
from mydocpy.source import SourceRange


class TypeCommentStyle(Enum):
    IN_LINE, NEW_LINE, ARG_PER_LINE = range(3)


class CommentStyle(object):

    styleOrder = None  # type: Sequence[TypeCommentStyle]

    # TODO: get editor style
    max_chars_per_line = 80  # type: int

    def __init__(self):
        # type: () -> None
        self.styleOrder = None

    def _handle_FunctionDocString(self, doc_string, source_replacements):
        # type: (FunctionDocString, MutableSequence[SourceReplacement]) -> None

        params = {}
        returns = None
        for type_info in doc_string.type_info:
            kind = type_info.var_type
            if kind in (VarType.PARAM, VarType.VAR):
                params[type_info.name] = type_info.expr
            elif kind == VarType.RETURN:
                returns = type_info.expr

        # ignore first arg of instance and class methods
        func_args = doc_string.args[:]
        if doc_string.func_type in (FuncType.INSTANCE, FuncType.CLASS):
            func_args.pop(0)

        # args
        if len(func_args) != 0 and len(params) == 0:
            arg_types = ["..."]
        else:
            arg_types = []
            for arg in func_args:
                arg_types.append(params.get(arg, "Any"))

        if doc_string.vaarg:
            arg_types.append("*" + params.get(doc_string.vaarg, "Any"))

        if doc_string.kwarg:
            arg_types.append("**" + params.get(doc_string.kwarg, "Any"))

        # TODO: add import for Any when needed!
        # TODO: use right indent (from origin docstring)
        # create
        srange = SourceRange.from_location(doc_string.obj_loc.next_line())
        replacement = "{}# type: ({}) -> {}\n".format(
            doc_string.guess_indent(), ", ".join(arg_types), returns
        )
        source_replacements.append(SourceReplacement(srange, replacement))

    def _handle_ClassDocString(self, doc_string, source_replacements):
        # type: (ClassDocString, MutableSequence[SourceReplacement]) -> None

        ivars = {}
        cvars = {}
        for type_info in doc_string.type_info:
            kind = type_info.var_type
            if kind in (VarType.IVAR, VarType.VAR):
                ivars[type_info.name] = type_info.expr
            elif kind == VarType.CVAR:
                cvars[type_info.name] = type_info.expr

        # TODO: add import for Any and ClassVar when needed!
        # TODO: use right indent (from origin docstring)
        # create
        indent = doc_string.guess_indent()
        srange = SourceRange.from_location(doc_string.doc_loc.next_line())
        replacement = "\n" + "".join(
            "{}{} = None  # type: {}\n".format(indent, name, value_type)
            for name, value_type in ivars.items()
        ) + "".join(
            "{}{} = None  # type: ClassVar[{}]\n".format(
                indent, name, value_type)
            for name, value_type in cvars.items()
        )
        source_replacements.append(SourceReplacement(srange, replacement))

    def __call__(self, doc_string, source_replacements):
        # type: (DocString, MutableSequence[SourceReplacement]) -> None

        getattr(self, "_handle_" + type(doc_string).__name__)(
            doc_string, source_replacements
        )


def register_formats(registry):
    # type: (Registry) -> None
    """
    register comment formats
    """
    registry.register("comment", CommentStyle())
