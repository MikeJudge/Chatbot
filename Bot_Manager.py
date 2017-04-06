from pymongo import MongoClient
import pickle
from Scenario import Scenario
from Bot import Bot
from Scenario_DB import Scenario_DB

class Bot_Manager:

	def __init__(self):
		self.bot_map = {}
		self.load_bots()


	#loads the data stored in MongoDB for each scenario, respawns them into scenario objects
	#and uses it to create Bots. Bots are stored in bot_map as scenario_key:(Bot,Scenario)

	def load_bots(self):
		db = Scenario_DB()
		for scenario_key, scenario in db.get_scenarios():
			self.bot_map[str(scenario_key)] = (Bot(scenario, 1e-8), scenario)


	#input:  key for scenario
	#ouptut: bot mapped to the key, or None if not found

	def get_bot(self, key):
		if key not in self.bot_map:
			return None
		return self.bot_map[key]


'''
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

print 'points: ' + str(points) + "out of: " + str(b.get_total_points())'''

