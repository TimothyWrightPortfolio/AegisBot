import tweepy
import datetime
import schedule
import time
import genmetrics


# Takes user input and posts it as a tweet on the given twitter account
def author_tweet():
    # Keys used to access the twitter api


    # Initiates OAuthHandler and passes the keys into the object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Checks authorization to access api
    api = tweepy.API(auth)

    # Take input for the desired tweet
    text = input("Please type the body of your Tweet: ")

    # Posts the tweet
    api.update_status(text)

    # Confirms tweet was posted
    print("Tweet posted Successfully")
    return


# Takes user input for time interval and desired tweet text
# Posts the desired text every time the time interval is reached
def auto():
    # Takes user input for the tweets text
    which = input("Would you like to Collect or Tweet? ")

    if which == "collect":
        interval = input("How often, in minutes, would you like this to repeat? ")
        search_terms = input("Please enter your search terms: ")
        numoprofiles = int(input("How many profiles would you like to examine? "))
        numotweets = int(input("How many tweets from each profile? "))
        after_date = input("How far back would you like to look?: YYYY-MM-DD ")
        schedule.every(int(interval)).minutes.do(auto_collect, numoprofiles, numotweets, search_terms, after_date)

    elif which == "tweet":

        # Takes user input for the desired time interval
        timeinterval = input("How often would you like this task to repeat?  Hours, Minutes, or Days? ")

        # If the user wants the tweet to be posted every X hours
        if timeinterval == "hours":
            # Takes user input for the desired number of hours
            interval = input("What interval would you like? (in hours using digits): ")
            text = input("Please input the body of your tweet: ")

            # Schedule the task
            schedule.every(int(interval)).hours.do(tweet_auto, text)

        # If the user wants the tweet posted every X days
        elif timeinterval == "days":
            # Takes user input for the number of days
            interval = input("What interval would you like? (in days using digits): ")
            text = input("Please input the body of your tweet: ")
            # Schedule the task
            schedule.every(int(interval)).days.do(tweet_auto, text)

        # If the user wants the tweet posted every X minutes
        elif timeinterval == "minutes":
            print("Warning!: If choosing less than 15 minutes, twitter may reject the tweet")

            # Takes user input for the number of minutes
            interval = input("What interval would you like? (in minutes using digits): ")

            # Takes user input for the body of the tweet
            text = input("Please input the body of your tweet: ")
            # Schedule the task
            schedule.every(int(interval)).minutes.do(tweet_auto, text)

    # Infinite loop designed to check for a pending task, and perform the task if it is ready
    while True:
        # Checks for and runs the pending task
        schedule.run_pending()

        # Pauses the execution of the program for 2 minutes
        time.sleep(60)


# Called by the auto_tweet function
# Posts the desired tweet text with the current time appended to the end
def tweet_auto(body):
    # Gets the current date and time
    current_time = datetime.datetime.now()

    # Converts the datetime object into a string
    time_string = current_time.strftime("%H:%M:%S.%f - %b %d %Y")

    # Appends the current time to the end of body
    text = body + " " + time_string

    # Keys used to access the twitter api


    # Initiates OAuthHandler and passes the keys into the object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Checks authorization
    api = tweepy.API(auth)

    # Posts the tweet
    api.update_status(text)

    # Alerts the user that the tweet was posted
    print("Tweet Successful")
    return


# Takes user input for search terms and a date you would like to start searching from
# Uses those searches to collect x profile names
# Calls the generate_metrics() function to begin analyzing each profile
def collect_profiles():
    # Keys used to access the twitter api


    # Initiates OAuthHandler and passes the keys into the object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Checks authorization, makes sure search doesnt surpass twitters rate limit for GET requests
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Takes input for search terms
    search_words = input("Please type in search terms: ")

    # Appends a filter to the provided search terms
    search_terms = search_words + " -filter:retweets"

    # Takes input for the desired date
    after_date = input("How far back would you like to look?: YYYY-MM-DD ")

    # Takes input for the desired number of profiles
    numberOfProf = int(input("How many profiles would you like to examine? :"))

    # Performs the search and names the result results
    results = tweepy.Cursor(api.search, q=search_terms, lang="en", since=after_date).items(numberOfProf)

    # Takes input for the number of tweets to be examined from each profile
    num = int(input("How many past tweets would you like to examine? : "))

    # For each tweet in results, captures profile name and passes it to the generate_metrics() function
    for tweet in results:
        genmetrics.generate_metrics(tweet.user.screen_name, num)

    return


def auto_collect(profile_num, tweet_num, search_term, date):
    # Keys used to access the twitter api
8

    # Initiates OAuthHandler and passes the keys into the object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Checks authorization, makes sure search doesnt surpass twitters rate limit for GET requests
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Appends a filter to the provided search terms
    search_terms = search_term + " -filter:retweets"

    results = tweepy.Cursor(api.search, q=search_terms, lang="en", since=date).items(profile_num)

    for tweet in results:
        genmetrics.generate_metrics(tweet.user.screen_name, tweet_num)

    return
