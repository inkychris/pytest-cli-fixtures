def test_without_fixture():
    assert 1 + 2 == 3


def test_with_fixture(value):
    assert 1 + value == 3


def test_with_optional_fixture(val2):
    assert val2 + 2 == 3
