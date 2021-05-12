# Asteres

## Overview

Custom tags for starred repos is a GitHub feature that I - and [others](https://github.com/dear-github/dear-github/issues/86) - have wanted for a long time. Solutions like [Astral](https://astralapp.com/) exist but use another platform. This solution leverages GitHub issues for tag management of starred repos, and is inspired by [this blog](https://github.com/lukego/blog) where posts are issues. A GitHub Workflow cronjob hits a Flask endpoint on Heroku every two hours to look for updates.

I initially intended to incorporate starred gists as well, but demurred since I personally don't use mine. Extending the code to do this is pretty easy, and I included a snippet in the appendix. 

## Issues

Let tackle these upfront:

* The code sets the initial tag of a starred repo issue as the repo's language. This can be a hassle since you can't leverage the `no-label` issue filter to find unlabeled items. I have a convoluted workaround for reasons which include the seemingly poor performance of the search's language filter. You may want to do something else.

* Adding repos during the updating provided by `app.py` may handle the following scenario in a way you might not agree with:

    1. A repo was starred and an issue was created
    2. The repo was unstarred and the issue was closed
    3. The repo was re-starred
    
As it stands now re-starring would leave the issue closed and not re-create it. A good argument exists that it should re-open it. I left it as is because it doesn't really matter to me that much, and GitHub's Rest API should really have the delete issue endpoint. If it did then unstarring would delete the issue and re-starring would recreate it.

## Installation

I used Python 3.6 on Ubuntu 18.04 but any Python 3 version should do. The only non base python library the setup requires is [PyGithub](https://github.com/PyGithub/PyGithub): `pip install PyGithub`. 

## Initialization

`init-from-astral.py` is my personal setup script since I had a lot of tags stored in Astral. `general-init.py` will get you started from scratch. First off: 

* Create a personal access token at `https://github.com/settings/tokens`. You can limit its access to `public_repo` if you want a public repo. Give it full `repo` permissions if you want it to be private.

* Store the token as an environment variable called `GHUB` so the script can locate it. 

* Fork this repo, go to settings and enable issues (and privacy if you want to), git clone a local version, and then cd into the folder.

* Run `python general-init.py` to create an issue for each starred repo where the title is the repository's name and id (id in parentheses), the body is its url and description, and the tag is the language. Each issue is immediately locked. (This may take a while since the function has a built in 3 second delay to get around the GitHub APIs limits.) If you want to change this structure you'll have to edit `app.py` to parse the repo id from wherever its new location is. It's integral for updating.

## Monitoring And Deployment

`.github/workflows/curl.yml` is a GitHub Workflow cronjob that hits an endpoint with a get request every hour to trigger updates to asteres. You can change `cron: "0 * * * *"` to suit how often you'd like to poll for updates. You must change `http://example.com/` to the endpoint of the deployed `app.py` file.

The deployment is setup for Heroku with all the required files. You can use [this](https://devcenter.heroku.com/articles/getting-started-with-python) tutorial as a guide or deploy wherever you wish.

## Conclusion

That should be it. I'd say file an issue if you run into problems but since this is my asteres repo...please don't. (Pull requests maybe?)

## Appendix

Here's the skeleton code to included starred gists.

```
def create_issue_from_gist(gist, repo):
  
    issue_title = "{}-{}".format("gist", repo[0])
    issue_body = "{}\n\n{}".format(repo[1], repo[2])
    lang = repo[4]
    
    If lang is None:
        repo.create_issue(title = issue_title, body = issue_body)
    else:
        repo.create_issue(title = issue_title, body = issue_body, labels = [lang])
      
    return(1)

g = Github(os.environ["GHUB"])
g_usr = g.get_user()
gists = [x for x in g_usr.get_starred_gists()]
gists_data = [[repo.id, repo.html_url, repo.description] for repo in gists] 
```
