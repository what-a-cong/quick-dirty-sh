#RUN: python %s

import qdsh as sh

sh('exit 1')
assert sh.exit_status == 1

sh('exit 2')
assert sh.exit_status == 2
