# AegisBot
Human supervised twitter bot detection

Currently running on command line, I recommend running it in pycharm. 
Packages needed are tweepy, copy, datetime, schedule, and time.  
Access keys have been removed, so as to prevent my account from being compromised.

To use this, you will need to setup your own twitter account, and apply for api access.
You will need to add these lines of code to any function that accesses the twitter api.

    consumer_key = "your key"
    consumer_secret = "your key"
    access_token = "your key"
    access_token_secret = "your key"
    
 A comment labeled (# Keys used to access the twitter api) is provided in any fucntion that 
 requires the keys.
 
 This program is capable of auto tweeting, manual tweeting, auto collection, and manual collection.
 The results of the collection process write to a file and store that file in a specified folder.
 
 You will need to alter these lines to your desired destinations.
 
    file_destinationP = "C:/Users/Timmy/Desktop/AegisBot/Positives/"
    file_destinationN = "C:/Users/Timmy/Desktop/AegisBot/Negatives/"
    
 Currently the program is running with zero false negatives and several false positives.
 It is recommended that you inspect every positive and validate it for yourself.  
