def test_assign_button(pytenki):
    assert pytenki._button is None
    pytenki.assign_button('')
    assert pytenki._button is None
    pytenki.assign_button(2)
    assert pytenki._button is not None


def test_close_button_before_reassignment(mocker, pytenki_init, button_pin):
    spy = mocker.spy(pytenki_init._button, 'close')
    pytenki_init.assign_button(button_pin)
    spy.assert_called_once()


def test_tts_forecast_summary_after_button_press(
        mock_factory, monkeypatch, mocker, pytenki_init):
    def mock_func():
        pass
    monkeypatch.setattr(pytenki_init, '_tts_forecast_summary', mock_func)

    spy = mocker.spy(pytenki_init, '_tts_forecast_summary')
    pin = mock_factory.pin(2)

    pytenki_init.tts_forecast_summary_after_button_press()

    pin.drive_low()
    spy.assert_called_once()

    pin.drive_high()
    spy.assert_called_once()
