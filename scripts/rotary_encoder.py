from RPi import GPIO
from time import sleep

clk = 17
dt = 18
sw = 27

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

def switch_callback(channel):
        print('switch clicked!')

GPIO.add_event_detect(sw, GPIO.FALLING, callback=switch_callback, bouncetime=200)

if __name__ == "__main__":
        counter = 0
        while True:
                counter += get_rotary_encoder_change()
                print(counter)
                sleep(0.01)

