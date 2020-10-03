import tweepy, config, requests, json, time
from datetime import datetime

print('This is a twitter bot')

from config import CONSUMER_KEY
from config import CONSUMER_SECRET
from config import ACCESS_KEY
from config import ACCESS_SECRET
from config import WEATHER_KEY

weather_description = ''
current_temp = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
COMPLETE_URL = BASE_URL + "appid=" + WEATHER_KEY + '&q=' + 'Harrisonburg'
response = requests.get(COMPLETE_URL)
x = response.json()
def get_weather():
    if x['cod'] != '404':
        y = x['main']
        #convert Kelving to Farhenheit
        current_temp = round((y['temp'] - 273.15) * 9/5 + 32, 2)
        z = x['weather']
        weather_description = z[0]['description']
    else:
        print('City Not Found')

def tweet():
    print('Checking time')
    try:
        minutes = datetime.now().minute
        if minutes == 0 or minutes == 13:
            print('Tweeting weather update')
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    api.destroy_status(status.id)
                except:
                    pass
            api.update_status(weather_description + ' with a current temperature of ' + str(current_temp) + 
                ' degrees Fahrenheit in Harrisonburg, VA')
    except tweepy.TweepError as e:
        print(e.reason)

while True:
    get_weather()
    tweet()
    time.sleep(60)