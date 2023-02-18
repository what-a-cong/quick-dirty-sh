#RUN: python %s

import qdsh as sh
import os

sh('export QDSH=test')

assert os.environ.get('QDSH', None) == 'test'

sh('export QDSH=test-again')

assert os.environ.get('QDSH', None) == 'test-again'
