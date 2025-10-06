import requests
from bs4 import BeautifulSoup

def get_weather_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text