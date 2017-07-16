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

import codecs

import sys
from typing import Sequence

from mydocpy import docformats, formats, replacements


def process(
        srcfiles,   # type: Sequence[unicode]
        srcformat,  # type: unicode
        destformat  # type: unicode
):
    from mydocpy.parse import parse_file

    # TODO: use threads or processes?
    for srcfile in srcfiles:
        docstrings = parse_file(srcfile)

        docformat = docformats.get_format(srcformat)
        for docstring in docstrings:
            docformat(docstring)

        source_replacements = []
        style_format = formats.get_format(destformat)
        for docstring in docstrings:
            style_format(docstring, source_replacements)

        with codecs.open(srcfile, "r", "utf-8") as src:
            replacements.apply(src, sys.stdout, source_replacements)

