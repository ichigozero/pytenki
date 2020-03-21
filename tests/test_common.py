import pytest


@pytest.mark.parametrize(
    'weather,expected', [
        ('晴れ', '晴れ'), ('大雨', '雨'),
        ('暴風雨', '雨'), ('一時晴', '時々晴'),
        ('雨か雪', '雨'), ('雪か雨', '雪'),
        ('', '')
    ]
)
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


def test_compose_forecast_summary(pytenki):
    pytenki._forecast = {
        'day': '今日',
        'city': '東京',
        'weather': '晴れ',
        'temp': {
            'min': '1度',
            'max': '10度'
        }
    }
    expected = (
        '今日の東京の天気は晴れ。'
        '予想最高気温は10度。'
        '予想最低気温は1度。'
    )

    assert pytenki._compose_forecast_summary() == expected


def test_compose_no_min_temp_forecast_summary(pytenki):
    pytenki._forecast = {
        'day': '今日',
        'city': '東京',
        'weather': '晴れ',
        'temp': {
            'max': '10度',
            'min': None
        }
    }
    expected = '今日の東京の天気は晴れ。予想最高気温は10度。'

    assert pytenki._compose_forecast_summary() == expected


def test_compose_no_max_temp_forecast_summary(pytenki):
    pytenki._forecast = {
        'day': '今日',
        'city': '東京',
        'weather': '晴れ',
        'temp': {
            'max': None,
            'min': '1度'
        }
    }
    expected = '今日の東京の天気は晴れ。予想最低気温は1度。'

    assert pytenki._compose_forecast_summary() == expected


def test_compose_no_min_max_temps_forecast_summary(pytenki):
    pytenki._forecast = {
        'day': '今日',
        'city': '東京',
        'weather': '晴れ',
        'temp': {
            'max': None,
            'min': None,
        }
    }
    expected = '今日の東京の天気は晴れ。'

    assert pytenki._compose_forecast_summary() == expected


invalid_forecast = {
    'none_obj': None,
    'day_blank': {
        'day': '',
        'city': '東京',
        'weather': '晴れ',
        'temp': {
            'min': '0度',
            'max': '0度'
        }
    },
    'day_none': {
        'day': None,
        'city': '東京',
        'weather': '晴れ',
        'temp': {
            'min': '0度',
            'max': '0度'
        }
    },
    'city_blank': {
        'day': '今日',
        'city': '',
        'weather': '晴れ',
        'temp': {
            'min': '0度',
            'max': '0度'
        }
    },
    'city_none': {
        'day': '今日',
        'city': None,
        'weather': '晴れ',
        'temp': {
            'min': '0度',
            'max': '0度'
        }
    },
    'weather_blank': {
        'day': '今日',
        'city': '東京',
        'weather': '',
        'temp': {
            'min': '0度',
            'max': '0度'
        }
    },
    'weather_none': {
        'day': '今日',
        'city': '東京',
        'weather': None,
        'temp': {
            'min': '0度',
            'max': '0度'
        }
    },
}


@pytest.mark.parametrize('forecast', invalid_forecast.values())
def test_compose_invalid_forecast_summary(pytenki, forecast):
    pytenki._forecast = forecast
    expected = '天気予報を取得できません。'

    assert pytenki._compose_forecast_summary() == expected
