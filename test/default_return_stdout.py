#RUN: python %s

import qdsh as sh

string = 'Hello world!'
assert string.strip() == str(sh('echo {}'.format(string))).strip()
