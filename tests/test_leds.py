def test_assign_leds(pytenki, led_pins):
    assert pytenki._leds is None
    pytenki.assign_leds(led_pins)
    assert pytenki._leds is not None
