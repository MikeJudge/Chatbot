from pymongo import MongoClient
import pickle
from Scenario import Scenario
from Bot import Bot

class Bot_Manager:

	def __init__(self):
		self.bot_map = {}
		self.load_bots()


	def load_bots(self):
		client = MongoClient('localhost', 27017)
		db = client.bot_database

		scenarios = db.scenario
		for scenario in scenarios.find():
			scenario = pickle.loads(scenario['data'])
			self.bot_map[scenario.get_name()] = Bot(scenario, 1e-8)

		client.close()



	def get_bot(self, key):
		return self.bot_map[key]



test = Bot_Manager()
b = test.get_bot("mike Judge")
s = ''
prev_response = -1 #initial id
while s != 'exit':
    s = raw_input("User: ")
    y =  b.reply(prev_response, s)
    for x in y:
    	print x
    print ""
    prev_response = y[0][2]

