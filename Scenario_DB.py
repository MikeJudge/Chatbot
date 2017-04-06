import pickle
from Scenario import Scenario
from pymongo import MongoClient

class Scenario_DB:

	def __init__(self):
		pass


	#output: list of (scenario_doc, Scenario)
	#        scenario_doc is used for delete and update operation indexing

	def get_scenarios(self):
		#set up connection to database
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios
		
		#run through each scenario in database and append (scenario_doc, Scenario)
		scenario_list = []
		for scenario_doc in scenarios.find():
			#pickle is used to construct Scenario from bson object
			scenario_list.append((scenario_doc['_id'], pickle.loads(scenario_doc['data'])))

		client.close()
		return scenario_list


	#input:  Scenario object
	#output: scenario_id linked to this Scenario object (use in update_scenario and delete_scenario functions)

	def add_scenario(self, scenario):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		scenario_doc = {'data':pickle.dumps(scenario)} #convert Scenario object to bson object
		scenarios.insert_one(scenario_doc)  #insert scenario_doc into database
		client.close()
		return scenario_doc['_id']


	#input: scenario_key - used to find Scenario being updated in database 
	#       scenario     - Scenario object to store in db

	def update_scenario(self, scenario_key, scenario):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		scenario_doc = scenarios.find_one({"_id": scenario_key})
		scenario_doc['data'] = pickle.dumps(scenario) #update mapping with new Scenario object
		scenarios.save(scenario_doc) #log change in database
		client.close()


	#input: scenario_key - key of scenario to be deleted from database

	def delete_scenario(self, scenario_key):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		scenarios.delete_one({"_id": scenario_key}) #remove the entry from the database
		client.close()


	#input: scenario_key - key of scenario to be returned from database

	def get_scenario(self, scenario_key):
		client = MongoClient('localhost', 27017)
		scenarios = client.scenario_database.scenarios

		scenario = pickle.loads(scenarios.find_one({"_id": scenario_key})['data']) #get the entry from the database
		client.close()
		return scenario

