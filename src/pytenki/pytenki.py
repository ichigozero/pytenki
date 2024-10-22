import subprocess

from gpiozero import Button, LEDBoard
from gpiozero.exc import GPIOPinMissing, PinInvalidPin


DIC_FPATH = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
VOICE_FPATH = '/usr/share/hts-voice/mei/mei_normal.htsvoice'
SPEECH_FPATH = '/tmp/tts_ja_mei.wav'
FCAST_WEATHER = '{day}の{city}の天気は{weather}。'
FCAST_MAX_TEMP = '予想最高気温は{max_temp}。'
FCAST_MIN_TEMP = '予想最低気温は{min_temp}。'
FCAST_SUM_ERR = '天気予報を取得できません。'


def _exc_attr_err(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AttributeError:
            pass
    return wrapper


class PyTenki:
    def __init__(self, forecast=None,
                 led_pins=None, button_pin=None):
        self._forecast = forecast
        self._leds = None
        self._button = None

        self._normalize_weather_str()
        self.assign_leds(led_pins)
        self.assign_button(button_pin)

    @property
    def forecast(self):
        return self._forecast

    @forecast.setter
    def forecast(self, forecast):
        self._forecast = forecast
        self._normalize_weather_str()

    def _normalize_weather_str(self):
        try:
            strings = (('大', ''), ('暴風', ''),
                       ('雷', ''), ('一時', '時々'),
                       ('雨か雪', '雨'), ('雪か雨', '雪'))

            for before, after in strings:
                tmp = self._forecast['weather']
                self._forecast['weather'] = tmp.replace(before, after)
        except (AttributeError, TypeError):
            pass

    def _compose_forecast_summary(self):
        try:
            day = self._forecast.get('day')
            city = self._forecast.get('city')
            weather = self._forecast.get('weather')

            if all([day, city, weather]):
                fcast_weather = FCAST_WEATHER.format(
                    day=day, city=city, weather=weather)
                fcast_max_temp = ''
                fcast_min_temp = ''

                temps = self._forecast.get('temp')
                max_temp = temps.get('max')
                min_temp = temps.get('min')

                if max_temp:
                    fcast_max_temp = FCAST_MAX_TEMP.format(
                        max_temp=max_temp)

                if min_temp:
                    fcast_min_temp = FCAST_MIN_TEMP.format(
                        min_temp=min_temp)

                return ''.join([fcast_weather, fcast_max_temp,
                                fcast_min_temp])
        except AttributeError:
            pass

        return FCAST_SUM_ERR

    @_exc_attr_err
    def assign_leds(self, led_pins):
        self._close_leds()

        try:
            self._leds = LEDBoard(
                fine=led_pins.get('fine'),
                cloud=led_pins.get('cloud'),
                rain=led_pins.get('rain'),
                snow=led_pins.get('snow'),
                pwm=True,
            )
        except PinInvalidPin:
            pass

    @_exc_attr_err
    def _close_leds(self):
        self._leds.close()

    def assign_button(self, button_pin):
        try:
            self._close_button()
            self._button = Button(button_pin)
        except (GPIOPinMissing, PinInvalidPin):
            pass

    @_exc_attr_err
    def _close_button(self):
        self._button.close()

    @_exc_attr_err
    def tts_forecast_summary_after_button_press(self):
        self._button.when_pressed = self._tts_forecast_summary

    def _tts_forecast_summary(self):
        summary = self._compose_forecast_summary()

        try:
            p1 = subprocess.Popen(['echo', summary], stdout=subprocess.PIPE)
            p2 = subprocess.Popen([
                'open_jtalk',
                '-x', DIC_FPATH,
                '-m', VOICE_FPATH,
                '-ow', SPEECH_FPATH
            ], stdin=p1.stdout, stdout=subprocess.PIPE)

            p1.stdout.close()
            p2.communicate()
            p2.wait()

            subprocess.run(['aplay', '--quiet', SPEECH_FPATH])
            subprocess.run(['rm', '-f', SPEECH_FPATH])
        except OSError:
            pass

    def operate_all_weather_leds(self, on_time=1, off_time=1,
                                 fade_in_time=1, fade_out_time=1):
        self._operate_fine_led(on_time, off_time,
                               fade_in_time, fade_out_time)
        self._operate_cloud_led(on_time, off_time,
                                fade_in_time, fade_out_time)
        self._operate_rain_led(on_time, off_time,
                               fade_in_time, fade_out_time)
        self._operate_snow_led(on_time, off_time,
                               fade_in_time, fade_out_time)

    @_exc_attr_err
    def _operate_fine_led(self, on_time=1, off_time=1,
                          fade_in_time=1, fade_out_time=1):
        weather = self._forecast.get('weather')

        if weather.startswith('晴'):
            self._leds.fine.on()
        elif 'のち晴' in weather:
            self._leds.fine.pulse(fade_in_time, fade_out_time)
        elif '時々晴' in weather:
            self._leds.fine.blink(on_time, off_time)
        else:
            self._leds.fine.off()

    @_exc_attr_err
    def _operate_cloud_led(self, on_time=1, off_time=1,
                           fade_in_time=1, fade_out_time=1):
        weather = self._forecast.get('weather')

        if weather.startswith('曇'):
            self._leds.cloud.on()
        elif 'のち曇' in weather:
            self._leds.cloud.pulse(fade_in_time, fade_out_time)
        elif '時々曇' in weather:
            self._leds.cloud.blink(on_time, off_time)
        else:
            self._leds.cloud.off()

    @_exc_attr_err
    def _operate_rain_led(self, on_time=1, off_time=1,
                          fade_in_time=1, fade_out_time=1):
        weather = self._forecast.get('weather')

        if weather.startswith('雨'):
            self._leds.rain.on()
        elif 'のち雨' in weather:
            self._leds.rain.pulse(fade_in_time, fade_out_time)
        elif '時々雨' in weather:
            self._leds.rain.blink(on_time, off_time)
        else:
            self._leds.rain.off()

    @_exc_attr_err
    def _operate_snow_led(self, on_time=1, off_time=1,
                          fade_in_time=1, fade_out_time=1):
        weather = self._forecast.get('weather')

        if weather.startswith('雪'):
            self._leds.snow.on()
        elif 'のち雪' in weather:
            self._leds.snow.pulse(fade_in_time, fade_out_time)
        elif '時々雪' in weather:
            self._leds.snow.blink(on_time, off_time)
        else:
            self._leds.snow.off()
