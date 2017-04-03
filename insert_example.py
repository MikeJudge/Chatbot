import math
import os
import pickle
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.bot_database

scenarios = db.scenario


responses = set()
questions = set()
questions.add('Has there ever been a time this was not a problem?')
questions.add('In the past, was there a time this was not seen as a problem')
questions.add('Has there ever been a time when this was not an issue')
questions.add('Looking back with your son was this ever OK?')
questions.add('In the past, was there a time this was not seen as a problem')
response = Response_Node("At one time there was a problem with my device", questions, set(), 1)
responses.add(response)


questions = set()
questions.add('Have you spoken with anyone else about this?')
questions.add('Have you consulted anyone else about this problem?')
questions.add('Have you talked to anyone yet?')
response = Response_Node("I have spoken to many people about this problem", questions, set(), 2)
responses.add(response)

questions = set()
questions.add('If I was there, what would I see?')
questions.add('What would I see if I were there?')
questions.add('What would he do I were there?')
questions.add('What would I see your son doing?')
response = Response_Node("If you were there, you would see my son running around", questions, set(), 3)
responses.add(response)


questions = set()
questions.add('why')
response = Response_Node("because that is the solution we have been looking for", questions, set(), 4)
responses.add(response)



questions = set()
questions.add('What would you see as the ideal solution?')
questions.add('What is the best solution in your eyes')
questions.add('What would you like the outcome to be?')
neighbors = set()
neighbors.add(response)
response = Response_Node("The ideal solution", questions, neighbors, 5)
responses.add(response)


questions = set()
questions.add('why')
response = Response_Node("because it is", questions, set(), 6)
responses.add(response)


questions = set()
questions.add('what color is the sky')
questions.add('is the color of the sky green?')
neighbors = set()
neighbors.add(response)
response = Response_Node("the sky is blue", questions, neighbors, 7)
responses.add(response)

dialog = Dialog(responses)
scenario = Scenario("mike Judge", "test description", None, dialog)

scenarios.insert_one({'data':pickle.dumps(scenario)})



client.close()
