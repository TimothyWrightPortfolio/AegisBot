class profile:
    def __init__(self, user_name):
        self.user_name = user_name
        self.score = 0
        self.metrics_array = []
        self.tweet_array = []


class metrics:
    def __init__(self, time_of_tweet, length):
        self.time_of_tweet = time_of_tweet
        self.length = length
        self.NumOfWords = 0
        self.mentions = []
        self.hashtags = []
        self.urls = []
        self.hash1 = 0
        self.hash2 = 0
        self.hash3 = 0
        self.hash4 = 0
        self.hash5 = 0
        self.hash6 = 0
        self.hash7 = 0
        self.hash8 = 0
