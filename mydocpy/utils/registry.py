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

from typing import Callable


class Registry(object):
    """
    :ivar entries: registered formats
    """

    def __init__(self):
        self.entries = {}  # type: dict[unicode, Callable]

    def register(self, name, func):
        # type: (unicode, Callable) -> None
        """
        register new format
        :param name: format name
        :param func: callback
        :raises ValueError: if format name is already registered
        """

        if name in self.entries:
            raise ValueError(
                "format name {} is already registered".format(name)
            )

        self.entries[name] = func
