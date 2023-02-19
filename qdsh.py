import logging
import os
import subprocess as subp
import sys
import tempfile
from types import ModuleType

_DEFAULT_DEBUG_OPTION = False
_DEFAULT_DEBUG_OPTION = True

logging.basicConfig(level=logging.WARNING)
if _DEFAULT_DEBUG_OPTION:
    logging.basicConfig(level=logging.DEBUG)

_qdsh_filepath = os.path.abspath(__file__)


class _OptionNameMeta(type):
    Debug = None
    DebugLog = None
    Encoding = None
    NoSaveAlias = None
    NoSaveEnv = None
    NoSaveFunction = None
    NoSaveWorkingDir = None
    NoSystemEnv = None
    NoThrowForDataCollect = None
    OutputToStd = None
    SetV = None
    SetX = None
    UseBash = None

    def __getattribute__(cls, name):
        return str(name)

    pass


class _OptionName(metaclass=_OptionNameMeta):
    pass


class _Options(dict):

    _default_options = {
        _OptionName.Debug: _DEFAULT_DEBUG_OPTION,
        _OptionName.DebugLog: _DEFAULT_DEBUG_OPTION,
        _OptionName.Encoding: 'utf-8',
        _OptionName.NoSaveAlias: False,
        _OptionName.NoSaveEnv: False,
        _OptionName.NoSaveFunction: False,
        _OptionName.NoSaveWorkingDir: False,
        _OptionName.NoSystemEnv: False,
        _OptionName.NoThrowForDataCollect: False,
        _OptionName.OutputToStd: True,
        _OptionName.SetV: False,
        _OptionName.SetX: False,
    }

    def __init__(self):
        super(_Options, self).__init__()
        self.update(_Options._default_options)
        pass

    def debug(self, value):
        self[_OptionName.Debug] = bool(value)
        pass

    pass


