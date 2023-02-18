#RUN: python %s | filecheck %s

import qdsh as sh

sh("""
echo line 1
echo line 2
echo line 3
""")

# CHECK: line 1
# CHECK: line 2
# CHECK: line 3
