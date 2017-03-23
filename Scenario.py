

class Scenario:

	def __init__(self, name, description, image, dialog):
		self.name = name
		self.description = description
		self.image = image
		self.dialog = dialog


	def set_name(self, name):
		self.name = name


	def get_name(self):
		return self.name

	def set_description(self, description):
		self.description = description


	def get_description(self):
		return self.description

	def set_image(self, image):
		self.image = image

	def get_image(self):
		return self.image


	def set_dialog(self, dialog):
		self.dialog = dialog

	def get_dialog(self):
		return self.dialog

