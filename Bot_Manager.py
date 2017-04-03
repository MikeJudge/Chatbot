from pymongo import MongoClient
import pickle
from Scenario import Scenario
from Bot import Bot

class Bot_Manager:

	def __init__(self):
		self.bot_map = {}
		self.load_bots()


	#loads the data stored in MongoDB for each scenario, respawns them into scenario objects
	#and uses it to create Bots. Bots are stored in bot_map as Name_of_person:Bot

	def load_bots(self):
		client = MongoClient('localhost', 27017)
		db = client.bot_database

		scenarios = db.scenario
		for scenario in scenarios.find():
			scenario = pickle.loads(scenario['data'])
			self.bot_map[scenario.get_name()] = Bot(scenario, 1e-8)

		client.close()


	#input:  string representing name of person in scenario
	#ouptut: bot mapped to the name

	def get_bot(self, key):
		return self.bot_map[key]



test = Bot_Manager()
b = test.get_bot("mike Judge")
s = ''
prev_response = -1 #initial id
points = 0
while True:
    s = raw_input("User: ")
    if s == 'exit':
    	break
    y =  b.reply(prev_response, s)
    for x in y:
    	print x
    print ""
    prev_response = y[0][2]
    points += y[0][3]

print 'points: ' + str(points) + "out of: " + str(b.get_total_points())

