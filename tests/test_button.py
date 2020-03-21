def test_assign_button(pytenki):
    assert pytenki._button is None
    pytenki.assign_button(2)
    assert pytenki._button is not None


def test_close_button_before_reassignment(mocker, pytenki_init, button_pin):
    spy = mocker.spy(pytenki_init._button, 'close')
    pytenki_init.assign_button(button_pin)
    spy.assert_called_once()
