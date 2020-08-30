import tweepy

consumer_key = "pnZ6U9Yciuls5Qif2hzdtVeRd"
consumer_secret = "ftpQvB3PSLn1gZ4J3IdJMITocU17MNYAhTXid2Cj5nXTfqgkpz"

access_token = "3386231271-Bd5pZxtfZNnwbJIg5vQ1vkAZ6L4kiYB7uQPvwcr"
access_token_secret = "X5FhhQzt7Yh5kwwjq3DEpeBL0M8Il0tWocbfhedOpm94d"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

api.update_status('Visita nuestro Sitio https://bartolo.org')