import tweepy

class TwitterBartolo():           
    def __init__(self, *args, **kwargs):
        super(TwitterBartolo, self).__init__(*args, **kwargs)

        consumer_key = "dNY7kBN9ptV6IUn49lSlkerN0"
        consumer_secret = "Gd1SqdmY0tZzD1Rttxusrhm8w5OI2N5pMKHujYCC2dBAT3aRKH"

        access_token = "1254462238460710915-c5JweuGrookBEQfTFjkuXWLXyI9OoV"
        access_token_secret = "0YLI7ULFMEJg1DBFc0B9qj0AfYNe81qfz6I4qq86bIoVz"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def sendTweet(self, msg):
        self.api.update_status(msg)