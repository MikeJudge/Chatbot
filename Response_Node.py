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

	#input: index of question in list
	#       question string to be placed at index in list
	def set_question(self, index, question):
		self.questions[index] = question

	#input:  index of question in list
	#output: question at index in question list, or None if index is out of bounds
	def get_question(self, index):
		if index < 0 or index >= len(self.questions):
			return None
		return self.questions[index]


	#output: this neighbors
	def get_neighbors(self):
		return self.neighbors

	#input: list of neighbors
	def set_neighbors(self, neighbors):
		self.neighbors = neighbors

	#input: Response_Node to be a new neighbor to this
	def add_neighbor(self, neighbor):
		#neighbor_list cannot contain duplicates and can't be a neighbor to itself
		if neighbor not in self.neighbors and neighbor != self:
			self.neighbors.append(neighbor)

	#input: index of Response_Node neighbor to remove from this.neighbors
	def remove_neighbor(self, index):
		del self.neighbors[index]

	#input:  index of neighbor to return
	#output: response_node at index, or None if out of bounds
	def get_neighbor(self, index):
		if index < 0 or index >= len(self.neighbors):
			return None
		return self.neighbors[index]

	#input: index - int index of neighbor to change
	#       neighbor - response_node
	def set_neighbor(self, index, neighbor):
		self.neighbors[index] = neighbor


	#input: points int
	def set_points(self, points):
		self.points = points

	#output: this points
	def get_points(self):
		return self.points
		