def test_no_args(plugin_tester):
    result = plugin_tester.runpytest()

    for flag in [
        'following arguments are required',
        '-X/--value/--val',
        '--fully-required'
    ]:
        assert flag in result.stderr.str()


def test_only_standard_arg(plugin_tester):
    result = plugin_tester.runpytest('--fully-required=1')

    for flag in ['following arguments are required', '-X/--value/--val']:
        assert flag in result.stderr.str()

    assert '--fully-required' not in result.stderr.str()


def test_standard_arg_invalid(plugin_tester):
    result = plugin_tester.runpytest('--fully-required=a', '--value=1')

    for val in ['--fully-required', 'invalid int value']:
        assert val in result.stderr.str()


def test_valid(plugin_tester):
    result = plugin_tester.runpytest('--fully-required=1', '--value=2')
    result.assert_outcomes(passed=3)


def test_invalid_fixture_arg(plugin_tester):
    result = plugin_tester.runpytest('--fully-required=1', '--value=x')

    for val in ['-X/--value/--val', 'invalid int value']:
        assert val in result.stderr.str()
