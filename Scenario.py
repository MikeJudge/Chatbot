from Dialog import Dialog

class Scenario:

	#input: name        - string of name of person in the scenario
	#       description - string respresenting description of the scenario
	#       image       - image of the person
	#       dialog      - Dialog object representing the dialog in the conversation

	def __init__(self, name="", description="", image="", dialog = Dialog()):
		self.name = name
		self.description = description
		self.image = image
		self.dialog = dialog


	#input: name - string name
	def set_name(self, name):
		self.name = name

	#output: string name
	def get_name(self):
		return self.name


	#input: description - string
	def set_description(self, description):
		self.description = description

	#output: string description
	def get_description(self):
		return self.description


	#input: image - image object
	def set_image(self, image):
		self.image = image

	#output: image object
	def get_image(self):
		return self.image

	#input: dialog - Dialog object
	def set_dialog(self, dialog):
		self.dialog = dialog

	#output - Dialog object
	def get_dialog(self):
		return self.dialog


