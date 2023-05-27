import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

# Define GPIO pins
CLK = 12
DOUT = 16
DIN = 20
CS = 21

# Set GPIO direction
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

def read_adc(channel):
    # Send start bit
    GPIO.output(CS, GPIO.HIGH)
    GPIO.output(CLK, GPIO.LOW)
    GPIO.output(CS, GPIO.LOW)

    # Send command (start bit, single-ended, channel selection)
    command = channel
    command |= 0x18  # 0x18: Start bit + single-ended bit
    command <<= 3    # Move to the next bit position
    for _ in range(5):
        if command & 0x80:
            GPIO.output(DIN, GPIO.HIGH)
        else:
            GPIO.output(DIN, GPIO.LOW)
        command <<= 1
        GPIO.output(CLK, GPIO.HIGH)
        GPIO.output(CLK, GPIO.LOW)

    # Read data
    adc_value = 0
    for _ in range(12):
        GPIO.output(CLK, GPIO.HIGH)
        GPIO.output(CLK, GPIO.LOW)
        adc_value <<= 1
        if GPIO.input(DOUT):
            adc_value |= 0x01

    # Set CS high to end conversion
    GPIO.output(CS, GPIO.HIGH)

    return adc_value

# Usage example
while True:
    channel = 0  # Channel 0 on MCP3008
    value = read_adc(channel)
    print(f"ADC Value (Channel {channel}): {value}")
    sleep(1)

# Clean up GPIO
GPIO.cleanup()

