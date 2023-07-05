import RPi.GPIO as GPIO
from time import sleep

def setup_motor(in1, in2, en):
	GPIO.setmode(GPIO.BCM)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(in1,GPIO.OUT)
	GPIO.setup(in2,GPIO.OUT)
	GPIO.setup(en,GPIO.OUT)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	pwm=GPIO.PWM(en,100)
	pwm.start(25)
	return pwm

def lumpy(val, pwm):
	for i in range(0, 1024, 200):
		if val > i - 50 and val < i + 50:
			if val > i + 3:
				GPIO.output(in1, GPIO.LOW)
				GPIO.output(in2, GPIO.HIGH)
				pwm.ChangeDutyCycle(50)
			elif val < i - 3:
				GPIO.output(in1, GPIO.HIGH)
				GPIO.output(in2, GPIO.LOW)
				pwm.ChangeDutyCycle(50)
			else:
				pwm.ChangeDutyCycle(0)

def slide_to_value(target, val, in1, in2, pwm):
	dif = abs(val - target)
	duration = 0.0001 * dif
	if(dif > 200):
		duration = 0.5
	if abs(val - target) > 20:
		if val > target:
			GPIO.output(in1, GPIO.LOW)
			GPIO.output(in2, GPIO.HIGH)
		else:
			GPIO.output(in1, GPIO.HIGH)
			GPIO.output(in2, GPIO.LOW)
		pwm.ChangeDutyCycle(max(min(dif/25, 25), 40))
		sleep(duration)
	GPIO.output(in1, GPIO.LOW)
	GPIO.output(in2, GPIO.LOW)
	pwm.ChangeDutyCycle(0)
	

	
if __name__ == "__main__":
	GPIO.setwarnings(False)
	in1 = 19
	in2 = 13
	en = 26
	pwm = setup_motor(19, 13, 26)
	slide_to_value(1000, 0, in1, in2, pwm)
	pwm.stop()
	GPIO.cleanup()
