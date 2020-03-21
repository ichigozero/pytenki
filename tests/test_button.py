def test_assign_button(pytenki):
    assert pytenki._button is None
    pytenki.assign_button(2)
    assert pytenki._button is not None
