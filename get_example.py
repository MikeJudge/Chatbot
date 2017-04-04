import math
import os
import pickle
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
from pymongo import MongoClient
from Scenario_DB import Scenario_DB


db = Scenario_DB()



for key, scenario in db.get_scenarios():
	print key
	'''print t.get_description()
	print t.image
	dialog = t.get_dialog()
	print dialog.get_total_points()
	responses = dialog.get_responses()
	for response in responses:
		print ""
		print response
		print response.get_response()
		print response.get_questions()
		print response.get_neighbors()
		print response.get_points()'''
	#db.delete_scenario(doc)


