

.PHONY: test-install
test-install:
	python3 -m pip install nox

.PHONY: test
test:
	python3 -m nox -k "not debug"

.PHONY: test-debug
test-debug:
	python3 -m nox -t debug