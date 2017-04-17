from Scenario import Scenario
from pymongo import MongoClient
from Dialog import Dialog
from Response_Node import Response_Node
from bson.objectid import ObjectId

#input:  scenario - Scenario object
#        doc      - dictionary
#output: updated doc

def scenario_to_doc(scenario, doc):
	doc['name'] = scenario.get_name()
	doc['description'] = scenario.get_description()
	doc['image'] = scenario.get_image()
	doc['video_link'] = scenario.get_video_link()


	dialog = []
	response_map = {}
	#populate response_map with response_node:index
	#we will use this data to serialize the dialog object
	for i in xrange(len(scenario.get_dialog().get_responses())):
		response_map[scenario.get_dialog().get_response(i)] = i

	for response in scenario.get_dialog().get_responses():
		neighbors = []
		#response points to indices instead of objects in the serialization
		for neighbor in response.get_neighbors():
			neighbors.append(response_map[neighbor])

		dialog.append((response.get_response(), response.get_questions(), neighbors, response.get_points()))

	doc['dialog'] = dialog
	return doc

#input:  doc - dictionary
#output: Scenario object represented by doc

def doc_to_scenario(doc):
	dialog_data = doc['dialog']
	dialog = []

	#create dialog list, but neighbor_ids is temporary
	for response_text, questions, neighbor_ids, points in dialog_data:
		dialog.append(Response_Node(response_text, questions, neighbor_ids, points))

	for response in dialog:
		neighbors = []
		neighbor_ids = response.get_neighbors() #indices of neighbors
		for neighbor_id in neighbor_ids:
			neighbors.append(dialog[neighbor_id]) #use indices to find neighbors
		response.set_neighbors(neighbors) #store actual neighbors for this response

	video_link = ''
	if 'video_link' in doc:
		video_link = doc['video_link']

	return Scenario(doc['name'], doc['description'], doc['image'], Dialog(dialog), video_link)



class Scenario_DB:


	def __init__(self):
		pass


	#output: list of (scenario_id, Scenario)
	#        scenario_id is used for indexing scenario in db

	def get_scenarios(self):
		#set up connection to database
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios
		
		#run through each scenario in database and append (scenario_id, Scenario)
		scenario_list = []
		for scenario_doc in scenarios.find():
			scenario_list.append((str(scenario_doc['_id']), doc_to_scenario(scenario_doc)))

		client.close()
		return scenario_list




	#input:  Scenario object
	#output: scenario_id linked to this Scenario object (use id to index into db)

	def add_scenario(self, scenario):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		scenario_doc = scenario_to_doc(scenario, {}) #convert Scenario object to form that is mongoDB compatible
		scenarios.insert_one(scenario_doc)  #insert scenario_doc into database, (id field will be added to scenario_doc)
		client.close()
		return str(scenario_doc['_id'])


	#input:  scenario_key - used to find Scenario being updated in database 
	#        scenario     - Scenario object to store in db
	#output: True on success, False on failure

	def update_scenario(self, scenario_key, scenario):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		scenario_doc = scenarios.find_one({"_id": ObjectId(scenario_key)})
		if scenario_doc == None: #not found
			return False

		scenario_to_doc(scenario, scenario_doc) #update mapping with new Scenario object
		scenarios.save(scenario_doc) #log change in database
		client.close()
		return True


	#input:  scenario_key - key of scenario to be deleted from database
	#output: True on success, False on failure

	def delete_scenario(self, scenario_key):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios
		if scenarios.find_one({"_id": ObjectId(scenario_key)}) == None:
			return False

		scenarios.delete_one({"_id": ObjectId(scenario_key)}) #remove the entry from the database
		client.close()
		return True


	#input:  scenario_key - key of scenario to be returned from database
	#output: scenario linked to the key, or None if not found
	
	def get_scenario(self, scenario_key):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		if scenarios.find_one({"_id": ObjectId(scenario_key)}) == None: #not found
			return None

		scenario_doc = scenarios.find_one({"_id": ObjectId(scenario_key)})
		scenario = doc_to_scenario(scenario_doc) #get the entry from the database
		client.close()
		return scenario

	
	#wipe all data from database
	def wipe_db(self):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		for scenario_doc in scenarios.find():
			scenarios.delete_one(scenario_doc)

		client.close()

	#output: list of scenario docs
	def export_raw(self):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		result = list(scenarios.find())
		client.close()
		return result


	#input: raw_docs: list of scenario docs
	def import_raw(self, raw_docs):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		for doc in raw_docs:
			#if scenario is not in the database, then add it to DB
			if scenarios.find_one({"_id": doc['_id']}) == None:
				scenarios.insert_one(doc)
			else: #update entry in DB if already there
				scenarios.save(doc)

		client.close()



