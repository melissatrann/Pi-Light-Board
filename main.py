from neopixel import Neopixel
import time, random
from machine import Pin, ADC
from collections import deque

# A color is a triple (G, R, B), defined in the usual manner.
OFF = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (255, 0, 0)
RED = (0, 255, 0)
BLUE = (0, 0, 255)

# Hard-coded constants depend on hardware configuration and heuristics.
NUM_PIXELS = 32
NEOPIXEL_PIN = 15
SENSOR_PIN = 28
SENSOR_ACTIVATION_HEURISTIC = 50
SMOOTHING_WINDOW_SIZE = 20


# Set up neopixel object. Brightness is set to 10 for ease of use,
# by default 150 is used to be able to be seen through the board,
# but too bright to comfortably work with.
pixels = Neopixel(NUM_PIXELS, 0, NEOPIXEL_PIN)
pixels.brightness(10)
pixels.fill(OFF)
pixels.show()



# Set up distance sensor.
sensor = machine.ADC(SENSOR_PIN)
## method to set all pixels to a certain color
np = Neopixel(NUM_PIXELS, NEOPIXEL_PIN)

def set_all_pixels(color):
    for i in range(NUM_PIXELS):
        np[i] = color
    np.show()

#Creates pulsing light effect by gradually increasing and decreasing the brightness of specified color
# Loops through range of of brightness scaling GRB components

def gradient_effect(color, steps=50, delay=20):
    # Increasing brightness
    for i in range(steps):
        brightness = i / steps
        scaled_color = tuple(int(brightness * c) for c in color)
        set_all_pixels(scaled_color)
        time.sleep_ms(delay)
    # Decreasing brightness
    for i in range(steps):
        brightness = (steps - i) / steps
        scaled_color = tuple(int(brightness * c) for c in color)
        set_all_pixels(scaled_color)
        time.sleep_ms(delay)

def main():
    # Buffer is used to store recent numbers, computes a moving average
    # to smooth out noisy data from the sensor stream.
    buffer = deque((), SMOOTHING_WINDOW_SIZE)

    
    # Read from sensor, run the routine if above heuristic value of 50.
    while True:
        analog_value = sensor.read_u16() // 300
        buffer.append(analog_value)
        total_sum = 0
        for _ in range(SMOOTHING_WINDOW_SIZE):
            val = buffer.popleft()
            total_sum += val
            buffer.append(val)
        
        smooth_value = total_sum / SMOOTHING_WINDOW_SIZE
        print(smooth_value)
        
        if smooth_value > SENSOR_ACTIVATION_HEURISTIC:
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
            # Test out gradient effect 
            gradient_effect(GREEN)
            
if __name__ == "__main__":
    main()

# EOF
