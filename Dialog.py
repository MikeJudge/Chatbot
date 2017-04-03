class Dialog:

	#input: responses - set of Response_Node
	def __init__(self, responses):
		self.responses = responses
		self.total_points = 0
		self.set_total_points()


	#calculates the total possible points in this dialog
	def set_total_points(self):
		self.total_points = 0
		for response in self.responses:
			self.total_points += response.get_points()

	#output: this total_points int
	def get_total_points(self):
		return self.total_points


	#output: set of Response_Node in this
	def get_responses(self):
		return self.responses

	#input: set of Response_Node to represent this dialog
	def set_responses(self, responses):
		self.responses = responses
		self.set_total_points() #update total points

	#input: Response_Node to add to the response set
	def add_response(self, response):
		self.responses.add(response)
		self.set_total_points() #update total points

	#input: Response_Node to remove from the reponse set
	def remove_response(self, response):
		self.responses.remove(response)
		self.set_total_points() #update total points


		