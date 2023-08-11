from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_picture_url(query):

    """
    Get the URL of a picture from the Pexels API
    """

    url = f"https://api.pexels.com/v1/search?query={query}"
    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(url, headers=headers)
    api_dict = response.json()
    return api_dict['photos'][0]['src']['original']


def get_weather_data(city, state):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},US&appid={OPEN_WEATHER_API_KEY}"

    response = requests.get(url)
    api_location = response.json()
    lat = api_location[0]["lat"]
    lon = api_location[0]["lon"]

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    response = requests.get(weather_url)
    current_weather = response.json()

    details = {
        "temperature": current_weather["main"]["temp"],
        "weather_description": current_weather["weather"][0]["description"],
    }

    return details
