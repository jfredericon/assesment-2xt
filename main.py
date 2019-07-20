from datetime import datetime, timedelta
from utils import operations
from data import air
from pprint import pprint

data = air.airports()

# print(len(data.keys()))

comb = air.combine(data.keys())

# print(len(comb))

comb = comb[:20]
for item in comb:

    data = {}

    departure_airport = item[0]
    arrival_airport = item[1]

    resp = air.search(departure_airport, arrival_airport)

    data['url'] = resp['url']

    from_city = resp['data']['summary']['from']
    to_city = resp['data']['summary']['to']

    lon1 = from_city['lon']
    lat1 = from_city['lat']
    lon2 = to_city['lon']
    lat2 = to_city['lat']

    distance = operations.haversine(lon1, lat1, lon2, lat2)

    data['distance'] = distance

    sorted_list_aircrafts = sorted(
        resp['data']['options'], key=lambda item: item['fare_price']
    )

    data['lowest_value'] = sorted_list_aircrafts[0]['fare_price']
    data['aircraft_model'] = sorted_list_aircrafts[0]['aircraft']['model']

    for modelo in sorted_list_aircrafts:
        departure_time = datetime.strptime(
            modelo['departure_time'], '%Y-%m-%dT%H:%M:%S'
        )

        arrival_time = datetime.strptime(
            modelo['arrival_time'], '%Y-%m-%dT%H:%M:%S'
        )

        flight_time = operations.flight_time(departure_time, arrival_time)

        average_speed = operations.average_speed(distance, flight_time)

        fare_price = modelo['fare_price']

        price_per_km = operations.price_per_km(fare_price, distance)

        # print(
        #     {
        #         'from': from_city['city'],
        #         'to': to_city['city'],
        #         'distance': f'{distance:.2f} km',
        #         'departure_time': f'{departure_time:%d-%m-%Y %H:%M:%S}',
        #         'arrival_time': f'{arrival_time:%d-%m-%Y %H:%M:%S}',
        #         'flight_time': f'{flight_time:.2f} h',
        #         'average_speed': f'{average_speed:.2f} km/h',
        #         'fare_price': f'R$ {fare_price}',
        #         'price_per_km': f'R$ {price_per_km:.2f}'
        #     }
        # )

    pprint(data)
