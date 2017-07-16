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

from mydocpy.utils.text import get_line_no


class LineNoTests(TestCase):

    def test_OneLine(self):
        self.assertEqual(
            (0, 5), get_line_no("-"*10, 5)
        )
        self.assertEqual(
            (0, 0), get_line_no("-"*10, 0)
        )

    def test_Multiline(self):
        s = """
        
        abc
        
        """
        self.assertEqual(
            (2, 8), get_line_no(s, s.index("abc"))
        )

        s = "\nsdghgfdhhfghabc              \n\n"
        self.assertEqual(
            (1, 16), get_line_no(s, s.index("abc"))
        )
        s = "\nabc"
        self.assertEqual(
            (1, 0), get_line_no(s, s.index("abc"))
        )
        s = "\n\nabc"
        self.assertEqual(
            (2, 0), get_line_no(s, s.index("abc"))
        )
        s = "\nabc\n\n"
        self.assertEqual(
            (1, 0), get_line_no(s, s.index("abc"))
        )
        s = "\n\nabc\n\n"
        self.assertEqual(
            (2, 0), get_line_no(s, s.index("abc"))
        )
