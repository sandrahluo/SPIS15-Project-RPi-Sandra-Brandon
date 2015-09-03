import RPi.GPIO as GPIO, sys, threading, time
GPIO.setwarnings(False)
#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#use pwm on inputs so motors don't go too fast
GPIO.setup(19, GPIO.OUT)
p=GPIO.PWM(19, 20)
p.start(0)
GPIO.setup(21, GPIO.OUT)
q=GPIO.PWM(21, 20)
q.start(0)
GPIO.setup(24, GPIO.OUT)
a=GPIO.PWM(24,20)
a.start(0)
GPIO.setup(26, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

# Setup LED pins as outputs
LED1 = 13
LED2 = 12
LED3 = 11
LED4 = 07
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

# Define Sonar Pin for Trigger and Echo to be the same
sonar_L = 8
sonarR_trigger =18
sonarR_echo = 22

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

def leftSonar():
  GPIO.setup(sonar_L, GPIO.OUT)
  GPIO.output(sonar_L, True)
  time.sleep(0.00001)
       	#sends out signal w/ TRIGGER?
  GPIO.output(sonar_L, False)
       	#ends signal
  start = time.time()
  count = time.time()
  GPIO.setup(sonar_L, GPIO.IN)
       	#receives input through ECHO?
  while GPIO.input(sonar_L)==0 and time.time()-count<0.1:
    start = time.time()
  stop=time.time()
  while GPIO.input(sonar_L)==1:
    stop = time.time()
       	# Calculate pulse length
  elapsed = stop-start
       	# Distance pulse travelled in that time is time
       	# multiplied by the speed of sound (cm/s)
  distanceL = elapsed * 34000
       	# That was the distance there and back so halve the value
  distanceL = distanceL / 2
##  print 'Distance_L:', distanceL
##  time.sleep(.75)
  return distanceL
  

def rightSonar():
  GPIO.setup(sonarR_trigger, GPIO.OUT)
  GPIO.output(sonarR_trigger, True)
  time.sleep(0.0001)
  GPIO.output(sonarR_trigger, False)
  start = time.time()
  count = time.time()
  GPIO.setup(sonarR_echo, GPIO.IN)
  while GPIO.input(sonarR_echo) == 0 and time.time()-count<0.1:
    start = time.time()
  stop = time.time()
  while GPIO.input(sonarR_echo) == 1:
    stop = time.time()
  elapsed = stop-start
  distanceR = elapsed * 34000
  distanceR = distanceR / 2
##  print 'Distance_R:', distanceR
##  time.sleep(.75)
  return distanceR

speed = 25
fastspeed = 100
turnspeed = 15
spinspeed = 15

def forwards(speed):
  p.ChangeDutyCycle(speed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(speed)
  b.ChangeDutyCycle(0)
  setLEDs(0, 0, 0, 0)
  #LEDs are reverse logic
  
def reverse(speed):
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(speed)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(speed)
  setLEDs(0, 1, 0, 1)
  time.sleep(0.3)
  setLEDs(1, 0, 1, 0)

def turnleft():
  p.ChangeDutyCycle(turnspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(turnspeed)
  setLEDs(0, 0, 1, 1)

def turnright():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(turnspeed)
  a.ChangeDutyCycle(turnspeed)
  b.ChangeDutyCycle(0)
  setLEDs(1, 1, 0, 0)

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  setLEDs(1, 1, 1, 1)


def bullFollow(distanceL, distanceR):
  if min((int(distanceL)/2), 50) == (int(distanceL)/2):
    speed = max(20, (int(distanceL)/2))
  else:
    speed = 50
  if distanceL >10 and distanceL < 20 and distanceR > 10 and distanceR < 20:
    stopall()
    time.sleep(.3)
  elif distanceL < 10 and distanceR < 10:
    reverse(speed)
    time.sleep(.3)
  elif distanceL > 20 and distanceL < 30 and distanceR > 20 and distanceR < 30:
    forwards(speed)
    time.sleep(.3)
  elif distanceL <30 and distanceR > 50:
    turnleft()
    time.sleep(0.5)
  elif distanceR < 30 and distanceL > 50:
    turnright()
    time.sleep(0.5)
    
def sprint():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(fastspeed)
  b.ChangeDutyCycle(0)
  setLEDs(0, 0, 0, 0)
  time.sleep(.3)
  setLEDs(1,1,1,1)

def spin180():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(spinspeed)
  a.ChangeDutyCycle(spinspeed)
  b.ChangeDutyCycle(0)
  setLEDs(0, 1, 1, 1)
  time.sleep(0.2)
  setLEDs(1, 0, 1, 1)
  time.sleep(0.2)
  setLEDs(1, 1, 0, 1)
  time.sleep(0.2)
  setLEDs(1, 1, 1, 0)
  time.sleep(0.2)
  setLEDs(1, 1, 1, 1)
#  time.sleep(0.2)
#  setLEDs(1, 0, 1, 1)
 # time.sleep(0.2)
 # setLEDs(1, 1, 0, 1)
following = 0
sprinting = 1
stopping = 2
 
# main loop
try:
    mode = following
        #starts out in following mode
    while True:
      distanceR = rightSonar()
      time.sleep(0.05)
      distanceL = leftSonar()
        #continuously measuring distance w/sonar
      if distanceL > 40 and distanceR >40 and mode != stopping:
        mode = sprinting
        sprint()
      elif mode == sprinting:
        stopall()
        spin180()
        time.sleep(.6)
        stopall()
        mode = stopping
        #when mode is sprinting but both distanceL and distanceR are greater than 40
	#will stop and go into stopping mode until reactivated when it detects distances < 40
      elif distanceL < 40 or distanceR < 40:
        mode = following
        bullFollow(distanceL, distanceR)       
        
except KeyboardInterrupt:
  setLEDs(1, 1, 1, 1)
  GPIO.cleanup()
  sys.exit()
