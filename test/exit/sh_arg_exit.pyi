import qdsh as sh

assert(sh.argc == 2)
sh.exit(int(sh.argv[1]))