class QuickDirtySh(ModuleType):

    def __init__(self, name):
        super(QuickDirtySh, self).__init__(name)

        self.options = _Options()
        self._debug = self.options[_OptionName.Debug]
        self._sh_exe = 'bash'

        self.argv = sys.argv
        self.argc = len(self.argv)
        self.env = os.environ

        self.stdout = None
        self.stderr = None
        self.exit_status = 0

        self._r_alias = ''
        self._r_function = ''

        pass

    def apply_options(self):
        self._debug = self.options[_OptionName.Debug]

        if self.options[_OptionName.DebugLog]:
            logging.basicConfig(level=logging.DEBUG)
            pass
        logging.debug('applying options: {}'.format(str(self.options)))

        if self.options[_OptionName.NoSystemEnv]:
            self.env = dict()
            # only clear this once
            self.options[_OptionName.NoSystemEnv] = False
            pass
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
        pass

    def run(self, cmd, env=None, cwd=None, stdin=None):
        logging.debug('cmd: {}'.format(cmd))
        self._r_env = env if env else self.env
        self._r_cwd = cwd if cwd else os.getcwd()
        self._r_stdin = stdin

        self._r_tmpdir_obj = tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True)
        self._r_tmpdir = os.path.abspath(self._r_tmpdir_obj.name)
        if self._debug:
            # Have to create new temp folder, or tempfile will clear the folder
            # before program exits
            self._r_tmpdir = os.path.abspath(
                self._r_tmpdir_obj.name + '-debug')
            os.mkdir(self._r_tmpdir)
            pass
        logging.debug('tempdir: {}'.format(self._r_tmpdir))

        self._r_script_file = os.path.join(self._r_tmpdir, 'qdsh.sh')
        logging.debug('script file: {}'.format(self._r_script_file))
        self._r_data_file = os.path.join(self._r_tmpdir, 'data')
        self._r_data_alias = os.path.join(self._r_tmpdir, 'data-alias')
        self._r_data_function = os.path.join(self._r_tmpdir, 'data-function')
        logging.debug('data file: {}'.format(self._r_data_file))
        self._r_data_stdout = os.path.join(self._r_tmpdir, 'data.out')
        self._r_data_stderr = os.path.join(self._r_tmpdir, 'data.err')

        self._generate_script(cmd)
        self._run_script()

        try:
            self._get_data_and_update()
        except Exception as e:
            if not self.options[_OptionName.NoThrowForDataCollect]:
                raise e
            pass

        return self.stdout
        pass

    def _generate_script(self, cmd):
        with open(self._r_script_file, 'w+') as f:

            # setup aliases and functions
            f.write(self._r_alias)
            f.write('\n')
            f.write(self._r_function)
            f.write('\n')

            f.write(self._generate_collect_data_script())
            f.write('\n')
            f.write('trap qdsh_collect_data exit\n')

            if self._debug and self.options[_OptionName.SetX]:
                f.write('set -x\n')
            if self._debug and self.options[_OptionName.SetV]:
                f.write('set -v\n')

            # cmd to run
            f.write('# user commands\n')
            f.write(cmd + '\n')
            pass

        pass

    def _generate_collect_data_script(self):
        cmd = 'qdsh_collect_data(){\n'

        cmd += 'QDSH_EXIT_STATUS=$?\n'
        cmd += 'set +x; set +v;\n'

        redirect = ' 1>/dev/null 2>&1'
        if self._debug:
            redirect = ' 1>{} 2>{}'.format(
                self._r_data_stdout, self._r_data_stderr)
        cmd += 'python {} {} $QDSH_EXIT_STATUS {}\n'.format(
            _qdsh_filepath, self._r_data_file, redirect)

        cmd += 'alias -p > {}\n'.format(self._r_data_alias)
        cmd += 'declare -f > {}\n'.format(self._r_data_function)

        cmd += '}\n'
        return cmd

    def _run_script(self):
        p = subp.Popen(
            (self._sh_exe, self._r_script_file),
            env=self._r_env, cwd=self._r_cwd,
            stdin=self._r_stdin, stderr=subp.PIPE, stdout=subp.PIPE
        )
        self.stdout, self.stderr = p.communicate()
        self.stdout = self.stdout.decode(
            self.options[_OptionName.Encoding]).strip()
        self.stderr = self.stderr.decode(
            self.options[_OptionName.Encoding]).strip()
        if self.options[_OptionName.OutputToStd]:
            sys.stdout.write(self.stdout)
            sys.stderr.write(self.stderr)
        pass

    def _get_data_and_update(self):
        if not os.path.exists(self._r_data_file):
            raise Exception('No data file generated')

        with open(self._r_data_file, 'r') as f:
            data = eval(f.readline())

        if not self.options[_OptionName.NoSaveWorkingDir]:
            os.chdir(data['cwd'])
            pass

        if not self.options[_OptionName.NoSaveEnv]:
            os.environ.update(data['env'])
            pass

        if not self.options[_OptionName.NoSaveAlias]:
            with open(self._r_data_alias, 'r') as f:
                self._r_alias = ''.join(f.readlines())
        else:
            self._r_alias = ''
            pass

        if not self.options[_OptionName.NoSaveFunction]:
            with open(self._r_data_function, 'r') as f:
                self._r_alias = ''.join(f.readlines())
        else:
            self._r_function = ''
            pass

        self.exit_status = data['exit_status']
        pass

    def exit(self, exit_code=0):
        sys.exit(exit_code)
        pass

    pass


def _gather_data(address_data, exit_status):
    '''
    After running the script, gather working dir & env data and send back to
    main process.
    '''
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


if __name__ == '__main__':
    'must be called with qdsh.py output_file exit_status'
    assert len(sys.argv) == 3
    _gather_data(sys.argv[1], sys.argv[2])
    pass
else:
    sys.modules[__name__] = QuickDirtySh(__name__)
    pass
