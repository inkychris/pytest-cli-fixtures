import pathlib

import pytest


pytest_plugins = ["pytester"]


@pytest.fixture
def plugin_tester(pytester):
    example_dir = pathlib.Path(__file__).absolute().parent / 'example'
    pytester.copy_example(example_dir / 'test_test.py')
    pytester.copy_example(example_dir / 'conftest.py')
    yield pytester
