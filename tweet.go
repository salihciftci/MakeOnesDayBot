package main

import (
	"github.com/dghubble/oauth1"
	"io/ioutil"
	"log"
	"net/url"
	"os"
)

// Setting up Twitter client
var (
	consumerKey    = ""
	consumerSecret = ""
	tokenKey       = ""
	tokenSecret    = ""

	config = oauth1.NewConfig(consumerKey, consumerSecret)
	token  = oauth1.NewToken(tokenKey, tokenSecret)

	client = config.Client(oauth1.NoContext, token)
)

// Authentication client
func verify() int {
	path := "https://api.twitter.com/1.1/account/verify_credentials.json"
	resp, err := client.Get(path)

	if err != nil {
		log.Println(err.Error())
		os.Exit(1)
	}
	defer resp.Body.Close()

	return resp.StatusCode
}

// Tweeting to twitter with client
func update(status string) int {
	path := "https://api.twitter.com/1.1/statuses/update.json"
	resp, err := client.PostForm(path, url.Values{"status": {status}})

	if err != nil {
		log.Println(err.Error())
	}
	defer resp.Body.Close()
	return resp.StatusCode
}

// Searching People with query keyword (from db.json)
func search(query string) []byte {
	path := "https://api.twitter.com/1.1/search/tweets.json?q=" + query
	resp, err := client.Get(path)

	if err != nil {
		log.Println(err.Error())
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Println(err.Error())
	}

	return body
}
