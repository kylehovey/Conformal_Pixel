#############################################################################
## Conformal Mapping Script						    #
## Author: Kyle Hovey							    #
## Feel free to modify this to your liking, but give credit where it is due #
#############################################################################

## Import neccessary libraries
from PIL import Image
import cmath
from math import floor

## Create a new PIL image object from a file path
def new_source(path):
	return Image.open(path)

## Generate a blank PIL image object given pixel width and height
def generate_output(w, h):
	return Image.new("RGB", (w, h), "white")

## Save a source PIL image object with the given name in the cwd
def save_output(source, name, ext="PNG"):
	im.save(str(name), ext)	

## Create a function that tiles an image to infinity
def create_map_bag(source):
	pixelMap = source.load()
	width = source.size[0]
	height = source.size[1]
	origin_x = floor(width/2)
	origin_y = floor(height/2)
	return lambda u, v: pixelMap[(u + origin_x) % width, (v + origin_y) % height]

## Create PIL-to-complex-cartesian transform given the image parameters
def gen_transform(origin_x, shift_x, origin_y, shift_y):
	return lambda u, v: complex((u - origin_x + shift_x) + (v - origin_y + shift_y)*1j)
 
## Class for creating conformal map images
class Conformal(object):
	def __init__(self, width, height, source_path):
		self.shift = [0, 0]
		self.offset = [0, 0]
		self.width = width
		self.height = height
		self.update_transform()
		self.img = generate_output(width, height)
		source = new_source(source_path)
		self.grab_pixel = create_map_bag(source)
		self.func = lambda x: x
	def update_transform(self):
		self.trans = gen_transform(self.width/2, self.shift[0], self.height/2, self.shift[1])
	def add_shift(self, x, y):
		self.shift[0] += x
		self.shift[1] += y
		self.update_transform()
	def abs_shift(self, x, y):
		self.shift = [x, y]
		self.update_transform()
	def add_offset(self, x, y):
		self.offset[0] += x
		self.offset[1] += y
	def abs_offset(self, x, y):
		self.offset = [x, y]
	def set_func(self, func):
		self.func = func
	def set_scale(self, scale):
		self.scale = scale
	def render(self):
		to_pixels = self.img.load()
		for u in range(self.width):
			for v in range(self.height):
				z = self.func(self.trans(u, v))
				to_pixels[u, v] = self.grab_pixel((round(z.real) + self.offset[0])/self.scale, (round(z.imag) + self.offset[1])/self.scale)
	def show(self):
		self.img.show()
	def save(self, name="conformal_output"):
		self.img.save(str(name) + ".png", "PNG")

if __name__ == "__main__":
    ## Create the map object
    cfr = Conformal(1920, 1080, "./tile.png")
    
    ## Set the scale of the incoming source image
    cfr.set_scale(1)
    
    ## Some functions (inverse of whatever you set is shown)
    tan = lambda z: 300*cmath.atan((z)/350 + .000000001)
    tanh = lambda z: 300*cmath.atanh((z)/1000 + .000000001)

    # Set function
    cfr.set_func(lambda z: tan(z) + tanh(z))

    # Create the map
    cfr.render()
    cfr.save("Warped_Forest")
