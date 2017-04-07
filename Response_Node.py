class Response_Node:

	#input: response  - response String
	#       questions - list of strings representing questions that trigger this response
	#       neighbors - list of Response_Node. These are responses to questions that can follow this one
	#	    points    - number of points awarded when response is made

	def __init__(self, response = '', questions = [], neighbors = [], points = 0):
		self.response = response
		self.questions = questions
		self.neighbors = neighbors
		self.points = points


	#output: this response
	def get_response(self):
		return self.response

	#input: response - string
	def set_response(self, response):
		self.response = response


	#output: this questions
	def get_questions(self):
		return self.questions

	#input: new list of questions to trigger this response
	def set_questions(self, questions):
		self.questions = questions

	#input: question String
	def add_question(self, question):
		self.questions.append(question)	

	#input: index of question to be removed from questions
	def remove_question(self, index):
		del self.questions[index]


	#output: this neighbors
	def get_neighbors(self):
		return self.neighbors

	#input: list of neighbors
	def set_neighbors(self, neighbors):
		self.neighbors = neighbors

	#input: Response_Node to be a new neighbor to this
	def add_neighbor(self, neighbor):
		self.neighbors.append(neighbor)


	#input: index of Response_Node neighbor to remove from this.neighbors
	def remove_neighbor(self, index):
		del self.neighbors[index]



	#input: points int
	def set_points(self, points):
		self.points = points

	#output: this points
	def get_points(self):
		return self.points
		