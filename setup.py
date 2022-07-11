import pathlib
import setuptools

about = {}
exec(pathlib.Path('src/pytest_cli_fixtures/__about__.py').read_text(), about)


setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    python_requires='>3.6',
    url=about['__uri__'],
    author=about['__author__'],
    packages=["pytest_cli_fixtures"],
    package_dir={'':'src'},
    entry_points={"pytest11": ["pytest_cli_fixtures = pytest_cli_fixtures.plugin"]},
    classifiers=["Framework :: Pytest"],
)
