import tweepy, config, requests, json, time
from datetime import datetime
# author Seth Walter
# Twitter bot that tweets the weather and a short description of Harrisonburg, VA
# every 30 minutes.
# TODO add functionality for more cities

print('This is a twitter bot')

#Import API keys from hidden file
from config import CONSUMER_KEY
from config import CONSUMER_SECRET
from config import ACCESS_KEY
from config import ACCESS_SECRET
from config import WEATHER_KEY

#Setup twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Setup OpenWeatherMap API
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
COMPLETE_URL = BASE_URL + "appid=" + WEATHER_KEY + '&q=' + 'Harrisonburg'

#Function to tweet weather
def tweet():
    print('Checking time')
    response = requests.get(COMPLETE_URL)
    x = response.json()
    #Getting weather data from OpeanWeatherMap
    if x['cod'] != '404':
        y = x['main']
        #convert Kelvin to Farhenheit
        current_temp = round((y['temp'] - 273.15) * 9/5 + 32, 1)
        z = x['weather']
        weather_description = z[0]['description']
    else:
        print('City Not Found')
    try:
        minutes = datetime.now().minute
        if minutes == 0 or minutes == 30:
            print('Tweeting weather update')
            #Deletes current tweet and replaces it with newest tweet
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
    tweet()
    time.sleep(60)