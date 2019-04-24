import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing

from textblob import TextBlob  # for sentimental
import re

# For plotting and visualization:
from IPython.display import display
# for display use only import matplotlib.pyplot as plt
import seaborn as sns
# We import our access keys:
from keys.twitter_keys import *    # This will allow us to use the keys as variables

# We import our access keys:
# optional from credentials import *    # This will allow us to use the keys as variables

# API's setup:
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

    # We create an extractor object:
extractor = twitter_setup()

# We create a tweet list as follows:
# tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200)

## search by hashtab
tweets = extractor.user_timeline(screen_name="cnnbrk", count=10)


    # We create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

# We display the first 10 elements of the dataframe:
#display(data.head(10))


# We add relevant data:
data['created_at'] = np.array([tweet.created_at for tweet in tweets])
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])



### Below for sentimental Analysis
def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
try:
    # We create a column with the result of the analysis:
    data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
    #api.send("sentimentPreview","Rules:\n" + data (10));
    #display (data (10))
    myString = data.to_csv()
    display ( myString )
except Exception as inst:
    display ( "errors" + str(inst))
