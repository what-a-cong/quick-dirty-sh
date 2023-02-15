import os
import sys
from types import ModuleType


class QuickDirtySh(ModuleType):

    def __init__(self, name):
        super(QuickDirtySh, self).__init__(name)

        self.argv = sys.argv
        self.argc = len(self.argv)
        pass

    def __call__(self, cmd):
        os.system(cmd)
        pass

    def exit(self, exit_code=0):
        sys.exit(exit_code)
        pass

    pass


sys.modules[__name__] = QuickDirtySh(__name__)
