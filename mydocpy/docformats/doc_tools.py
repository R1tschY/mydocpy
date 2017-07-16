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

from typing import Pattern, List

from mydocpy.docstrings import TypeInformation, DocString, VarType, \
    FunctionDocString
from mydocpy.source import SourceLocation
from mydocpy.utils.registry import Registry


class DocUtilsStyle(object):
    """
    Parse type information in docstring of Epydoc and Sphinx:

    For example:

        :type id: int

    or

        @type id: int

    """
    _re_type = None  # type: Pattern
    _re_rtype = None  # type: Pattern

    def __init__(self):
        # variable, parameter or return type
        #
        # Parameter with type
        # http://www.sphinx-doc.org/en/stable/domains.html#the-python-domain
        self._re_type = re.compile(
            r"^[ \t]*[@:]([a-zA-Z]+)([ \t]+\w+)?([ \t]+\w+)?[ \t]*:(.*)$",
            re.MULTILINE)

    def __call__(self, doc_string):  # type: (DocString) -> None
        type_info = doc_string.type_info or []  # type: List[TypeInformation]
        content = doc_string.content

        is_func = isinstance(doc_string, FunctionDocString)

        for match in self._re_type.finditer(content):
            field = match.group(1)
            if field in ("type", "vartype"):
                if match.group(3):
                    continue  # broken
                vartype = VarType.PARAM if is_func else VarType.VAR
                name = match.group(2).strip()
                expr = match.group(4).strip()

            elif field == "rtype":
                if match.group(2):
                    continue  # broken
                vartype = VarType.RETURN
                name = None
                expr = match.group(4).strip()

            elif field in ("param", "parameter", "arg", "argument", "key",
                           "keyword"):
                if not match.group(3):
                    continue  # no type info
                vartype = VarType.PARAM
                name = match.group(3).strip()
                expr = match.group(2).strip()
            else:
                continue

            type_info.append(TypeInformation(
                vartype, name, expr,
                SourceLocation.from_text_pos(content, match.start(0))
            ))

        doc_string.type_info = type_info


def register_doc_formats(registry): # type: (Registry) -> None
    registry.register("epydoc", DocUtilsStyle())
    registry.register("sphinx", DocUtilsStyle())
