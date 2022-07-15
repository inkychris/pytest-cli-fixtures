# pytest-cli-fixtures

[![Package Version][pypi_badge]][pypi]
[![Python Versions][pyversions_badge]][pypi]
[![Build Status][ci_status_badge]][gh_actions]
[![Code Coverage][codecov_badge]][codecov]
[![License][license_badge]][license_file]

[pypi]: https://pypi.python.org/pypi/pytest-cli-fixtures
[pypi_badge]: https://img.shields.io/pypi/v/pytest-cli-fixtures.svg

[pyversions_badge]: https://img.shields.io/pypi/pyversions/pytest-cli-fixtures.svg

[gh_actions]: https://github.com/inkychris/pytest-cli-fixtures/actions
[ci_status_badge]: https://github.com/inkychris/pytest-cli-fixtures/actions/workflows/ci.yaml/badge.svg

[codecov]: https://codecov.io/gh/inkychris/pytest-cli-fixtures
[codecov_badge]: https://codecov.io/gh/inkychris/pytest-cli-fixtures/branch/main/graph/badge.svg?token=TYWP82UBSB

[license_badge]: https://img.shields.io/pypi/l/pytest-cli-fixtures.svg
[license_file]: https://github.com/inkychris/pytest-cli-fixtures/blob/main/LICENSE.md

The `pytest-cli-fixtures` plugin provides a way
to automatically register fixtures
based off of command line argument definitions.
This plugin will also allow
mandatory arguments to be omitted from the command line
when tests don't use the fixtures
that they are associated with.

## Usage
There is only one hook function
that is needed to use CLI fixtures:

```python
def pytest_add_cli_fixtures(parser):
    ...
```

This hook is similar to the built-in `pytest_addoption` hook,
and the `parser` object that is provided
is the same as in the built-in hook.

***Note:*** Like the built-in [`pytest_addoption`][pytest_addoption_doc] hook,
the `pytest_add_cli_fixtures` hook
should only be implemented
in plugins, or in `conftest.py`.

[pytest_addoption_doc]: https://docs.pytest.org/en/latest/reference/reference.html#_pytest.hookspec.pytest_addoption

## Installation
This plugin is available on [PyPI][pypi]:
```
> pip install pytest-cli-fixtures
```
***Note:*** *This plugin requires [pytest][pytest]
version 7.0 or later.*

[pytest]: https://docs.pytest.org/

## Example
The following `conftest.py` defines
a `--value` argument within the `my args` group.
Since it specifies a `dest`,
the fixture relating to the value
will be called `my_val`.
The argument specifies `required=True`,
meaning that `pytest` will return an error
if a test uses the `my_val` fixture
but `--value` isn't specified on the command line.

```python
# conftest.py

def pytest_add_cli_fixtures(parser):
    group = parser.getgroup('my args')
    group.addoption('--value', dest='my_val', type=int, required=True)
```

With the following test file,
the `--value` argument must be specified
or `pytest` will return an error.
Alternatively, filters would need to be used
to exclude the test that uses the CLI fixture.

```python
# test_something.py

def test_something_else():
    assert 1 + 2 == 3


def test_value(my_val):
    assert 1 + my_val == 3
```

### Without arguments
```
> pytest example
=================================== test session starts ====================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: C:\...\pytest-cli-fixtures, configfile: pytest.ini
plugins: cli-fixtures-1.0
collected 2 items

================================== no tests ran in 0.01s ===================================
ERROR: usage: pytest [options] [file_or_dir] [file_or_dir] [...]
pytest: error: the following arguments are required: --value
```

### Filter out test that uses CLI fixture
```
> pytest example -k 'not test_value'
=================================== test session starts ====================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: C:\...\pytest-cli-fixtures, configfile: pytest.ini
plugins: cli-fixtures-1.0
collected 2 items / 1 deselected / 1 selected

example\test_something.py .                                                           [100%]

============================= 1 passed, 1 deselected in 0.02s ==============================
```

### Provide CLI fixture argument
```
> pytest example --value=2
=================================== test session starts ====================================
platform win32 -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
rootdir: C:\...\pytest-cli-fixtures, configfile: pytest.ini
plugins: cli-fixtures-1.0
collected 2 items

example\test_something.py ..                                                          [100%]

==================================== 2 passed in 0.03s =====================================
```
