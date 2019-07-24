# -*- coding: utf-8 -*-

from math import radians, cos, sin, asin, sqrt
from decimal import Decimal


def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    km = 6371 * c

    value = Decimal(str(km))

    return value


def flight_time(departure_time, arrival_time):
    value = Decimal(
        str((arrival_time - departure_time).seconds / 3600)
    )

    return value


def average_speed(distance, flight_time):
    value = Decimal(distance / flight_time)

    return value


def price_per_km(fare_price, distance):
    value = Decimal(Decimal(fare_price) / distance)
    
    return value
