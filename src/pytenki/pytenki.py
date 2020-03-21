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
                fine=led_pins.get('fine'),
                cloud=led_pins.get('cloud'),
                rain=led_pins.get('rain'),
                snow=led_pins.get('snow'),
                pwm=True,
            )
        except AttributeError:
            pass

    def _close_leds(self):
        try:
            self._leds.close()
        except AttributeError:
            pass

    def _operate_fine_led(self):
        try:
            weather = self.forecast.get('weather')

            if weather.startswith('晴'):
                self._leds.fine.on()
            elif 'のち晴' in weather:
                self._leds.fine.pulse()
            elif '時々晴' in weather:
                self._leds.fine.blink()
            else:
                self._leds.fine.off()
        except AttributeError:
            pass

    def _operate_cloud_led(self):
        try:
            weather = self.forecast.get('weather')

            if weather.startswith('曇'):
                self._leds.cloud.on()
            elif 'のち曇' in weather:
                self._leds.cloud.pulse()
            elif '時々曇' in weather:
                self._leds.cloud.blink()
            else:
                self._leds.cloud.off()
        except AttributeError:
            pass

    def _operate_rain_led(self):
        try:
            weather = self.forecast.get('weather')

            if weather.startswith('雨'):
                self._leds.rain.on()
            elif 'のち雨' in weather:
                self._leds.rain.pulse()
            elif '時々雨' in weather:
                self._leds.rain.blink()
            else:
                self._leds.rain.off()
        except AttributeError:
            pass
