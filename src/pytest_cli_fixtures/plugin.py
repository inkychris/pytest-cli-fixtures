import dataclasses
import itertools
import re

import pytest


def pytest_addhooks(pluginmanager):
    import pytest_cli_fixtures.hooks
    pluginmanager.add_hookspecs(pytest_cli_fixtures.hooks)


@dataclasses.dataclass
class _RegisteredOption:
    opt_names: list[tuple[str]]
    attrs: dict
    required: bool
    is_fixture: bool = False

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

        globals()[f'_cli_fixture_{fixture_name}'] = pytest.fixture(
            scope='session',
            name=fixture_name
        )(fixture)


class _Parser:
    def __init__(self, parser, stash, parent=None):
        self._parser = parser
        self._stash = stash
        self._parent = parent
        if '_anonymous' in self._parser.__dict__:
            self._parser._anonymous = self._wrapped(self._parser._anonymous)
        if '_groups' in self._parser.__dict__:
            for i, group in enumerate(self._parser._groups):
                self._parser._groups[i] = self._wrapped(group)
        self._fixture_mode = False

    def _wrapped(self, parser):
        return self.__class__(parser, self._stash, parent=self)

    def __getattr__(self, attr):
        return getattr(self._parser, attr)

    def addoption(self, *optnames, **attrs):
        option = _RegisteredOption(
            optnames, attrs,
            required=attrs.pop('required', False),
            is_fixture=self.fixture_mode)
        self._stash['registered_options'].append(option)
        option.register_fixture()
        return self._parser.addoption(*optnames, **attrs)

    def getgroup( self, name, description='', after=None):
        return self._wrapped(self._parser.getgroup(name, description, after))

    @property
    def fixture_mode(self):
        return self._fixture_mode or getattr(self._parent, 'fixture_mode', False)

    @fixture_mode.setter
    def fixture_mode(self, val):
        self._fixture_mode = val


@pytest.hookimpl(hookwrapper=True)
def pytest_load_initial_conftests(early_config):
    early_config.stash['registered_options'] = []
    early_config._parser = _Parser(early_config._parser, early_config.stash)
    yield
    early_config._parser.fixture_mode = True
    early_config.hook.pytest_add_cli_fixtures(parser=early_config._parser)


def pytest_collection_finish(session):
    required_fixtures = set(itertools.chain(*[item.fixturenames for item in session.items]))
    registered_options = session.config.stash['registered_options']
    missing_options = [
        '/'.join(option.opt_names)
        for option in registered_options
        if not session.config.getoption(option.dest)
        and (
            option.dest in required_fixtures
            or not option.is_fixture and option.required)
    ]
    if missing_options:
        session.config._parser._getparser().error(f'the following arguments are required: {", ".join(missing_options)}')
