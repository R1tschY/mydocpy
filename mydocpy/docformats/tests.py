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

from testtools import TestCase

from mydocpy.docstrings import DocString, TypeInformation, VarType
from mydocpy.source import SourceLocation
from mydocpy.docformats.doc_tools import DocUtilsStyle


class DocUtilsStyleTests(TestCase):

    def test_SameLine(self):
        sut = DocUtilsStyle()

        input = DocString(content="""
            :type name1: int
            @type name2: long
            :type\t\tname3\t\t:\t\tstr\t\t
        """)

        sut(input)

        self.assertEqual([
            TypeInformation(
                VarType.VAR, "name1", "int", SourceLocation(1, 0)),
            TypeInformation(
                VarType.VAR, "name2", "long", SourceLocation(2, 0)),
            TypeInformation(
                VarType.VAR, "name3", "str", SourceLocation(3, 0))
        ], input.type_info)

    def test_RType(self):
        sut = DocUtilsStyle()

        input = DocString(content="""
            :rtype: int
            :rtype : list[int]
        """)

        sut(input)

        self.assertEqual([
            TypeInformation(
                VarType.RETURN, None, "int", SourceLocation(1, 0)),
            TypeInformation(
                VarType.RETURN, None, "list[int]", SourceLocation(2, 0)),
        ], input.type_info)

    def test_VarType(self):
        sut = DocUtilsStyle()

        input = DocString(content="""
            @vartype name1: long
            :vartype name2 \t: int
        """)

        sut(input)

        self.assertEqual([
            TypeInformation(
                VarType.VAR, "name1", "long", SourceLocation(1, 0)),
            TypeInformation(
                VarType.VAR, "name2", "int", SourceLocation(2, 0)),
        ], input.type_info)

    def test_ParamType(self):
        sut = DocUtilsStyle()

        input = DocString(content="""
            @param long name1: doc1
            @param name2: doc2
            @key long name3: doc1
            @argument long name4: doc1
        """)

        sut(input)

        self.assertEqual([
            TypeInformation(
                VarType.PARAM, "name1", "long", SourceLocation(1, 0)),
            TypeInformation(
                VarType.PARAM, "name3", "long", SourceLocation(3, 0)),
            TypeInformation(
                VarType.PARAM, "name4", "long", SourceLocation(4, 0)),
        ], input.type_info)

    # def test_MultiLine(self):
    #     sut = DocUtilsStyle()
    #
    #     doc = DocString(content="""
    #         Same text
    #         and more ...
    #
    #         :type name1:
    #             int
    #         @type name2:
    #             long
    #
    #         Same text
    #
    #         :type\t\tname3\t\t:
    #             \t\tstr\t\t
    #
    #         @type
    #             name4:
    #                 dict
    #
    #         :type name5:float""")
    #
    #     sut(doc)
    #
    #     self.assertEqual([
    #         TypeInformation("name1", "int", SourceLocation(None, 4, 0)),
    #         TypeInformation("name2", "long", SourceLocation(None, 6, 0)),
    #         TypeInformation("name3", "str", SourceLocation(None, 11, 0)),
    #         TypeInformation("name4", "dict", SourceLocation(None, 14, 0)),
    #         TypeInformation("name5", "float", SourceLocation(None, 18, 0))
    #     ], doc.type_info)
