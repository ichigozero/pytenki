from gpiozero import LEDBoard


class PyTenki:
    def __init__(self, forecast=None, led_pins=None):
        self._forecast = forecast
        self._leds = None

        self._normalize_weather_str()
        self.assign_leds(led_pins)

    @property
    def forecast(self):
        return self._forecast

    @forecast.setter
    def forecast(self, forecast):
        self._forecast = forecast
        self._normalize_weather_str()

    def _normalize_weather_str(self):
        try:
            strings = (('大', ''), ('暴風', ''), ('雷', ''),
                       ('一時', '時々'), ('雨か雪', '雨'),
                       ('雪か雨', '雪'))

            for before, after in strings:
                tmp = self._forecast['weather']
                self._forecast['weather'] = tmp.replace(before, after)
        except (AttributeError, TypeError):
            pass

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
