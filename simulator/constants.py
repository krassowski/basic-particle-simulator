from vector import *

def hex_color_to_vector3(hex_color):
	out = Vector3()
	out.x = int(hex_color[1:3], base=16)
	out.y = int(hex_color[3:5], base=16)
	out.z = int(hex_color[5:], base=16)
	return out/255.0
	
class Constants():

	constants = {}

	def __getattr__(self, constant_name):
		if constant_name in self.constants:
			return self.constants[constant_name]
		else:
			raise KeyError("There is no constant >> " + constant_name + " <<")

	def __init__(self, path_to_file_with_constants=None):
		if path_to_file_with_constants:
			self.load_from_file(path_to_file_with_constants)

	def load_from_file(self, file_name):

		from ConfigParser import ConfigParser
		config = ConfigParser()
		config.read(file_name)

		for section in config.sections():

			if section == "colors":
				for name, value in config.items(section):
					self.add(name, hex_color_to_vector3(value))
			else:
				for name, value in config.items(section):
					# TODO - wywalic eval jakos inaczej liczby pobierac
					self.add(name, eval(value))

	def save_to_file(self):
		# TODO
		pass

	def get_all(self):
		return constants.keys()

	def add(self, name, value):
		self.constants[name] = value

