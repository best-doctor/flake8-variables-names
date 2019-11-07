# flake8-variables-names


[![Build Status](https://travis-ci.org/best-doctor/flake8-variables-names.svg?branch=master)](https://travis-ci.org/best-doctor/flake8-variables-names)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7502e578af3f4437179/maintainability)](https://codeclimate.com/github/best-doctor/flake8-variables-names/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c7502e578af3f4437179/test_coverage)](https://codeclimate.com/github/best-doctor/flake8-variables-names/test_coverage)
[![PyPI version](https://badge.fury.io/py/flake8-variables-names.svg)](https://badge.fury.io/py/flake8-variables-names)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-variables-names)


An extension for flake8 that helps to make more readable variables names.

We believe, that variable name should unmistakably shows, what it contains.
Thats why we try not to use varnames with only one symbol or not to use
too common names, such as `result`, `value` or `info`.

This extensions helps to detect such names. By default it works in
non-strict mode. You can change it with `--use-varnames-strict-mode`
parameter end extend variable names blacklist even more.

## Installation

    pip install flake8-variables-names


## Example

Sample file:

```python
# test.py

a = 1
foo = 2
result = a + foo
```

Usage:

```terminal
$ flake8 test.py
test.py:1:1: VNE001 single letter variable names are not allowed
test.py:2:1: VNE002 variable name should be clarified
```


## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have. Wait for approve from maintainer.
2. Create a pull request. Make sure all checks are green.
3. Fix review comments if any.
4. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`. Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/python_styleguide.md). Sorry, styleguide is available only in Russian for now.
- We respect [Django CoC](https://www.djangoproject.com/conduct/). Make soft, not bullshit.
