def pytest_add_cli_fixtures(parser):
    group = parser.getgroup('my args')
    group.addoption('--value', dest='my_val', type=int, required=True)
