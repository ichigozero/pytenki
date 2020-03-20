import pytest


@pytest.mark.parametrize('weather,expected', [
        ('晴れ', '晴れ'), ('大雨', '雨'),
        ('暴風雨', '雨'), ('一時晴', '時々晴'),
        ('雨か雪', '雨'), ('雪か雨', '雪'),
        ('', '')
    ])
def test_normalize_weather_str(pytenki, weather, expected):
    pytenki._forecast = dict()
    pytenki._forecast['weather'] = weather
    pytenki._normalize_weather_str()

    assert pytenki._forecast['weather'] == expected


def test_catched_exceptions_on_normalize_weather_str(pytenki):
    pytenki._forecast = None
    pytenki._normalize_weather_str()
    assert pytenki._forecast is None

    forecast = {'weather': None}
    pytenki._forecast = forecast
    pytenki._normalize_weather_str()
    assert pytenki._forecast is forecast


def test_function_is_called_during_forecast_var_assignment(mocker, pytenki):
    spy = mocker.spy(pytenki, '_normalize_weather_str')
    pytenki.forecast = {'weather': '晴れ'}
    spy.assert_called_once()
