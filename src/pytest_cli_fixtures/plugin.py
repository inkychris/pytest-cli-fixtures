import dataclasses
import re

import pytest


def pytest_addhooks(pluginmanager):
    import pytest_cli_fixtures.hooks
    pluginmanager.add_hookspecs(pytest_cli_fixtures.hooks)


@dataclasses.dataclass
class _RegisteredOption:
    opt_names: list[tuple[str]]
    attrs: dict

    @property
    def dest(self):
        try:
            return self.attrs['dest']
        except KeyError:
            bare_names = [
                re.sub(r'^-{1,2}', '', name).replace('-', '_')
                for name in self.opt_names
            ]
            return [
                *[name for name in bare_names if len(name) > 1],
                *[name for name in bare_names if len(name) == 1],
            ][0]

    def register_fixture(self):
        fixture_name = self.dest

        def fixture(pytestconfig):
            return pytestconfig.getoption(fixture_name)

        globals()[fixture_name] = pytest.fixture(scope='session')(fixture)


_registered_options = []


def _patch_addoption(parser):
    option_group_class = type(parser.getgroup(''))
    addoption = option_group_class.addoption

    def _addoption(self, *optnames, **attrs):
        _registered_options.append(
            _RegisteredOption(optnames, attrs))
        return addoption(self, *optnames, **attrs)

    option_group_class.addoption = _addoption


@pytest.hookimpl(trylast=True)
def pytest_load_initial_conftests(early_config, parser, args):
    _patch_addoption(parser)

    early_config.hook.pytest_add_cli_fixtures(parser=parser)

    for option in _registered_options:
        option.register_fixture()
