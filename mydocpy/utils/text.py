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

from typing import Text, Tuple

from mydocpy.source import SourceLocation


def get_line_no(text, pos):  # type: (Text, int) -> SourceLocation
    """
    get line number (starting at 0) and column offset of ``pos`` in ``text``.

    :return: tuple of ``(lineno, col_offset)``
    """
    last_nl = text.rfind('\n', 0, pos)
    if last_nl < 0:
        return SourceLocation(0, pos)

    return SourceLocation(text[:pos].count('\n'), pos - (last_nl + 1))
