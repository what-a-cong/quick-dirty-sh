import logging
import os
import subprocess as subp
import sys
import tempfile
from types import ModuleType

logging.basicConfig(level=logging.DEBUG)
_qdsh_filepath = os.path.abspath(__file__)


class _OptionNameMeta(type):
    OutputToStd = None
    NoSystemEnv = None
    NoSaveWorkingDir = None
    NoSaveEnv = None
    UseBash = None
    Debug = None
    Encoding = None

    def __getattribute__(cls, name):
        return str(name)

    pass


class _OptionName(metaclass=_OptionNameMeta):
    pass


class _Options(dict):

    _default_options = {
        _OptionName.OutputToStd: True,
        _OptionName.NoSystemEnv: False,
        _OptionName.NoSaveWorkingDir: False,
        _OptionName.NoSaveEnv: False,
        _OptionName.UseBash: False,
        _OptionName.Debug: False,
        _OptionName.Encoding: 'utf-8',
    }

    def __init__(self):
        super(_Options, self).__init__()
        self.update(_Options._default_options)
        pass

    def debug(self, value):
        self[_OptionName.Debug] = bool(value)

    pass


class QuickDirtySh(ModuleType):

    def __init__(self, name):
        super(QuickDirtySh, self).__init__(name)

        self.options = _Options()
        self._debug = self.options[_OptionName.Debug]
        self._sh_exe = 'sh'

        self.argv = sys.argv
        self.argc = len(self.argv)
        self.env = os.environ

        self.stdout = None
        self.stderr = None
        self.exit_status = 0

        pass

    def apply_options(self):
        if self.options[_OptionName.Debug]:
            logging.basicConfig(level=logging.DEBUG)
            self._debug = True
            pass
        logging.debug('applying options: {}'.format(str(self.options)))

        if self.options[_OptionName.NoSystemEnv]:
            self.env = dict()
            # only clear this once
            self.options[_OptionName.NoSystemEnv] = False
            pass
        if self.options[_OptionName.UseBash]:
            self._sh_exe = 'bash'
            pass
        pass

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)
        pass

    def run(self, cmd, env=None, cwd=None, stdin=None):
        self._run_env = env if env else self.env
        self._run_cwd = cwd if cwd else os.getcwd()
        self._run_stdin = stdin

        self._run_tmpdir_obj = tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True)
        self._run_tmpdir = os.path.abspath(self._run_tmpdir_obj.name)
        if self._debug:
            # Have to create new temp folder, or tempfile will clear the folder
            # before program exits
            self._run_tmpdir = os.path.abspath(
                self._run_tmpdir_obj.name + '-debug')
            os.mkdir(self._run_tmpdir)
            pass
        logging.debug('tempdir: {}'.format(self._run_tmpdir))

        self._run_script_file = os.path.join(self._run_tmpdir, 'qdsh.sh')
        logging.debug('script file: {}'.format(self._run_script_file))
        self._run_data_file = os.path.join(self._run_tmpdir, 'data.out')
        logging.debug('data file: {}'.format(self._run_data_file))

        self._generate_script(cmd)
        self._run_script()
        self._get_data_and_update()

        pass

    def _generate_script(self, cmd):
        with open(self._run_script_file, 'w+') as f:
            # pre-run hook
            f.write('# pre-run hooks\n')

            # cmd to run
            f.write('# user commands\n')
            f.write(cmd)
            f.write('\n')

            # data collection
            f.write('# collect post-run data\n')
            f.write(
                "python {} {} $? \n".format(
                    _qdsh_filepath, self._run_data_file)
            )

            # post-run hooks
            f.write('# post-run hooks\n')
            pass

        pass

    def _run_script(self):
        p = subp.Popen(
            (self._sh_exe, '-e', self._run_script_file),
            env=self._run_env, cwd=self._run_cwd,
            stdin=self._run_stdin, stderr=subp.PIPE, stdout=subp.PIPE
        )
        self.stdout, self.stderr = p.communicate()
        self.stdout = self.stdout.decode(self.options[_OptionName.Encoding])
        self.stderr = self.stderr.decode(self.options[_OptionName.Encoding])
        if self.options[_OptionName.OutputToStd]:
            sys.stdout.write(self.stdout)
            sys.stderr.write(self.stderr)
        pass

    def _get_data_and_update(self):
        with open(self._run_data_file, 'r') as f:
            data = eval(f.readline())
        if not self.options[_OptionName.NoSaveWorkingDir]:
            os.chdir(data['cwd'])
        if not self.options[_OptionName.NoSaveEnv]:
            os.environ.update(data['env'])
        self.exit_status = data['exit_status']
        pass

    def exit(self, exit_code=0):
        sys.exit(exit_code)
        pass

    pass


def _gather_data(address_data, exit_status):
    """
    After running the script, gather working dir & env data and send back to
    main process.
    """
    addr = address_data
    data = {
        'cwd': str(os.getcwd()),
        'env': dict(os.environ),
        'exit_status': int(exit_status),
    }

    with open(addr, 'w') as f:
        f.write(repr(data) + '\n')

    # restore exit_status
    sys.exit(exit_status)
    pass


if __name__ == "__main__":
    "must be called with qdsh.py output_file exit_status"
    assert len(sys.argv) == 3
    _gather_data(sys.argv[1], sys.argv[2])
    pass
else:
    sys.modules[__name__] = QuickDirtySh(__name__)
    pass
