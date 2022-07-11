import pytest


def pytest_addhooks(pluginmanager):
    import pytest_cli_fixtures.hooks
    pluginmanager.add_hookspecs(pytest_cli_fixtures.hooks)


@pytest.hookimpl(trylast=True)
def pytest_load_initial_conftests(early_config, parser, args):
    early_config.hook.pytest_add_cli_fixtures(parser=parser)
