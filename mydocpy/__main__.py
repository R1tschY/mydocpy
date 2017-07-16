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

import argparse
import sys

from mydocpy import process
import mydocpy.docformats as docformats
import mydocpy.formats as formats


def main():
    parser = argparse.ArgumentParser(
        description='Convert Epy/Sphinx docstring type documentation to python '
                    'type hints'
    )

    formats.load_formats()
    docformats.load_formats()

    parser.add_argument(
        '-s', '--src-format', metavar='SRCFMT', type=str,
        help='Format of source doc strings. '
        'Supported formats: ' + ", ".join(docformats.get_formats())
    )

    parser.add_argument(
        '-f', '--format', metavar='FMT', type=str,
        help='Destination format of type traits. '
        'Supported formats: ' + ", ".join(formats.get_formats())
    )

    parser.add_argument(
        "files", metavar='FILE', nargs='+', default=None,
        help='File paths which should be processed'
    )

    args = parser.parse_args()
    process(args.files, args.src_format, args.format)

    return 0

if __name__ == '__main__':
    sys.exit(main())
