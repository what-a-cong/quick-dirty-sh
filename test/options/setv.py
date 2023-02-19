#RUN: python %s | filecheck %s

import qdsh as sh

sh.options['Debug'] = True
sh.options['SetV'] = True
sh.apply_options()

sh('echo enable filecheck-dag')
# CHECK: dag

sh('echo 123 && echo 456')
# CHECK-DAG: 123
# CHECK-DAG: echo 123 && echo 456

assert sh.stdout == '123\n456'
assert 'echo 123 && echo 456' in sh.stderr
