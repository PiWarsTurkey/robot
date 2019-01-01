from piwarsturkey_robot import *
import time
ultrasonic = Ultrasonic(21, 20)
old_speed = 0
while True:
  distance = ultrasonic.getDistance()
  if distance <= 1.5:
    setSpeeds(100,100)
    time.sleep(0.1)
    setSpeeds(0,0)
    break
  
  new_speed = 8*distance*distance
  if new_speed - old_speed > 5:
    setSpeeds(new_speed, new_speed)
    time.sleep(0.05)
    print(distance)

