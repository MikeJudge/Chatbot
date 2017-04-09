class Dialog:

	#input: responses - list of Response_Node
	def __init__(self, responses = []):
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


	#output: list of Response_Node in this
	def get_responses(self):
		return self.responses

	#input: list of Response_Node to represent this dialog
	def set_responses(self, responses):
		self.responses = responses
		self.set_total_points() #update total points

	#input: Response_Node to add to the response list
	def add_response(self, response):
		self.responses.append(response)
		self.set_total_points() #update total points


	#input: index of Response_Node to remove from the response list
	def remove_response(self, index):
	    #since we are deleting a response, all responses pointing to this response need to be updated
	    response = self.responses[index]
	    for curr_response in self.responses:
	    	print self.responses
	    	for i in xrange(len(curr_response.get_neighbors())):
	    		if curr_response.get_neighbor(i) == response:
	    			curr_response.remove_neighbor(i)
	    			break
	    print self.responses
	    del self.responses[index]
	    self.set_total_points() #update total points


	#input:  index of response
	#output: response_node located at index, or None if out of bounds
	def get_response(self, index):
		if index < 0 or index >= len(self.responses):
			return None
		return self.responses[index]

	#input: index of response
	#       Response_Node object to save to index
	def set_response(self, index, response):
		self.responses[index] = response
		self.set_total_points()

	#output: number of responses in dialog
	def get_length(self):
		return len(self.responses)