from config_data.config import headers
from requests_to_api.api_request import main_request
import re
import json


def city_founding(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    try:
        response = main_request(url=url, headers=headers, params=querystring)
        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, response.text)
        if find:
            suggestions = json.loads(f"{{{find[0]}}}")

            cities = list()
            for dest_id in suggestions['entities']:
                cities.append({'city_name': dest_id['name'], 'destination_id': dest_id['destinationId']})
            else:
                return cities
        else:
            raise Exception
    except Exception:
        return None


def hotel_founding(id, checkIn, checkOut, quan_hotels, sorting):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": id, "pageNumber": "1", "pageSize": "25",
                   "checkIn": checkIn, "checkOut": checkOut, "adults1": "1",
                   "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"}
    try:
        response = main_request(url=url, headers=headers, params=querystring)
        pattern = r'(?<=,)"results":.+?(?=,"pagination")'
        find = re.search(pattern, response.text)
        if find:
            data = json.loads(f"{{{find[0]}}}")
            hotels = list()
            sorted_data = sorting(data['results'])
            for count, i_hotel in enumerate(sorted_data):
                if count < quan_hotels:
                    hotels.append({'hotel_name': i_hotel['name'],
                                   'address': i_hotel['address']['streetAddress'], # добавить: как далеко расположен от центра
                                   'price_per_day': i_hotel['ratePlan']['price']['current'],
                                   'full_price': i_hotel['ratePlan']['price']['fullyBundledPricePerStay'],
                                   'destination_id': i_hotel['id']})
                else:
                    return hotels
        else:
            raise Exception
    except Exception:
        return None


photos_url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
photos_querystring = {"id": str}  # id отеля
