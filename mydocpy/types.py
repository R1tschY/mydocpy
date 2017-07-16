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

import re
from collections import namedtuple

from typing import Text, Tuple, Sequence

ImportedType = namedtuple("ImportedType", ["module", "name"])


class TypeInterpreter(object):

    # options
    # imports.prevered_import = typing | collections

    def interpret(self, type_expr):
        # type: (Text) -> Tuple[Text, Sequence[ImportedType]]
        """
        Interpret a user type expression to a python type hint
        :param type_expr: type expression (for example:
            ``List[int]`` or ``list<int>``)
        :return: Type hint expression and needed imports
        """
        re.sub(r"(\S+)\s*->\s*(\S+)", "Callable[[\1], \2]")
        re.sub(r"(\S+)\s*|\s*(\S+)+", "Union[\1, \2]")

        re.sub(r"[<(]", "[")
        re.sub(r"[>)]", "]")

        return (type_expr, ())

        typing_replacements = {
            "dict": "Dict",
            "list": "List",
            "set": "Set",
            "tuple": "Tuple",
            "defaultdict": "DefaultDict",
            "frozenset": "FrozenSet",
            "namedtuple": "NamedTuple",
            "deque": "Deque",
            "str": "ByteString",
            "unicode": "Text",
            "string": "Text",
            "object": "Any",
            "function": "Callable"
        }

        builtin_replacements = {
            "integer": "int",
            "long": "int",
            "double": "float",
            "real": "float",
            "floating point": "float"
        }



