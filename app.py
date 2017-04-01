from flask import Flask, render_template, session, request, flash, g
import os
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
from Bot import Bot

app = Flask(__name__)


responses = set()
questions = set()
questions.add('Has there ever been a time this was not a problem?')
questions.add('In the past, was there a time this was not seen as a problem')
questions.add('Has there ever been a time when this was not an issue')
questions.add('Looking back with your son was this ever OK?')
questions.add('In the past, was there a time this was not seen as a problem')
response = Response_Node("At one time there was a problem with my device", questions, set())
responses.add(response)


questions = set()
questions.add('Have you spoken with anyone else about this?')
questions.add('Have you consulted anyone else about this problem?')
questions.add('Have you talked to anyone yet?')
response = Response_Node("I have spoken to many people about this problem", questions, set())
responses.add(response)

questions = set()
questions.add('If I was there, what would I see?')
questions.add('What would I see if I were there?')
questions.add('What would he do I were there?')
questions.add('What would I see your son doing?')
response = Response_Node("If you were there, you would see my son running around", questions, set())
responses.add(response)


questions = set()
questions.add('why')
response = Response_Node("because that is the solution we have been looking for", questions, set())
responses.add(response)



questions = set()
questions.add('What would you see as the ideal solution?')
questions.add('What is the best solution in your eyes')
questions.add('What would you like the outcome to be?')
neighbors = set()
neighbors.add(response)
response = Response_Node("The ideal solution", questions, neighbors)
responses.add(response)


questions = set()
questions.add('why')
response = Response_Node("because it is", questions, set())
responses.add(response)


questions = set()
questions.add('what color is the sky')
questions.add('is the color of the sky green?')
neighbors = set()
neighbors.add(response)
response = Response_Node("the sky is blue", questions, neighbors)
responses.add(response)

dialog = Dialog(responses)
scenario = Scenario("mike Judge", "test description", None, dialog)



b = Bot(scenario, 1e-8)

@app.route("/", methods=['POST', 'GET'])
def home():
   if request.method == 'GET':
      session['dialog'] = []
      return render_template('chat.html')

   s = request.form['input_text']
   l = session['dialog']
   l.append((s, b.reply(s)[0][0]))
   session['dialog'] = l

   return render_template('chat.html', dialog = l)



app.secret_key = 'secret key'
if __name__ == "__main__":
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run()

