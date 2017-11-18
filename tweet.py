import requests, sys, json, time, random
from requests_oauthlib import OAuth1

## auth to twitter api

authUrl = 'https://api.twitter.com/1.1/account/verify_credentials.json'
#auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET','USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
r = requests.get(authUrl, auth=auth)

if not r.status_code == 200:
	print("Auth unsuccessful!")
	sys.exit()
else:
	print("Auth successful!")

## read db.json file
with open('db.json') as file:
	data = json.load(file)

## loading tweets
dailyTweets = data["dailyTweets"]
mentionTweets = data["mentionTweets"];

## setting up api
url = "https://api.twitter.com/1.1/statuses/update.json?status=%s"
randomPerson = "%40ciftcisalih"

## post daily tweet
def postDailyTweet():
	randomTweet = dailyTweets[random.randint(0,len(dailyTweets)-1)]
	r = requests.post(url % randomTweet, auth=auth)
	print("%s - Daily Tweet tweeted." % time.ctime())

## post mention tweet
## url encoding (@ = %40)
def postMentionTweet():
	randomTweet = mentionTweets[random.randint(0,len(mentionTweets)-1)]
	r = requests.post(url % randomPerson + " " + randomTweet, auth=auth)
	print("%s - Mention Tweet tweeted." % time.ctime())

## action time
postedTweetCount = 0
while postedTweetCount < 16:
	postDailyTweet()
	postedTweetCount += 1
	print("Waiting 30 min for Mention Tweet")
	time.sleep(1800) #wait 30 min for mention tweet
	postMentionTweet()
	postedTweetCount += 1
	print("Waiting 1 hour for Daily Tweet")
	time.sleep(3600) #wait 1 hour for daily tweet

print("Today's works are done.")