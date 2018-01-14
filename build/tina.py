import requests
import sys
import json
import time
import random
import os.path
from requests_oauthlib import OAuth1
from urllib.parse import quote_plus as encode


def findPeople():
    # Selecting random keyword
    keywords = db["keywords"]
    keyword = keywords[random.randint(0, len(keywords) - 1)]
    print("%s - Tina: Searching people keyword is %s now." %
          (time.ctime(), keyword))

    # Searching people
    sUrl = "https://api.twitter.com/1.1/search/tweets.json?q=%s&vertical=news"
    searchUrl = sUrl % keyword
    r = requests.get(searchUrl, auth=auth)

    if r.status_code == 200:
        randomPersonJson = json.loads(r.text)
    else:
        print("%s - Tina: Unexpected Error, Error Code: %s" %
              (time.ctime(), r.status_code))
        print("%s - Tina: Trying to find people.." % time.ctime())
        findPeople()

    global randomPerson
    randomPerson = []
    while len(randomPerson) < 15:
        try:
            randomPerson.append(randomPersonJson["statuses"][len(
                randomPerson)]["user"]["screen_name"])
        except Exception as e:
            print("%s - Tina: Error: %s" % (time.ctime(), e))
            print("%s - Tina: Trying to find people.." % time.ctime())
            findPeople()


mentionCount = 0


def tweet(status):
    tweetUrl = "https://api.twitter.com/1.1/statuses/update.json?status=%s"

    if status == "tweet":
        randomTweet = tweets[random.randint(0, len(tweets) - 1)]
        r = requests.post(tweetUrl % encode(randomTweet), auth=auth)

        if r.status_code == 200:
            print("%s - Tina: tweeted." % time.ctime())
        elif r.status_code == 403:
            print("%s - Tina: Tweet duplicated." % time.ctime())
            print("%s - Tina: Trying to tweet again.." % time.ctime())
            tweet("tweet")
        else:
            print("%s - Tina: Unexpected Error, Error Code: %s" %
                  (time.ctime(), r.status_code))

    elif status == "mention":
        global mentionCount
        randomMentionTweet = mentionTweets[random.randint(
            0, len(mentionTweets) - 1)]
        randomPersonToTweet = randomPerson[mentionCount]

        r = requests.post(tweetUrl % "%40" + randomPersonToTweet +
                          "%20" + encode(randomMentionTweet), auth=auth)
        if r.status_code == 200:
            print("%s - Tina: Mentioned to %s" %
                  (time.ctime(), randomPersonToTweet))
        elif r.status_code == 403:
            print("%s - Tina: Mention tweet duplicated." % time.ctime())
        else:
            print("%s - Tina: Unexpected Error, Error Code: %s" %
                  (time.ctime(), r.status_code))

        if mentionCount == 14:
            findPeople()
            mentionCount = 0
        else:
            mentionCount += 1


if __name__ == "__main__":
    scriptPath = os.path.dirname(__file__)
    with open(os.path.join(scriptPath, "auth.json")) as file:
        authJson = json.load(file)

    authUrl = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(authJson["API_KEY"], authJson["API_SECRET"],
                  authJson["OAUTH_TOKEN"], authJson["OAUTH_TOKEN_SECRET"])

    # Trying to Auth to Twitter
    r = requests.get(authUrl, auth=auth)
    if not r.status_code == 200:
        print("%s - Tina: Auth unsuccessful!" % time.ctime())
        sys.exit()
    else:
        print("%s - Tina: Auth successful!" % time.ctime())

    # Reading db.json for tweets
    with open(os.path.join(scriptPath, "db.json")) as file:
        db = json.load(file)

    tweets = db["tweets"]
    mentionTweets = db["mentionTweets"]

    # Finding People
    findPeople()

    while True:
        for x in range(0, 16):
            tweet("mention")
            time.sleep(901)
        tweet("tweet")
        time.sleep(901)
