import pytest


def spy_assert_cloud_led(mocker, pytenki_init, func_name, weather):
    spy = mocker.spy(pytenki_init._leds.cloud, func_name)

    pytenki_init._forecast = {'weather': weather}
    pytenki_init._operate_cloud_led()

    spy.assert_called_once_with()


@pytest.mark.parametrize(
    'weather', [
        '曇り',
        '曇のち晴',
        pytest.param('晴のち曇', marks=pytest.mark.xfail),
        pytest.param('晴時々曇', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_cloud_led_to_on(mocker, pytenki_init, weather):
    spy_assert_cloud_led(mocker, pytenki_init, 'on', weather)


@pytest.mark.parametrize(
    'weather', [
        '晴のち曇',
        pytest.param('曇り', marks=pytest.mark.xfail),
        pytest.param('曇のち晴', marks=pytest.mark.xfail),
        pytest.param('晴時々曇', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_cloud_led_to_pulse(mocker, pytenki_init, weather):
    spy_assert_cloud_led(mocker, pytenki_init, 'pulse', weather)


@pytest.mark.parametrize(
    'weather', [
        '晴時々曇',
        pytest.param('曇り', marks=pytest.mark.xfail),
        pytest.param('曇のち晴', marks=pytest.mark.xfail),
        pytest.param('晴のち曇', marks=pytest.mark.xfail),
        pytest.param('晴れ', marks=pytest.mark.xfail),
    ]
)
def test_operate_cloud_led_to_blink(mocker, pytenki_init, weather):
    spy_assert_cloud_led(mocker, pytenki_init, 'blink', weather)


@pytest.mark.parametrize(
    'weather', [
        '晴れ',
        pytest.param('曇り', marks=pytest.mark.xfail),
        pytest.param('曇のち晴', marks=pytest.mark.xfail),
        pytest.param('晴のち曇', marks=pytest.mark.xfail),
        pytest.param('晴時々曇', marks=pytest.mark.xfail),
    ]
)
def test_operate_cloud_led_to_off(mocker, pytenki_init, weather):
    spy_assert_cloud_led(mocker, pytenki_init, 'off', weather)
