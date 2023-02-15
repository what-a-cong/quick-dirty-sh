import os
import sys


class QuickDirtySh():

    def __call__(self, cmd):
        os.system(cmd)
        pass

    pass


sys.modules[__name__] = QuickDirtySh()
