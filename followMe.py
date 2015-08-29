import RPi.GPIO as GPIO, sys, threading, time
GPIO.setwarnings(False)
#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)

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
LED1 = 07
LED2 = 11
LED3 = 12
LED4 = 13
GPIO.setup(LED1, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

# Setup LED pins as outputs
LED1 = 07
LED2 = 11
LED3 = 12
LED4 = 13
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

setLEDs(1, 1, 1, 1)

# Define Sonar Pin for Trigger and Echo to be the same
sonar_L = 8
sonarR_trigger =18
sonarR_echo = 22

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
  distance = elapsed * 34000
       	# That was the distance there and back so halve the value
  distance = distance / 2
  print 'Distance_L:', distance
  time.sleep(1)
  return distance
  

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
  distance = elapsed * 34000
  distance = distance / 2
  print 'Distance_R:', distance
  time.sleep(1)
  return distance
		

try:
  while True:
    leftSonar() and rightSonar()
except KeyboardInterrupt:
  GPIO.cleanup()
  sys.exit()

# Pizazz Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# Also demonstrates writing to the LEDs
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTest.py


import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#use pwm on inputs so motors don't go too fast
# Pins 19, 21 Right Motor
# Pins 24, 26 Left Motor
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

slowspeed = 25
fastspeed = 100
turnspeed = 15
LED1 = 22
LED2 = 18
LED3 = 11
LED4 = 07
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

def forwards():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(fastspeed)
  b.ChangeDutyCycle(0)
  setLEDs(1, 0, 0, 1)
  print('straight')

def reverse():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  setLEDs(0, 1, 1, 0)
  print('straight')

def turnleft():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(slowspeed)
  b.ChangeDutyCycle(0)
  setLEDs(0, 0, 1, 1)
  print('left')

def turnright():
  p.ChangeDutyCycle(slowspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(fastspeed)
  b.ChangeDutyCycle(0)
  setLEDs(1, 1, 0, 0)
  print('right')

def sharpright():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(slowspeed)
  a.ChangeDutyCycle(turnspeed)
  b.ChangeDutyCycle(0)
  setLEDs(1,1,0,0)
  print('sharp right')

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  setLEDs(1, 1, 1, 1)
  print('stop')

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

setLEDs(1, 1, 1, 1) # switch all LEDs off

# main loop
#try:
    #while True:
     # forwards()
     # time.sleep(1)
     # sharpright()
     # time.sleep(1)
     # forwards()
     # time.sleep(1)
     # sharpright()
     # time.sleep(1)
     # forwards()
     # time.sleep(1)
     # sharpright()
     # time.sleep(1)
     # forwards()
     # time.sleep(1)
     # sharpright()
     # time.sleep(1)
     # stopall()
     # GPIO.cleanup()

#except KeyboardInterrupt:
       #Going = False
       #GPIO.cleanup()
       #sys.exit()
