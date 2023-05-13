from RPi import GPIO
from time import sleep

def setup_rotary_encoder(clk, dt, sw):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def get_rotary_encoder_change():
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
		counter += get_rotary_encoder_change()
		print(counter)
		sleep(0.01)
