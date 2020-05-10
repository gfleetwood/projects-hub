import tweepy
import pickle
import settings_tweet as st

with open('philosophy_bot.pkl', 'rb') as f:
    bot = pickle.load(f)

CONSUMER_KEY = st.CK
CONSUMER_SECRET = st.CS
ACCESS_KEY = st.AK
ACCESS_SECRET = st.AS
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
api.update_status(bot.make_short_sentence(140))

##Links

#http://blog.mollywhite.net/twitter-bots-pt2/
#http://www.pygaze.org/2016/03/how-to-code-twitter-bot/
#http://briancaffey.github.io/2016/04/05/twitter-bot-tutorial.html