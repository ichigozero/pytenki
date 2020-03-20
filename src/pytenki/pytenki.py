from gpiozero import LEDBoard


class PyTenki:
    def __init__(self, led_pins=None):
        self._leds = None

        self.assign_leds(led_pins)

    def assign_leds(self, led_pins):
        try:
            self._close_leds()

            self._leds = LEDBoard(
                fine=led_pins['fine'],
                cloud=led_pins['cloud'],
                rain=led_pins['rain'],
                snow=led_pins['snow'],
                pwm=True,
            )
        except TypeError:
            pass

    def _close_leds(self):
        try:
            self._leds.close()
        except AttributeError:
            pass
