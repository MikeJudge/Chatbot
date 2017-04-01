import math
import os
import pickle
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.bot_database

scenarios = db.scenario


for scenario in scenarios.find():
	t = pickle.loads(scenario['data'])
	print t.get_name()
	print t.get_description()
	print t.image
	dialog = t.get_dialog()
	responses = dialog.get_responses()
	for response in responses:
		print ""
		print response
		print response.get_response()
		print response.get_questions()
		print response.get_neighbors()
	'''t.set_name('new_name')
	scenario['data'] = pickle.dumps(t)
	scenarios.save(scenario)'''


		


client.close()