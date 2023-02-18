
import os
import subprocess
import logging


# print(subprocess.run('env',  capture_output=True))

# os.environ.update({'ALEX':'123'})

# print('======')

# print(subprocess.run('env',  capture_output=True))

###########################

import qdsh as sh
sh.options.debug(True)

logging.basicConfig(level=logging.DEBUG)
sh.apply_options()

sh('echo 123')

###########################

# class A():
#     a123123 = None

#     def __init__(self):
#         pass

#     def __getattribute__(cls, name):
#         print('get attribute', name)
#         return name
#         pass

# print(A.a123123)

# os.chdir('/tmp')

# print(os.getcwd())

###########################

if __name__ == "__main__":
    pass
