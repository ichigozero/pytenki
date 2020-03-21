import pytest


def spy_assert_snow_led(mocker, pytenki_init, func_name, weather):
    spy = mocker.spy(pytenki_init._leds.snow, func_name)

    pytenki_init._forecast = {'weather': weather}
    pytenki_init._operate_snow_led()

    spy.assert_called_once_with()


@pytest.mark.parametrize(
    'weather', [
        '雪',
        '雪のち晴',
        pytest.param('晴のち雪', marks=pytest.mark.xfail),
        pytest.param('晴時々雪', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_snow_led_to_on(mocker, pytenki_init, weather):
    spy_assert_snow_led(mocker, pytenki_init, 'on', weather)


@pytest.mark.parametrize(
    'weather', [
        '晴のち雪',
        pytest.param('雪', marks=pytest.mark.xfail),
        pytest.param('雪のち晴', marks=pytest.mark.xfail),
        pytest.param('晴時々雪', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_snow_led_to_pulse(mocker, pytenki_init, weather):
    spy_assert_snow_led(mocker, pytenki_init, 'pulse', weather)


@pytest.mark.parametrize(
    'weather', [
        '晴時々雪',
        pytest.param('雪', marks=pytest.mark.xfail),
        pytest.param('雪のち晴', marks=pytest.mark.xfail),
        pytest.param('晴のち雪', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_snow_led_to_blink(mocker, pytenki_init, weather):
    spy_assert_snow_led(mocker, pytenki_init, 'blink', weather)


@pytest.mark.parametrize(
    'weather', [
        '晴れ',
        pytest.param('雪', marks=pytest.mark.xfail),
        pytest.param('雪のち晴', marks=pytest.mark.xfail),
        pytest.param('晴のち雪', marks=pytest.mark.xfail),
        pytest.param('晴時々雪', marks=pytest.mark.xfail),
    ]
)
def test_operate_snow_led_to_off(mocker, pytenki_init, weather):
    spy_assert_snow_led(mocker, pytenki_init, 'off', weather)
