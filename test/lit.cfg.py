import os
import tempfile
import lit.formats

config.name = "QDSH Lit test"
config.test_format = lit.formats.ShTest(True)

config.suffixes = ['.py']
config.excludes = ['lit.cfg.py']

config.test_source_root = os.path.dirname(__file__)
config.test_exec_root = tempfile.TemporaryDirectory().name
print("TestExecRoot: {}".format(config.test_exec_root))
