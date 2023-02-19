#RUN: python %s | filecheck %s

import qdsh as sh

sh.options['Debug'] = True
sh.options['SetX'] = True
sh.apply_options()

sh('echo enable filecheck-dag')
# CHECK: dag

sh('echo 123')
# CHECK-DAG: 123
# CHECK-DAG: + echo 123

assert sh.stdout == '123'
assert '+ echo 123' in sh.stderr
