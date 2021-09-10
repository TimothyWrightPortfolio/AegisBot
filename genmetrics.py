import copy
import tweepy
import tweet_class


# Collects all URLs in the provided string
def collect_urls(string):
    # Splits the string on whitespace and names it tweet
    tweet = str.split(string)

    # Creates an empty array for work
    url_array = []

    # For each string in the tweet array
    for strng in tweet:

        # If length is greater than 4
        if len(strng) > 4:

            # Check first four chars to see if it is a link
            if strng[0] == "h" and strng[1] == "t" and strng[2] == "t" and strng[3] == "p":

                # If it is a link appends it to url_array
                url_array.append(strng)
                continue

            # Check the first four chars to see if it is a link
            elif strng[0] == "H" and strng[1] == "T" and strng[2] == "T" and strng[3] == "P":

                # If it is a link appends it to url_array
                url_array.append(strng)
                continue
            else:
                continue
    # Returns the array of discovered URLs
    return url_array


# Collects each hashtag used in the tweet
def collect_hashtags(string):
    # Creates empty array for work
    hashtag_array = []

    # Splits the string on whitespace
    strng = str.split(string)

    # for each string in the split tweet
    for each in strng:

        # If the string is longer than one char
        if len(each) > 1:

            # If the first char is a #
            if each[0] == "#":

                # Append the hashtag to the array
                hashtag_array.append(each)
                continue
            else:
                continue
        else:
            continue
    # Returns the array of collected hashtags
    return hashtag_array


# Collects every @ mention in the provided tweet
def collect_mentions(string):
    # Creates an empty array for work
    mentions_array = []

    # Splits the tweet on whitespace
    strng = str.split(string)

    # For each string in the split tweet
    for each in strng:

        # If its greater than one char
        if len(each) > 1:

            # if the string starts with @
            if each[0] == "@":

                # Append the string to the array
                mentions_array.append(each)
                continue
            else:
                continue
        else:
            continue
    # Returns the array of collected mentions
    return mentions_array


# Divides the tweet into 8 roughly equal segments
# Takes each segment and runs it through the hash function
def generate_hash(string):
    # Creates an array for work
    stringarray = []

    # Sets x to be the length of the provided tweet divided by 8
    # For tweets not divisible by 8, the quotient is converted into an integer
    x = int(len(string) / 8)

    # sets y to be the length of the string
    y = len(string)

    # Partitions the tweet into 8 equal segments of length x
    for i in range(0, y, x):
        partition = string[i:i + x]

        # Appends the string to the array
        stringarray.append(partition)

    # Converts each string in the array into its hash value
    hash1 = hash(stringarray[0])
    hash2 = hash(stringarray[1])
    hash3 = hash(stringarray[2])
    hash4 = hash(stringarray[3])
    hash5 = hash(stringarray[4])
    hash6 = hash(stringarray[5])
    hash7 = hash(stringarray[6])
    hash8 = hash(stringarray[7])

    # Returns each hash in the order listed
    return hash1, hash2, hash3, hash4, hash5, hash6, hash7, hash8


