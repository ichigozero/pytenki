def test_assign_leds(pytenki, led_pins):
    assert pytenki._leds is None
    pytenki.assign_leds(led_pins)
    assert pytenki._leds is not None


def test_close_leds_before_reassignment(mocker, pytenki_init, led_pins):
    spy = mocker.spy(pytenki_init._leds, 'close')
    pytenki_init.assign_leds(led_pins)
    spy.assert_called_once()
