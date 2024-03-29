import RPi.GPIO as GPIO
from time import sleep

def setup_MCP3008(clk, dout, din, cs):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clk, GPIO.OUT)
	GPIO.setup(dout, GPIO.IN)
	GPIO.setup(din, GPIO.OUT)
	GPIO.setup(cs, GPIO.OUT)

def	get_analog_value(channel, clk, dout, din, cs):
	# Send start bit
	GPIO.output(cs, GPIO.HIGH)
	GPIO.output(clk, GPIO.LOW)
	GPIO.output(cs, GPIO.LOW)
	
	# Send command (start bit, single-ended, channel selection)
	command = channel
	command |= 0x18	 # 0x18: Start bit + single-ended bit
	command <<= 3    # Move to the next bit position
	for _ in range(5):
		if command & 0x80:
			GPIO.output(din, GPIO.HIGH)
		else:
			GPIO.output(din, GPIO.LOW)
		command <<= 1
		GPIO.output(clk, GPIO.HIGH)
		GPIO.output(clk, GPIO.LOW)

	# Read data
	adc_value = 0
	for _ in range(12):
		GPIO.output(clk, GPIO.HIGH)
		GPIO.output(clk, GPIO.LOW)
		adc_value <<= 1
		if GPIO.input(dout):
			adc_value |= 0x01
	GPIO.output(cs, GPIO.HIGH)
	return adc_value

if __name__ == "__main__":
	clk = 12
	dout = 16
	din = 20
	cs = 21
	channel = 0
	
	setup_MCP3008(clk, dout, din, cs)
	while True:
		value = get_analog_value(channel, clk, dout, din, cs)
		print(f"ADC Value (Channel {channel}): {value}")
		sleep(1)
