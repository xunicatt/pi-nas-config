import RPi.GPIO as GPIO
from time import sleep
from subprocess import Popen, PIPE

class fan_control:
    __max_temp = 70
    __min_temp = 40

    def __init__(self, fan_pin: int, freq: int):
        self.fan_pin = fan_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.fan_pin, freq)
        self.pwm.start(0)

    def __measure_temp(self) -> int:
        p = Popen(["vcgencmd", "measure_temp"], stdout=PIPE, text=True)
        out, _ = p.communicate()
        out = out.replace("temp=", "").replace("'C\n", "")
        return int(float(out))

    def __get_duty_cycle(self) -> int:
        temp = self.__measure_temp()
        if temp < self.__min_temp:
            return 0

        duty_cycle = (temp - self.__min_temp)*(100/(self.__max_temp - self.__min_temp))
        return int(duty_cycle)

    def start(self):
        real_pwm = lambda x: 100 - x
        try:
            while True:
                duty_cycle = self.__get_duty_cycle()
                self.pwm.ChangeDutyCycle(real_pwm(duty_cycle))
                sleep(5)
                pass
        except KeyboardInterrupt:
            self.pwm.stop()
            GPIO.cleanup()

if __name__ == "__main__":
    fc = fan_control(13, 100)
    fc.start()

