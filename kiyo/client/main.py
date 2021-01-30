from flask import Flask, render_template, request, jsonify
from twilio.rest import Client 
import random 
import time
import os

account_sid = os.getenv("SID")
auth_token = os.getenv("TOKEN")
client = Client(account_sid, auth_token)

data_storage = []
status = "No status"
texts_sent = 0

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/query-example', methods = ['PUT', 'POST'])
def index2():

  global data_storage

  if request.method == 'PUT':
    data_temp = request.args.get('test')
    print(data_temp)
    data_storage.append(data_temp)

  return """<h1>Hello World</h1>"""

@app.route('/get-data', methods = ['GET'])
def get_data():

  global data_storage
  
  data = "No data"
  state = "No status"

  if request.method == 'GET':
    try:
      data = data_storage[-1]
    except:
      pass

  if len(data_storage) > 5:
    state = calc_slope(data_storage)

  return jsonify(result = data, status = state)

def calc_slope(data):

  global status
  global texts_sent

  state_old = status
  
  data_enumerated = [[i,float(j)] for i,j in enumerate(data)]
  
  prev = data_enumerated[-2]
  current = data_enumerated[-1]
    
  slope = (current[1] - prev[1])/(current[0] - prev[0])
    
  if slope >= 2:
    state = "ON"
  elif slope <= -2:
    state = "OFF"
  else:
    state = "STEADY"

  # if state_old != state & texts_sent < 10:
  #   message = client.messages \
  #               .create(
  #                    body = "Your machine's status is {}".format(status),
  #                    from_ = os.getenv("TWILIOPHONE"),
  #                    to = os.getenv("MYPHONE"))
  #   texts_sent = texts_sent + 1
            
    return(state)

app.run('0.0.0.0', 8080)
