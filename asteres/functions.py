import time

def create_issue_from_starred_repo(star, repo):
  
    issue_title = "{} ({})".format(star[1], star[0])
    issue_body = "{}\n\n{}".format(star[2], star[3])
    issue_lang = star[4]
    repo.create_issue(title = issue_title, body = issue_body)
    
    time.sleep(3)
      
    return(1)

def read_repo_id_from_issue(issue):
    
    result = int(issue.title.split("(")[1].replace(")", ""))
    
    return(result)
    
def create_issue_from_starred_repo_df(df, repo):
    """
    Takes in a dataframe of a starred repos data and makes it a issue
    for the repo
    """
    
    issue_title = "{} ({})".format(df['name'], df['repo_id'])
    issue_body = "{}\n\n{}".format(df['url'], df['description'])
    issue_tags = [tag for tag in df['tags_lang'].split(",")]
    
    if issue_tags[0] == "no-tag":
          
        repo.create_issue(
          title = issue_title, 
          body = issue_body
          )
    else:
        repo.create_issue(
          title = issue_title, 
          body = issue_body, 
          labels = issue_tags
          )
    
    # This is usually processed functionally as a batch so the delay
    # sidesteps GitHub API limiting
    time.sleep(3)
    
    return(1)
