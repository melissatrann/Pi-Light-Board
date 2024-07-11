class Pixel():
    def __init__(self, grb, how_bright):
        self.color = grb
        self.brightness = how_bright

    def set_brightness(self, value):
        self.brightness = value

    def set_color(self, grb):
        self.color = grb

    def __repr__(self):
        return f"({self.color}, {self.brightness})"  
        
class PixelArray():
    def __init__(self, num_pixels):
        self.num_pixels = num_pixels
        self.pixels = [Pixel((255, 255, 255), 1.0) for _ in range(num_pixels)]
        
    def set_pixel(self, index, grb, brightness=1.0):
        if 0 <= index < self.num_pixels:
            self.pixels[index].set_color(grb)
            self.pixels[index].set_brightness(brightness)

    def fill(self, grb):
        list(map(lambda c: c.set_color(grb), self.pixels))

    def __repr__(self):
        return str(self.pixels)
