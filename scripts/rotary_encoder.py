from RPi import GPIO
from time import sleep

def setup_rotary_encoder(clk, dt, sw):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def handle_rotary_encoder_change(clk, dt, exec_function, os, ssh, volumeStep, canvas, volumeText):
	GPIO.remove_event_detect(clk)
	clkState = GPIO.input(clk)
	dtState = GPIO.input(dt)
	if clkState == dtState:
		exec_function(os, ssh, volumeStep, canvas, volumeText)
	else:
		exec_function(os, ssh, -volumeStep, canvas, volumeText)
	sleep(0.4)
	GPIO.add_event_detect(
		clk, 
		GPIO.BOTH, 
		callback=lambda x: handle_rotary_encoder_change(clk, dt, exec_function, os, ssh, volumeStep, canvas, volumeText), 
		bouncetime=20
	)

def get_rotary_encoder_change(clk, dt):
	clkLastState = GPIO.input(clk) 
	update = False
	while not update:
		clkState = GPIO.input(clk)
		dtState = GPIO.input(dt)
		if clkState != clkLastState:
			update = True
			if dtState != clkState:
				return 1
			else:
				return -1

if __name__ == "__main__":
	clk = 17
	dt = 18
	sw = 27
	counter = 0
	while True:
		counter += get_rotary_encoder_change(clk, dt)
		print(counter)
		sleep(0.01)

