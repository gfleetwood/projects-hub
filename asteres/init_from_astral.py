"""
My initialization of my asteres repo given that I already had a legion of tags in astral.
I also created the astered repo manually. See general-init.py for a fully automated workflow.
"""

# data collection: from github

import functions as hf
import pandas as pd
from github import Github
import json
import time
import os

g = Github(os.environ['GHUB'])
repo = g.get_repo("gfleetwood/asteres")
likes = [r for r in g.get_user().get_starred()]

likes_data = [
    # The replacing in the url is formatting to create the actual web link
    [repo.id, repo.full_name, repo.url.replace("api.", "").replace("repos/", ""), repo.description, repo.language]
    for repo in likes
]

likes_df = pd.DataFrame(
    likes_data, 
    columns = ["repo_id", "name", "url", "description", "language"]
)

# data collection: from astral

with open("my_astral_data.json", "r") as f:
    astral_raw_data = f.read()

astral_dict = json.loads(astral_raw_data)

astral_df = pd.DataFrame([
    [astral_dict[x]['repo_id'], ','.join(y['name'] for y in astral_dict[x]['tags'])]
    for x in astral_dict.keys()], 
    columns = ['repo_id', 'tags']
)

# join data

assert len(likes_df) == len(astral_df)

ghub_star_data = pd.merge(likes_df, astral_df, on = ["repo_id"])
ghub_star_data["tags_lang"] = ghub_star_data["tags"] + "," + ghub_star_data["language"]

ghub_star_data = ghub_star_data.fillna(
    value = {'description': "No Description", 'tags_lang': "no-tag"}
)

# upload data to repo

ghub_star_data["written_to_repo"] = ghub_star_data.apply(lambda x: hf.create_issue_from_starred_repo_df(x, repo), axis = 1)

# Lock issues
issues = [x for x in repo.get_issues()]
_ = [x.lock("resolved") for x in issues]
