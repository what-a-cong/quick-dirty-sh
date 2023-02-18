#RUN: python %s | filecheck %s

import qdsh as sh

sh('echo Hello world!')
# CHECK: Hello world!
