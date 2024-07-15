from neopixel import Neopixel
import time, random, gc
from machine import Pin, ADC
from buffer import FixedLengthBuffer

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
SENSOR_ACTIVATION_HEURISTIC = 30
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
segments = {}

def define_segment(name, start, end):
    """
    Defines a segment of the neopixel light
    
    Parameters:
    :name: The name of the segment.
    :start: The starting index of the segment (inclusive).
    :end: The ending index of the segment (inclusive).
    
    Example:
    To define the first half of a 16-pixel strip:
    define_segment("left_half", 0, 7)
    To define the second half of a 16-pixel strip:
    define_segment("right_half", 8, 15)
    """
    if 0 <= start <= end < NUM_PIXELS:
        segments[name] = (start, end)
        
def set_segment_color(name, color):
    """
    Sets the color of a defined segment.
    
    Parameters:
    :name: The name of the segment.
    :color: The GRB color tuple (G, R, B).
    
    Example:
    set_segment_color("left_half", (0, 255, 0))  # Sets left half to red
    """
    if name in segments:
        start, end = segments[name]
        for i in range(start, end + 1):
            pixels.set_pixel(i, color)
        pixels.show()

def main():
    # Enable automatic garbage collection.
    gc.enable()

    # Buffer is used to store recent numbers, computes a moving average
    # to smooth out noisy data from the sensor stream.
    buf = FixedLengthBuffer(SMOOTHING_WINDOW_SIZE)

    # Define segments 
    define_segment("left_half", 0, 7)  # First half of the 16-pixel strip
    define_segment("right_half", 8, 15)  # Second half of the 16-pixel strip

    # Read from sensor, run the routine if above a heuristically chosen value.
    while True:
        analog_value = sensor.read_u16() // 257
        buf.append(analog_value)  
        smooth_value = sum(buf) / len(buf)
        time.sleep_ms(10)
        
        if smooth_value > SENSOR_ACTIVATION_HEURISTIC:
            # Randomly finds a pixel to turn off, waits, and then repeats.
            for i in range(30):
                rand_pixel = random.randint(0, NUM_PIXELS - 1)
                pixels.set_pixel(rand_pixel, OFF)
                pixels.show()
                time.sleep_ms(200)
                pixels.fill(WHITE)
                pixels.show()
                
            # To prevent the moving average from staying high for too long
            # causing multiple detections when there should only be one.
            buf.clear()

            # Blank out pixels at the end, for testing purposes only.
            pixels.fill(OFF)
            pixels.show()
            
            # Test Apply effects to segments
            set_segment_color("left_half", BLUE)  # Set left half to blue
            set_segment_color("right_half", RED)  # Set right half to red
            
if __name__ == "__main__":
    main()

# EOF
