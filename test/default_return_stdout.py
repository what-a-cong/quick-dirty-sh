#RUN: python %s

import qdsh as sh

string = 'Hello world!'
assert string == sh('echo {}'.format(string))
