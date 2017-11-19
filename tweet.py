import requests, sys, json, time, random
from requests_oauthlib import OAuth1
from urllib.parse import quote_plus

## read db.json file
with open('db.json') as file:
	data = json.load(file)

## auth to twitter api
authUrl = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(data['auth']['YOUR_APP_KEY'], data['auth']['YOUR_APP_SECRET'],
 data['auth']['USER_OAUTH_TOKEN'], data['auth']['USER_OAUTH_TOKEN_SECRET'])
r = requests.get(authUrl, auth=auth)

## checking auth
if not r.status_code == 200:
	print("Auth unsuccessful!")
	sys.exit()
else:
	print("Auth successful!")


randomPerson = []
def getPpl():
	global randomPerson
	## select keyword from db.json
	keyword = data["keywords"][random.randint(0,len(data["keywords"])-1)]
	print("Searching keyword is %s" % keyword)

	## trying to find ppl to mention them.
	searchUrl = "https://api.twitter.com/1.1/search/tweets.json?q=%s&vertical=news" % keyword
	r = requests.get(searchUrl, auth=auth)
	searchData = json.loads(r.text) #request to json

	randomPerson = [] #clearing array.

	## getting usernames and putting them in to array.
	count = 0
	while count < 15:
		randomPerson.append(searchData["statuses"][count]["user"]["screen_name"])
		count += 1

## loading tweets
dailyTweets = data["dailyTweets"]
mentionTweets = data["mentionTweets"];

getPpl() ## getting ppl.

## setting up api
url = "https://api.twitter.com/1.1/statuses/update.json?status=%s"

## post daily tweet
def postDailyTweet():
	randomTweet = dailyTweets[random.randint(0,len(dailyTweets)-1)]
	r = requests.post(url % quote_plus(randomTweet), auth=auth)
	if r.status_code == 403:
		print("%s - Tweet Duplicated." % time.ctime())
	else:
		print("%s - Daily Tweet tweeted." % time.ctime())

## post mention tweet
## url encoding (@ = %40)
randomMentionPersonCount = 0
def postMentionTweet():
	global randomMentionPersonCount #local variable to global variable
	randomTweet = mentionTweets[random.randint(0,len(mentionTweets)-1)]
	randomMentionPerson = randomPerson[randomMentionPersonCount]
	r = requests.post(url % "%40" + randomMentionPerson + " " + quote_plus(randomTweet), auth=auth)
	if r.status_code == 403:
		print("%s - Mention Tweet Duplicated." % time.ctime())
	else:
		print("%s - Mention Tweet tweeted to %s." % (time.ctime(), randomMentionPerson))
	randomMentionPersonCount += 1
	if randomMentionPersonCount == 14:
		print("Refreshing people..")
		getPpl()
		randomMentionPersonCount = 0


## action time..
limit = 0
while limit < 1:
	postDailyTweet()
	print("Waiting 15 min for next tweet.")
	time.sleep(901) #wait 15 min for next tweet.
	postMentionTweet()
	print("Waiting 15 min for next tweet.")
	time.sleep(901) #wait 15 min for next tweet.
