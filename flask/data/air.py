from datetime import datetime, timedelta
from itertools import combinations
from dotenv import load_dotenv
from requests import get
import os

load_dotenv()

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_BASE_URL = os.getenv('API_BASE_URL')
API_KEY = os.getenv('API_KEY')


def airports():
    url = f'{API_BASE_URL}airports/pCuwoCxInvjSutnq9Dp7WpKaqrHqOzvw'
    resp = get(
        url,
        auth=(API_USER, API_PASSWORD)
    )

    return resp.json()


def search(departure_airport, arrival_airport, departure_date):
    url = f'{API_BASE_URL}search/{API_KEY}/:departure_airport:/:arrival_airport:/'

    url = url.replace(':departure_airport:', departure_airport)
    url = url.replace(':arrival_airport:', arrival_airport)
    url = f'{url}{departure_date:%Y-%m-%d}'

    resp = get(
        url,
        auth=(API_USER, API_PASSWORD)
    )

    return {
        'data': resp.json(),
        'url': url
    }


def combine(arr, r=2):
    return list(combinations(arr, r))
