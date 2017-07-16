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

import os
import pkgutil
from importlib import import_module

from typing import Sequence, Text, Callable

from mydocpy.docstrings import DocString
from mydocpy.utils.registry import Registry


registry = None  # type: Registry


def get_formats():
    # type: () -> Sequence[unicode]
    """
    :return: names of all registered formats or None if formats are not
        loaded (call ``load_formats`` first)
    """
    return registry.entries.keys() if registry else None


def get_format(name):
    # type: (Text) -> Callable[DocString, None]
    """
    Get format with ``name``

    :raises: KeyError, when format with ``name`` does not exit
    """
    return registry.entries[name]


def load_formats():
    # type: () -> None
    """
    import all format modules and call ``register_doc_formats(registry)`` on
    them (when a module has this function).
    """
    global registry

    if registry is not None:
        return

    registry = Registry()

    modules = pkgutil.iter_modules(
        [os.path.dirname(__file__)],
        'mydocpy.docformats.'
    )
    # TODO: add a way to add formats from the outside

    for module_loader, name, ispkg in modules:
        if not ispkg:
            # TODO: use module_loader?
            mdl = import_module(name)
            if hasattr(mdl, 'register_doc_formats'):
                mdl.register_doc_formats(registry)


