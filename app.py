from flask import Flask, render_template, session, request, flash, g
import os
from bot import Bot

app = Flask(__name__)
b = Bot('input.txt', 1e-2)

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

