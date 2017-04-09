import math
import os
import pickle
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
import pymongo
from pymongo import MongoClient
from Scenario_DB import Scenario_DB


db = Scenario_DB()



responses = []
questions = []
questions.append('Has there ever been a time this was not a problem?')
questions.append('In the past, was there a time this was not seen as a problem')
questions.append('Has there ever been a time when this was not an issue')
questions.append('Looking back with your son was this ever OK?')
questions.append('In the past, was there a time this was not seen as a problem')
response = Response_Node("At one time there was a problem with my device", questions, [], 1)
responses.append(response)


questions = []
questions.append('Have you spoken with anyone else about this?')
questions.append('Have you consulted anyone else about this problem?')
questions.append('Have you talked to anyone yet?')
response = Response_Node("I have spoken to many people about this problem", questions, [], 2)
responses.append(response)

questions = []
questions.append('If I was there, what would I see?')
questions.append('What would I see if I were there?')
questions.append('What would he do I were there?')
questions.append('What would I see your son doing?')
response = Response_Node("If you were there, you would see my son running around", questions, [], 3)
responses.append(response)


questions = []
questions.append('why')
response = Response_Node("because that is the solution we have been looking for", questions, [], 4)
responses.append(response)



questions = []
questions.append('What would you see as the ideal solution?')
questions.append('What is the best solution in your eyes')
questions.append('What would you like the outcome to be?')
neighbors = []
neighbors.append(response)
response = Response_Node("The ideal solution", questions, neighbors, 5)
responses.append(response)


questions = []
questions.append('why')
response = Response_Node("because it is", questions, [], 6)
responses.append(response)


questions = []
questions.append('what color is the sky')
questions.append('is the color of the sky green?')
neighbors = []
neighbors.append(response)
response = Response_Node("the sky is blue", questions, neighbors, 7)
responses.append(response)

dialog = Dialog(responses)
scenario = Scenario("mike", "test description", None, dialog)

db.add_scenario(scenario)
