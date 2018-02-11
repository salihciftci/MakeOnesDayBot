package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"time"
)

// Struct for "db.json"
type Database struct {
	Keywords      []string `json:"keywords"`
	MentionTweets []string `json:"mentionTweets"`
	Tweets        []string `json:"tweets"`
}

var (
	people Tweet
)

func main() {
	//Checking Auth
	if verify() == 200 {
		log.Println("Auth succesful.")
	} else {
		log.Println("Auth unsuccesful.")
		os.Exit(1)
	}

	//Reading Json File
	file, err := ioutil.ReadFile("./db.json")
	if err != nil {
		log.Println(err.Error())
	}

	//Json file to slice
	var db Database
	json.Unmarshal(file, &db)

	// Main loop for Tina
	for {
		//Tweeting to homeline
		if update(db.Tweets[rand.Intn(len(db.Tweets))]) == 200 {
			log.Println("Tweeted to homeline")
		} else {
			log.Println("Couldn't tweet to homeline, skipping.")
		}

		time.Sleep(15 * time.Minute)

		//Finding people
		query := db.Keywords[rand.Intn(len(db.Keywords))]
		json.Unmarshal(search(query), &people)

		//Tweeting to everyone in slice
		for i := 0; i < len(people.Statuses); i++ {
			//Randomly getting tweet from db slice
			tweet := db.MentionTweets[rand.Intn(len(db.MentionTweets))]
			//Mentioning to someone.
			if update("@"+people.Statuses[i].User.ScreenName+" "+tweet) == 200 {
				log.Println("Mention tweeted.")
			} else {
				log.Println("Couldn't tweeted, skipping")
			}

			time.Sleep(15 * time.Minute)
		}
	}
}
