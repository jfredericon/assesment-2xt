from datetime import datetime, timedelta
from itertools import combinations
from requests import get


USER = 'josefrederico'
PASSWORD = 'szqwoC'
BASE_URL = 'http://stub.2xt.com.br/air/'
API_KEY = 'pCuwoCxInvjSutnq9Dp7WpKaqrHqOzvw'


def airports():
    url = f'{BASE_URL}airports/pCuwoCxInvjSutnq9Dp7WpKaqrHqOzvw'
    resp = get(
        url,
        auth=(USER, PASSWORD)
    )

    return resp.json()


def search(departure_airport, arrival_airport):
    departure_date = datetime.now() + timedelta(days=40)

    url = f'{BASE_URL}search/{API_KEY}/:departure_airport:/:arrival_airport:/'

    url = url.replace(':departure_airport:', departure_airport)
    url = url.replace(':arrival_airport:', arrival_airport)
    url = f'{url}{departure_date:%Y-%m-%d}'
    
    resp = get(
        url,
        auth=(USER, PASSWORD)
    )

    return {
        'data': resp.json(),
        'url': url
    }


def combine(arr, r=2):
    return list(combinations(arr, r))
