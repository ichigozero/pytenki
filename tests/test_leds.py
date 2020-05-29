def test_assign_leds(pytenki, led_pins):
    assert pytenki._leds is None
    pytenki.assign_leds(
        {
            'fine': '',
            'cloud': '',
            'rain': '',
            'snow': ''
        }
    )
    assert pytenki._leds is None
    pytenki.assign_leds(led_pins)
    assert pytenki._leds is not None


def test_close_leds_before_reassignment(mocker, pytenki_init, led_pins):
    spy = mocker.spy(pytenki_init._leds, 'close')
    pytenki_init.assign_leds(led_pins)
    spy.assert_called_once()


def test_operate_all_weather_leds(mocker, pytenki_init):
    methods = ['_operate_fine_led', '_operate_cloud_led',
               '_operate_rain_led', '_operate_snow_led']
    spies = list()

    for method in methods:
        spies.append(mocker.spy(pytenki_init, method))

    pytenki_init.operate_all_weather_leds()

    for spy in spies:
        spy.assert_called_once()
