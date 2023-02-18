# RUN: python %s

import qdsh as sh
import imp
import os

singleton_2 = imp.load_source('singleton_2', os.path.join(
    os.path.dirname(__file__), 'singleton_2.pyi'))

assert(id(sh) == singleton_2.get_qdsh_id())