# Uses the provided profile name
# Looks at that profiles num most recent tweets
# calls the various functions to collect mentions, @, #, time, hash values
def generate_metrics(name: object, num):
    # Keys used to access the twitter api


    # Initiates OAuthHandler and passes the keys into the object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Confirms authorization and sets the rate limit to not exceed twitters rate limit for get requests
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Performs the search and names the result results
    results = api.user_timeline(screen_name=name, count=num, include_rts=False, tweet_mode='extended', language='en')

    # Creates a new profile object with the provided name
    new_user = tweet_class.profile(name)

    # If the account has fewer than num tweets
    if len(results) < num:

        # Inform the user
        print("\n")
        print(name + "Has fewer than " + str(num) + " tweets on their account")
        return

    else:

        # For each tweet collected
        for tweet in results:

            # If the length of the tweet is less than 20 chars, ignore it
            # For reference 20 chars is roughly 4 words
            if len(tweet.full_text) < 20:
                continue
            else:

                # Appends the full text of the tweet to the tweet_array of the new_user object
                new_user.tweet_array.append(tweet.full_text)

                # Sets new_user length field to be the length of the tweet
                tweet_length = len(tweet.full_text)

                # Creates a new instance of the metrics class with
                metrics = tweet_class.metrics(tweet.created_at, tweet_length)

                # Collects the urls and stores them in the url field
                metrics.urls = collect_urls(tweet.full_text)

                # Collects the number of words in the tweet and stores them in the NumOfWords field
                metrics.NumOfWords = int(len(str.split(tweet.full_text)))

                # Collects the mentions and stores them in the mentions field
                metrics.mentions = collect_mentions(tweet.full_text)

                # Collects the hashtags and stores them in the hashtag field
                metrics.hashtags = collect_hashtags(tweet.full_text)

                # Takes the hash values and stores them in the corresponding field
                metrics.hash1, metrics.hash2, metrics.hash3, metrics.hash4, metrics.hash5, metrics.hash6, metrics.hash7, metrics.hash8 = generate_hash(
                    tweet.full_text)

                # appends the metrics object to the metrics_array field in the profile class
                new_user.metrics_array.append(metrics)
                continue

        # Calls the generate_report() function and passes the profile object
        generate_report(new_user)

    return


# Determine whether the account has recently tweeted urls or duplicate urls
def examine_urls(array_urls: object):
    # creates a placeholder int for scoring
    x = 0

    # Creates empty array for work
    url_array = []
    temp_url = copy.deepcopy(array_urls)
    # for each entry in the profile objects metric array
    for each_metric in temp_url:

        if not each_metric.urls:
            continue

        # Creates a copy of the url array
        url_copy = copy.deepcopy(each_metric.urls)

        # Appends the copy to the working array
        url_array.append(url_copy)


    # If there are no urls exit the function
    if not url_array:
        return x


    # While there are still items in the array

    while url_array:
        # Adds 1 to the current score
        x = x + 1

        # Pops a url off the url array
        url = url_array.pop()

        # Checks each url for duplicates
        for urls in url_array:
            # For each duplicate increase current score by 2
            if url == urls:
                x = x + 2
    # Return the score
    return x


# Checks whether the account has recently tweeted with duplicate hashtags
def examine_hashtags(array_hashtags: object):
    # Sets a placeholder score
    x = 0

    hashtag_array = []
    temp_hashtag = copy.deepcopy(array_hashtags)
    # For each metric object
    for each_metric in temp_hashtag:

        if not each_metric.hashtags:
            continue

        # Create a copy of the hashtag_array for work
        hashtag_copy = copy.deepcopy(each_metric.hashtags)
        hashtag_array.append(hashtag_copy)

    # If the array is empty exit the function
    if not hashtag_array:
        return x

    # While there are still items in the array
    while hashtag_array:

        # pop the hashtag at I off the array
        hashtag = hashtag_array.pop()

        # For each remaining hashtag check if its a duplicate
        for string in hashtag_array:

            # If it is a duplicate increase the score by 1
            if hashtag == string:
                x = x + 1
    # Return the score
    return x


def examine_mentions(array_mentions: object):

    # Sets a placeholder score
    x = 0

    # Creates an empty array for work
    mentions_array = []
    temp_mentions = copy.deepcopy(array_mentions)

    # For each metric object
    for each_metric in temp_mentions:

        if not each_metric.mentions:
            continue

        # Create a copy of the mentions array
        mentions_copy = copy.deepcopy(each_metric.mentions)

        # Append that copy to the working array
        mentions_array.append(mentions_copy)

    # If the array is empty
    if not mentions_array:
        return x


    # While the array is not empty
    while mentions_array:

        # Pop the mention at mentions_array[i}
        mention = mentions_array.pop()

        # Add a point for each duplicate mention
        for string in mentions_array:
            if string == mention:
                x = x + 1

    # Return the score
    return x


