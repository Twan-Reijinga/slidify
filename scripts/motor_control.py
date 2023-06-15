import RPi.GPIO as GPIO          
from time import sleep

setup_motor(in1, in2, en):
	GPIO.setmode(GPIO.BCM)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(in1,GPIO.OUT)
	GPIO.setup(in2,GPIO.OUT)
	GPIO.setup(en,GPIO.OUT)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	PWM=GPIO.PWM(en,1000)
	PWM.start(25)

def lumpy(val):
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

def slide_to_value(target, val):
    if abs(val - targetValue) > 20:
        if val > targetValue:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
        else:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        pwm.ChangeDutyCycle(max(min(abs(val - targetValue), 255), 200))
    else:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        pwm.ChangeDutyCycle(0)

	
if __name__ == "__main__":
	setup_motor(19, 13, 26)
	lumpy(0)
