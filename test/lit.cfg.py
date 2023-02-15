import os
import tempfile
import lit.formats

config.name = "QDSH Lit test"
config.test_format = lit.formats.ShTest()

# tested python file which not contains lit directives will use extension name
# ".pyi" to avoid being discovered as test which having editors recognized as
# python files and have syntax highlighting
config.suffixes = ['.py', '.sh']
config.excludes = ['lit.cfg.py', 'assert.sh']

config.test_source_root = os.path.dirname(__file__)
config.test_exec_root = tempfile.TemporaryDirectory().name
print("TestExecRoot: {}".format(config.test_exec_root))

# Add project dir to path so that test scripts can import qdsh
project_dir = os.path.abspath(os.path.join(config.test_source_root, '..'))
config.environment['PYTHONPATH'] = project_dir

config.substitutions.append(('%{source_root}', config.test_source_root))