def examine_length(array_len: object):

    # Set placeholder score
    x = 0

    # Create a copy of the metrics array
    length_array = copy.deepcopy(array_len)

    # While length_array is not empty
    while length_array:

        # Pop length_array(i)
        length = length_array.pop()

        # For each item in the metrics array
        for each in length_array:

            # If the char length is equal add 3
            if length.length == each.length:
                x = x + 2

            # If the word length is equal add 3
            if length.NumOfWords == each.NumOfWords:
                x = x + 2

    # Return the score
    return x


def examine_hashvalues(array_hash: object):

    # Set placeholder score
    x = 0


    # Create a copy of the metrics array
    hashes = copy.deepcopy(array_hash)

    # While the array is not empty
    while hashes:

        # Pop hashes[i]
        value = hashes.pop()

        # For each matching hash, increase the score by 3
        for each in hashes:

            if value.hash1 == each.hash1:
                x = x + 3
            if value.hash2 == each.hash2:
                x = x + 3
            if value.hash3 == each.hash3:
                x = x + 3
            if value.hash4 == each.hash4:
                x = x + 3
            if value.hash5 == each.hash5:
                x = x + 3
            if value.hash6 == each.hash6:
                x = x + 3
            if value.hash7 == each.hash7:
                x = x + 3
            if value.hash8 == each.hash8:
                x = x + 3

    # Return the score
    return x


def examine_times(array_time: object):
    score = 0

    # Create two working arrays
    diff_array = []
    temp_array = []
    time_temp = copy.deepcopy(array_time)
    # For each object in the metrics array
    for each_time in time_temp:

        # Set new_time equal to the time_of_tweet field
        new_time = each_time.time_of_tweet

        # Append new_time
        temp_array.append(new_time)
    # Set placeholder score
    x = 0


    # While the temp_array is not empty
    while temp_array:

        # Pop temp_array[i]
        time = temp_array.pop()

        # For each time, take the difference and append them to the diff array
        for times in temp_array:
            z = time - times
            diff_array.append(z)

    # While the diff array is not empty
    while diff_array:

        # Pop diff_array[i]
        diff = diff_array.pop()
        # For each duplicate difference add 3 to the score
        for difference in diff_array:
            if diff == difference:
                score = score + 3

                continue
            else:
                continue

    # Return the score
    return score


def generate_report(user: object):

    # Update the score based on URLS
    user.score = user.score + examine_urls(user.metrics_array)

    # Update the score based on hashtags
    user.score = user.score + examine_hashtags(user.metrics_array)

    # Update the score based on mentions
    user.score = user.score + examine_mentions(user.metrics_array)

    # Update the score based on lengths
    user.score = user.score + examine_length(user.metrics_array)

    # Update the score based on the hash values
    user.score = user.score + examine_hashvalues(user.metrics_array)

    # Update the score based on time
    user.score = user.score + examine_times(user.metrics_array)

    # The desired destination for reports on user profiles
    file_destinationP = "C:/Users/Timmy/Desktop/Class/Positives/"
    file_destinationN = "C:/Users/Timmy/Desktop/Class/Negatives/"

    # Sets the filename to be user_name.txt
    username = user.user_name + ".txt"

    # Sets the full file path
    if user.score >= 40:
        complete_filename = file_destinationP + username
    else:
        complete_filename = file_destinationN + username

    # Opens a file with the given path for writing
    f = open(complete_filename, "w", encoding="utf-8")

    # Writes the profiles twitter handle
    f.write(user.user_name + "\n" + "\n")

    # Writes the users score
    f.write(str(user.score) + "\n" + "\n")

    # If the score is above the threshold, recommend human examination
    if user.score >= 40:
        f.write("This user has is likely a bot.  Human examination is recommended. \n" + "\n")
        print("\n")
        print(user.user_name + ": It is recommended to examine this user")

    # Else no recommendation
    else:
        f.write("This user is likely a human.  No further steps necessary. \n" + "\n")

    # Write to file each tweet that was examined
    for tweet in user.tweet_array:
        f.write(tweet + "\n" + "\n")

    # Close the file
    f.close()

    # Exit the function
    return
