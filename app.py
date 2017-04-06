from flask import Flask, render_template, session, request, flash, abort, redirect, g
import os
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
from Bot import Bot
from Bot_Manager import Bot_Manager
from Scenario_DB import Scenario_DB
from bson.objectid import ObjectId

app = Flask(__name__)

manager = Bot_Manager() #global
db = Scenario_DB()


@app.route('/login', methods=['POST'])
def do_admin_login():
    #credential check
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return admin() 


@app.route("/logout")
def logout():
    #logout user and show them the home page
    session['logged_in'] = False
    return admin()



@app.route("/admin", methods=['POST', 'GET'])
def admin(): 
   #if not logged in, show user the login screen
   if not session.get('logged_in'):
        return render_template('login.html')
   


   scenario_list = db.get_scenarios()
   return render_template('admin_main.html', scenario_list = scenario_list)
   
 

   #return "Hello Boss!  <a href='/logout'>Logout</a>" #todo: return html for admin page

@app.route("/scenario/<scenario_id>", methods=['POST', 'GET'])
def view_scenario(scenario_id):
   scenario = db.get_scenario(ObjectId(scenario_id))
   return render_template('scenario_view.html', scenario = scenario)



@app.route("/chat/<scenario_id>", methods=['POST', 'GET'])
def chat(scenario_id):
   #the name parameter in web address is looked up in bot db
   if manager.get_bot(scenario_id) == None: #bad request, the bot for this scenario doesn't exist
      return "bot not found"

   bot, scenario = manager.get_bot(scenario_id)

   if request.method == 'GET': #first time visiting page, initialize user data
      session['dialog'] = []
      session['prev_response'] = -1
      session['score'] = 0
      session['prev_response_ids'] = []
      return render_template('chat.html', scenario = scenario)

   s = request.form['input_text'] #get input from user
   dialog = session['dialog']
   prev_response = session['prev_response']
   curr_score = session['score']
   prev_response_ids = session['prev_response_ids']

   reply, prob_score, response_id, points = bot.reply(prev_response, s)[0]

   #this check is needed to give user points only the first time it hits this response
   if response_id not in prev_response_ids: 
      curr_score += points
      prev_response_ids.append(response_id)
   dialog.append((s, reply))

   #update session data
   session['dialog'] = dialog
   session['prev_response'] = response_id
   session['score'] = curr_score
   session['prev_response_ids'] = prev_response_ids

   #send data to render_template in order to display it to the user
   return render_template('chat.html', dialog = dialog, score = curr_score, scenario = scenario)
   


app.secret_key = 'secret key'
if __name__ == "__main__":
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run()

