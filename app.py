from flask import Flask, render_template, session, request, flash, abort, redirect, g, redirect
import os
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node
from Bot import Bot
from Bot_Manager import Bot_Manager
from Scenario_DB import Scenario_DB

app = Flask(__name__)

manager = Bot_Manager() #global
db = Scenario_DB()      #global


def check_input(admin = None, scenario_id = None, response_index = None, question_index = None):
    if not admin:
        return "Not logged in"

    if scenario_id == None:
        return ''
    scenario = db.get_scenario(scenario_id)
    if scenario == None:
        return "scenario not found"

    if response_index == None:
        return ''
    response = scenario.get_dialog().get_response(int(response_index))
    if response == None:
        return "response not found"

    if question_index == None:
        return ''
    question = response.get_question(int(question_index))
    if question == None:
        return 'question not found'

    return ''



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



@app.route("/admin")
def admin(): 
   #if not logged in, show user the login screen
   if not session.get('logged_in'):
       return render_template('login.html')

   scenario_list = db.get_scenarios()
   return render_template('admin_main.html', scenario_list = scenario_list)
   #return "Hello Boss!  <a href='/logout'>Logout</a>" #todo: return html for admin page


@app.route("/admin/scenario/<scenario_id>", methods=['POST', 'GET'])
def view_scenario(scenario_id):
    c = check_input(session.get('logged_in'), scenario_id)
    if c != '':
        return c

    scenario = db.get_scenario(scenario_id)
    if request.method == 'POST': #updating a scenario
        scenario.set_name(request.form['scenario_name'])
        scenario.set_description(request.form['scenario_description'])

        dialog = scenario.get_dialog()
        for i in xrange(len(dialog.get_responses())):
            response = dialog.get_response(i)
            response.set_response(request.form.get('response' + str(i)))
            response.set_points(int(request.form.get('response_points' + str(i))))

            for n in xrange(len(response.get_questions())):
                response.set_question(n, request.form.get('question' + str(i) + '_' + str(n)))

        dialog.set_total_points() #update points for the dialog
        db.update_scenario(scenario_id, scenario) #update scenario in db

    #display scenario
    return render_template('scenario_view.html', scenario = scenario, scenario_id = scenario_id)




@app.route("/admin/scenario/add_response/<scenario_id>")
def add_response(scenario_id):
    c = check_input(session.get('logged_in'), scenario_id)
    if c != '':
        return c

    scenario = db.get_scenario(scenario_id)
    scenario.get_dialog().add_response(Response_Node())
    db.update_scenario(scenario_id, scenario)
    return redirect("/admin/scenario/" + scenario_id)



@app.route("/admin/scenario/remove_response/<scenario_id>/<response_index>")
def remove_response(scenario_id, response_index):
    c = check_input(session.get('logged_in'), scenario_id, response_index)
    if c != '':
        return c

    scenario = db.get_scenario(scenario_id)
    response = scenario.get_dialog().get_response(int(response_index))

    #since we are deleting a response, all responses pointing to this response need to be updates
    for curr_response in scenario.get_dialog().get_responses():
        for i in xrange(len(curr_response.get_neighbors())):
            if curr_response.get_neighbor(i) == response:
                curr_response.remove_neighbor(i)
                break


    scenario.get_dialog().remove_response(int(response_index))
    db.update_scenario(scenario_id, scenario)
    return redirect("/admin/scenario/" + scenario_id)



@app.route("/admin/scenario/add_question/<scenario_id>/<response_index>")
def add_question(scenario_id, response_index):
    c = check_input(session.get('logged_in'), scenario_id, response_index)
    if c != '':
        return c
    
    scenario = db.get_scenario(scenario_id)
    scenario.get_dialog().get_response(int(response_index)).add_question('')
    db.update_scenario(scenario_id, scenario)
    return redirect("/admin/scenario/" + scenario_id)




@app.route("/admin/scenario/remove_question/<scenario_id>/<response_index>/<question_index>")
def remove_question(scenario_id, response_index, question_index):
    c = check_input(session.get('logged_in'), scenario_id, response_index, question_index)
    if c != '':
        return c

    scenario = db.get_scenario(scenario_id)
    response = scenario.get_dialog().get_response(int(response_index))
    response.remove_question(int(question_index))
    db.update_scenario(scenario_id, scenario)
    return redirect("/admin/scenario/" + scenario_id)


@app.route("/admin/scenario/new")
def create_scenario():
    c = check_input(session.get('logged_in'))
    if c != '':
        return c

    scen = Scenario()
    key = db.add_scenario(scen)
    return redirect('/admin/scenario/' + key)


@app.route("/admin/scenario/remove_scenario/<scenario_id>")
def remove_scenario(scenario_id):
    c = check_input(session.get('logged_in'), scenario_id)
    if c != '':
        return c

    db.delete_scenario(scenario_id)
    return redirect('/admin')



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

    #Post part
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

