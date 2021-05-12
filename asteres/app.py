import functions as hf
from github import Github
import json
import os
from flask import Flask, make_response, request, jsonify, render_template
import threading

app = Flask(__name__)
g = Github(os.environ["GHUB"])
g_usr = g.get_user()
repo = g_usr.get_repo("asteres")

def update_asteres():
  
    likes = [
        # The replacing in the url is formatting to create the actual web link
        [repo.id, repo.full_name, repo.url.replace("api.", "").replace("repos/", ""), repo.description, repo.language]
        for repo in  g.get_user().get_starred()
    ]
    
    issues = [x for x in repo.get_issues()]
    
    if len(issues) == 0:
        _ = [hf.create_issue_from_starred_repo(repo) for repo in likes]
        return("1")
    
    issue_ids = {hf.read_repo_id_from_issue(x) for x in issues}
    like_ids = {x[0] for x in likes}
    
    repos_to_add = [x for x in likes if x[0] in like_ids.difference(issue_ids)]
    
    repos_to_close = [
      x for x in issues 
      if hf.read_repo_id_from_issue(x) in issue_ids.difference(like_ids)
      ]
      
    _ = [issue.edit(state = "closed") for issue in repos_to_close]
    _ = [hf.create_issue_from_starred_repo(star, repo) for star in repos_to_add]

    # Lock issues
    not_locked_issues = [x for x in repo.get_issues() if not x.locked]
    _ = [x.lock("resolved") for x in not_locked_issues]
    
    return(1)
    
@app.route("/")
def hello():
    return("1")

@app.route("/update", methods = ["GET"])
def updater():
  
    _ = threading.Thread(target = update_asteres).start()
    
    return("1")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port, debug = True)
