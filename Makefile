.PHONY: empty
empty:
	echo "an empty makefile target"

.PHONY: test-install
test-install:
	python3 -m pip install nox

.PHONY: test
test:
	python3 -m nox -k "not manual"

.PHONY: lit
lit:
	python3 -m nox -s lit

.PHONY: lit-debug
lit-debug:
	python3 -m nox -s lit_debug