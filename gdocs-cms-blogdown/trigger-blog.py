from flask import Flask, request
import os
app = Flask(__name__) 

@app.route("/")
def hello():
  return "Hello World!" 
  
@app.route('/meh', methods = ['GET'])
def index2():
  if request.method == 'GET':
    os.system("Rscript /home/paperspace/projects/gdocs-cms/gdrive-cms.R")
    
  return "Hello World!"

if __name__ == "__main__":
  app.run(host='0.0.0.0')
