"""
This script adds the language as an initial tag. This makes it difficult to find untagged items 
with GitHub's limited search functionality. Consider making adjustments to save yourself the headache.
"""

import functions as hf
import pandas as pd
from github import Github
import json
import time
import os

g = Github(os.environ["GHUB"])
g_usr = g.get_user()
repo = g_usr.get_repo("asteres")

likes = [r for r in g.get_user().get_starred()]

likes_data = [
    # The replacing in the url is formatting to create the actual web link
    [repo.id, repo.full_name, repo.url.replace("api.", "").replace("repos/", ""), repo.description, repo.language]
    for repo in likes
]

# This may take a while since the function has a built in 3 second delay to get around the GitHub APIs limits.
_ = list(map(
  lambda star: hf.create_issue_from_starred_repo(star, repo),
  likes_data
  ))

# Lock issues
issues = [x for x in repo.get_issues()]
_ = [x.lock("resolved") for x in issues]
