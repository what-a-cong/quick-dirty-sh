# Quick Dirty Sh

A Quick & Dirty Shell library for Python, which helps you write a Python script
that works like a shell script.

```python
import qdsh as sh

sh('echo hello world')
```

## Why this project?

There are penty of python shell scripting modules, such as [Plumbum](https://plumbum.readthedocs.io/en/latest/)
and [sh](https://github.com/amoffat/sh). But they don't quite meet my needs, which
as the project's name suggests, is quick to learn and use, despite being dirty.

This module aims to help those who is familiar with Python and not so good at
shell scripting (I am one of those people) to create some temporary Python
scripts that work like shell scripts.

You can consider this module a wrapper of os, sys and subprocess.

## Installation

This module aims to work with offline servers, so the core code file
is `qdsh.py`, which you can copy & paste to your project or system and just
import it then use it.

Or just like any other python modules, you can install it by pip:

```
pip install qdsh
```

## Quick Usage

## Options

## References

- [sh](https://github.com/amoffat/sh)