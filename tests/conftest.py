import pytest
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin

from pytenki import PyTenki


@pytest.yield_fixture
def mock_factory(request):
    save_factory = Device.pin_factory
    Device.pin_factory = MockFactory()
    yield Device.pin_factory

    if Device.pin_factory is not None:
        Device.pin_factory.reset()
    Device.pin_factory = save_factory


@pytest.fixture
def pwm(request, mock_factory):
    mock_factory.pin_class = MockPWMPin


@pytest.fixture(scope='module')
def led_pins():
    return {
        'fine': 4,
        'cloud': 17,
        'rain': 27,
        'snow': 22,
    }


@pytest.fixture
def pytenki(mock_factory, pwm):
    return PyTenki()


@pytest.fixture
def pytenki_init(mock_factory, pwm, led_pins):
    return PyTenki(led_pins)
