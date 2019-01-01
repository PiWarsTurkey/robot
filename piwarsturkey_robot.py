from pololu_drv8835_rpi import motors, MAX_SPEED
from time import sleep, time
import RPi.GPIO as GPIO
import atexit

GPIO_SETUP = False

GPIO.setmode(GPIO.BCM)

current_speeds = (0, 0)
max_step = 50
class Servo:
  def __init__(self, pin):
    GPIO_SETUP = True
    GPIO.setup(pin, GPIO.OUT)
    self.pwm = GPIO.PWM(pin, 50)
    self.pwm.start(0)
    self.pin = pin

  def setAngle(self, angle):
    duty = angle / 18 + 2
    GPIO.output(self.pin, True)
    self.pwm.ChangeDutyCycle(duty)
    sleep(0.2)
    GPIO.output(self.pin, False)
    pwm.ChangeDutyCycle(0)

class Ultrasonic:
  def __init__(self, echo, trig):
    GPIO_SETUP = True

    self.echo = echo
    self.trig = trig
    
    GPIO.setup(trig,GPIO.OUT)
    GPIO.setup(echo,GPIO.IN)

    GPIO.output(trig, False)
    
  def getDistance(self):
    GPIO.output(self.trig, True)
    sleep(0.00001)
    GPIO.output(self.trig, False)

    while not GPIO.input(self.echo):
      pulse_start = time()
      sleep(0.0000001)

    while GPIO.input(self.echo):
      pulse_end = time()
      sleep(0.0000001)

    duration = pulse_end - pulse_start
    return duration*17150

def setSpeeds(left, right):
  left = int(left)
  right = int(right)

  if left > 480: left = 480
  if left < -480: left = -480
  if right > 480: right = 480
  if right < -480: right = -480
  print("setting left: {0}, right: {1}".format(left, right))
  left_dif = left - current_speeds[0]
  right_dif = right - current_speeds[1]
  max_dif = max(abs(left_dif), abs(right_dif))

  num_intervals = max_dif / max_step
  
  for i in range(num_intervals):
    cLeft = current_speeds[0] + left_dif / num_intervals
    cRight = current_speeds[1] + right_dif / num_intervals
    motors.setSpeeds(cLeft, cRight)
    sleep(0.001)
  motors.setSpeeds(left, right)

def cleanup():
  setSpeeds(0,0)
  if GPIO_SETUP: GPIO.cleanup()

atexit.register(cleanup)
