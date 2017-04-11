import pickle
from Scenario import Scenario
from pymongo import MongoClient
from Dialog import Dialog
from Response_Node import Response_Node
from bson.objectid import ObjectId


def scenario_to_doc(scenario, doc):
	doc['name'] = scenario.get_name()
	doc['description'] = scenario.get_description()
	doc['image'] = scenario.get_image()


	dialog = []
	response_map = {}
	for i in xrange(len(scenario.get_dialog().get_responses())):
		response_map[scenario.get_dialog().get_response(i)] = i

	for response in scenario.get_dialog().get_responses():
		neighbors = []
		for neighbor in response.get_neighbors():
			neighbors.append(response_map[neighbor])

		dialog.append((response.get_response(), response.get_questions(), neighbors, response.get_points()))

	doc['dialog'] = dialog
	return doc

			

def doc_to_scenario(doc):
	dialog_data = doc['dialog']
	dialog = []

	for response_text, questions, neighbor_ids, points in dialog_data:
		dialog.append(Response_Node(response_text, questions, neighbor_ids, points))

	for response in dialog:
		neighbors = []
		neighbor_ids = response.get_neighbors()
		for neighbor_id in neighbor_ids:
			neighbors.append(dialog[neighbor_id])
		response.set_neighbors(neighbors)

	return Scenario(doc['name'], doc['description'], doc['image'], Dialog(dialog))



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
			#pickle is used to construct Scenario from bson object
			scenario_list.append((str(scenario_doc['_id']), doc_to_scenario(scenario_doc)))

		client.close()
		return scenario_list




	#input:  Scenario object
	#output: scenario_id linked to this Scenario object (use this id to index into db)

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
		if scenario_doc == None:
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

		if scenarios.find_one({"_id": ObjectId(scenario_key)}) == None:
			return None

		scenario_doc = scenarios.find_one({"_id": ObjectId(scenario_key)})
		scenario = doc_to_scenario(scenario_doc) #get the entry from the database
		client.close()
		return scenario

	def clear_db(self):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		for scenario_doc in scenarios.find():
			scenarios.delete_one(scenario_doc)

		client.close()


