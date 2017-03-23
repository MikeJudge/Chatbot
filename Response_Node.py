class Response_Node:

	#input: response  - response String
	#       questions - set of strings representing questions that trigger this response
	#       neighbors - set of Response_Node. These are responses to questions that can follow this one

	def __init__(self, response, questions, neighbors):
		self.response = response
		self.questions = questions
		self.neighbors = neighbors


	#output: this response
	def get_response(self):
		return self.response

	#input: response - string
	def set_response(self, response):
		self.response = response


	#output: this questions
	def get_questions(self):
		return self.questions

	#input: new set of questions to trigger this response
	def set_questions(self, questions):
		self.questions = questions

	#input: question String
	def add_question(self, question):
		self.questions.add(question)	

	#input: String of question to be removed from questions
	def remove_question(self, question):
		self.questions.remove(question)

	#output: this neighbors
	def get_neighbors(self):
		return self.neighbors

	#input: set of neighbors to add to list
	def set_neighbors(self, neighbors):
		self.neighbors = neighbors

	#input: Response_Node to be a new neighbor to this
	def add_neighbor(self, neighbor):
		self.neighbors.add(neighbor)


	#input: Response_Node neighbor to remove from this.neighbors
	def remove_neighbor(self, neighbor):
		self.neighbors.remove(neighbor)
		