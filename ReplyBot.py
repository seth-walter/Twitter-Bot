import tweepy, time, requests, json, config
# author Seth Walter
# Twitter bot that replies to tweets that mention the bot and the 
# hashtag 'weather' with the current temperature of Harrisonburg, VA.
# TODO add functionality for more cities, add descriptive weather to tweets
# also add daily tweets about the weather for JMU.

##CURRENTLY NOT FUNCTIONAL DUE TO TWITTER RESTRICTIONS ON NEW ACCOUNTS

print("This is a twitter Bot")

from config import CONSUMER_KEY
from config import CONSUMER_SECRET
from config import ACCESS_KEY
from config import ACCESS_SECRET
from config import WEATHER_KEY

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
COMPLETE_URL = BASE_URL + "appid=" + WEATHER_KEY + '&q=' + 'Harrisonburg'
response = requests.get(COMPLETE_URL)
x = response.json()
if x['cod'] != '404':
    y = x['main']
    #convert Kelvin to Farhenheit
    current_temp = round((y['temp'] - 273.15) * 9/5 + 32)
    z = x['weather']
    weather_desciption = z[0]['description']
else:
    print('City Not Found')
    
FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#weather' in mention.full_text.lower():
            print('found weather')
            api.update_status('@' + mention.user.screen_name + ' It is currently ' +
                str(current_temp) + " degrees Fahrenheit in Harrisonburg, VA", mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)
