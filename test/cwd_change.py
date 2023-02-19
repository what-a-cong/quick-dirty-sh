#RUN: python %s

import qdsh as sh
import os

sh('cd /tmp')

print(os.getcwd())

assert os.getcwd() == '/tmp'

sh('cd /etc')

assert os.getcwd() == '/etc'
