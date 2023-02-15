#RUN: env SOURCE_ROOT=%{source_root} CUR_DIR=%S bash %s

source "$SOURCE_ROOT/assert.sh"

python "$CUR_DIR/sh_exit.pyi"
assert_eq "$?" "1" "exit code does not match"

python "$CUR_DIR/sh_arg_exit.pyi" 0
assert_eq "$?" "0" "exit code does not match"

python "$CUR_DIR/sh_arg_exit.pyi" 255
assert_eq "$?" "255" "exit code does not match"
