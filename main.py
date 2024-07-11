from neopixel import Neopixel
import time, random
from machine import Pin, ADC

# A color is a triple (G, R, B), defined in the usual manner.
OFF = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (255, 0, 0)
RED = (0, 255, 0)

# Hard-coded constants depend on hardware configuration and heuristics.
NUM_PIXELS = 32
NEOPIXEL_PIN = 15
SENSOR_PIN = 28
SENSOR_ACTIVATION_HEURISTIC = 50

# Set up neopixel object. Brightness is set to 10 for ease of use,
# by default 150 is used to be able to be seen through the board,
# but too bright to comfortably work with.
pixels = Neopixel(NUM_PIXELS, 0, NEOPIXEL_PIN)
pixels.brightness(10)
pixels.fill(OFF)
pixels.show()

# Set up distance sensor.
sensor = machine.ADC(SENSOR_PIN)

def main():
    # Read from sensor, run the routine if above heuristic value of 50.
    while True:
        analog_value = sensor.read_u16() // 300
        time.sleep_ms(100) # wait for sensor reading to complete
        
        if analog_value > SENSOR_ACTIVATION_HEURISTIC:
            # Randomly finds a pixel to turn off, waits, and then repeats.
            for i in range(30):
                rand_pixel = random.randint(0, NUM_PIXELS - 1)
                pixels.set_pixel(rand_pixel, OFF)
                pixels.show()
                time.sleep_ms(200)
                pixels.fill(WHITE)
                pixels.show()

            # Blank out pixels at the end, for testing purposes only.
            pixels.fill(OFF)
            pixels.show()
            
if __name__ == "__main__":
    main()

# EOF
