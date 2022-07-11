def test_no_args(plugin_tester):
    result = plugin_tester.runpytest('-k=test_without_fixture')

    for flag in ['required', '--fully-required']:
        assert flag in result.stderr.str()

    assert '-X/--value/--val' not in result.stderr.str()


def test_only_standard_arg(plugin_tester):
    result = plugin_tester.runpytest('-k=test_without_fixture', '--fully-required=1')
    result.assert_outcomes(passed=1)


def test_standard_arg_invalid(plugin_tester):
    result = plugin_tester.runpytest('-k=test_without_fixture', '--fully-required=a', '--value=1')

    for val in ['--fully-required', 'invalid int value']:
        assert val in result.stderr.str()


def test_with_fixture_arg(plugin_tester):
    result = plugin_tester.runpytest('-k=test_without_fixture', '--fully-required=1', '--value=2')
    result.assert_outcomes(passed=1)
