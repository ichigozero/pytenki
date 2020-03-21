import pytest


def spy_rain_led(mocker, pytenki_init, func_name, weather):
    spy = mocker.spy(pytenki_init._leds.rain, func_name)

    pytenki_init._forecast = {'weather': weather}
    pytenki_init._operate_rain_led()

    return spy


@pytest.mark.parametrize(
    'weather', [
        '雨',
        '雨のち晴',
        pytest.param('晴のち雨', marks=pytest.mark.xfail),
        pytest.param('晴時々雨', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_rain_led_to_on(mocker, pytenki_init, weather):
    spy = spy_rain_led(mocker, pytenki_init, 'on', weather)
    spy.assert_called_once_with()


@pytest.mark.parametrize(
    'weather', [
        '晴のち雨',
        pytest.param('雨', marks=pytest.mark.xfail),
        pytest.param('雨のち晴', marks=pytest.mark.xfail),
        pytest.param('晴時々雨', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_rain_led_to_pulse(mocker, pytenki_init, weather):
    spy = spy_rain_led(mocker, pytenki_init, 'pulse', weather)
    spy.assert_called_once_with(1, 1)


@pytest.mark.parametrize(
    'weather', [
        '晴時々雨',
        pytest.param('雨', marks=pytest.mark.xfail),
        pytest.param('雨のち晴', marks=pytest.mark.xfail),
        pytest.param('晴のち雨', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_rain_led_to_blink(mocker, pytenki_init, weather):
    spy = spy_rain_led(mocker, pytenki_init, 'blink', weather)
    spy.assert_called_once_with(1, 1)


@pytest.mark.parametrize(
    'weather', [
        '晴れ',
        pytest.param('雨', marks=pytest.mark.xfail),
        pytest.param('雨のち晴', marks=pytest.mark.xfail),
        pytest.param('晴のち雨', marks=pytest.mark.xfail),
        pytest.param('晴時々雨', marks=pytest.mark.xfail),
    ]
)
def test_operate_rain_led_to_off(mocker, pytenki_init, weather):
    spy = spy_rain_led(mocker, pytenki_init, 'off', weather)
    spy.assert_called_once_with()
