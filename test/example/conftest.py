def pytest_add_cli_fixtures(parser):
    parser.addoption('--bare-value', dest='val2', type=int, default=1)

    group = parser.getgroup('custom')
    group.addoption('-X','--value','--val', type=int, help='integer value used in test', required=True)


def pytest_addoption(parser):
    parser.addoption('--optional', type=int, default=5)
    parser.addoption('--fully-required', type=int, required=True)
