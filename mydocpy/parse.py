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

from typing import Sequence, Union, TextIO, List, Text

from mydocpy.docstrings import DocString, FunctionDocString, ClassDocString, \
    FuncType


def parse_file(filepath):
    # type: (Union[Text, TextIO]) -> Sequence[DocString]
    """
    parse file
    :param filepath: file path to file to process
    :return:
    """
    if isinstance(filepath, basestring):
        with open(filepath, "r") as f:
            content = f.read()
        return parse(content)
    else:
        return parse(filepath.read())


def parse(content):
    # type: (unicode) -> Sequence[DocString]
    """
    parse file
    :param content: source to process
    :return:
    """
    extractor = DocStringExtractor()
    extractor.visit(ast.parse(content))
    # TODO: add a hook for use from the outside
    return extractor.doc_strings


def _get_node_docstring(node, cls=DocString):
    """
    Return the docstring for a ClassDef or FunctionDef node
    """
    if node.body:
        first_expr = node.body[0]

        if (isinstance(first_expr, ast.Expr)
                and isinstance(first_expr.value, ast.Str)):
            return cls.from_node(node, first_expr.value)


class DocStringExtractor(ast.NodeVisitor):

    doc_strings = None  # type: List[DocString]

    def __init__(self):
        self.doc_strings = []
        self.in_class = False

    def visit_ClassDef(self, node):
        docstring = _get_node_docstring(node, ClassDocString)
        if docstring:
            self.doc_strings.append(docstring)

        # inlined for performance
        in_class = self.in_class
        self.in_class = True
        self.generic_visit(node)
        self.in_class = in_class

    def visit_FunctionDef(self, node):
        docstring = _get_node_docstring(node, FunctionDocString)
        if docstring:
            docstring.args = [arg.id for arg in node.args.args]
            docstring.vaarg = node.args.vararg
            docstring.kwarg = node.args.kwarg
            if self.in_class:
                if node.decorator_list:
                    # FIXME: we hope nobody overwriten staticmethod or
                    # classmethod
                    decorators = [
                        decorator.id for decorator in node.decorator_list
                    ]
                    if "staticmethod" in decorators:
                        docstring.func_type = FuncType.STATIC
                    elif "classmethod" in decorators:
                        docstring.func_type = FuncType.CLASS
                    else:
                        docstring.func_type = FuncType.INSTANCE
                else:
                    docstring.func_type = FuncType.INSTANCE
            else:
                docstring.func_type = FuncType.FREE
            self.doc_strings.append(docstring)

        # inlined for performance
        in_class = self.in_class
        self.in_class = False
        self.generic_visit(node)
        self.in_class = in_class

