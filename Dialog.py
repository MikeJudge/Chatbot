class Dialog:

	#input: responses - set of Response_Node
	def __init__(self, responses):
		self.responses = responses


	#output: set of responses in this
	def get_responses(self):
		return self.responses

	#input: set of responses to represent this dialog
	def set_responses(self, responses):
		self.responses = responses

	#input: Response_Node to add to the response set
	def add_response(self, response):
		self.responses.add(response)

	#input: Response_Node to remove from the reponse set
	def remove_response(self, response):
		self.responses.remove(response)


		