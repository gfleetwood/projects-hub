from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os

app = Flask(__name__, template_folder = '.')
data = pd.read_csv("https://gist.githubusercontent.com/gfleetwood/c35710d4466c40de3c95bdb411d16a31/raw/c682f96fa81dfe2ee68962c394712210bca6aa57/nyc-subway.csv")#.fillna("").sort_values(by = ['Train', 'Id'])

@app.route('/')
def hello_world():
  
  return(render_template(
    "index.html", 
    data = data.to_html(table_id="example", escape = False, justify = 'center', index = False)
    ))

if __name__=="__main__":
  app.debug = True
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port = port)
