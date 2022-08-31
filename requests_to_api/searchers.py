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
            raise ValueError
    except ValueError:
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
            write_to_json(data=data, file_name="hotels.json")
            hotels = list()
            sorted_data = sorting(data['results'])
            if len(sorted_data) <= quan_hotels:
                for i_hotel in sorted_data:
                    hotels.append({'hotel_name': i_hotel['name'],
                                   'address': i_hotel['address']['streetAddress'],
                                   # добавить: как далеко расположен от центра
                                   'price_per_day': i_hotel['ratePlan']['price']['current'],
                                   'full_price': i_hotel['ratePlan']['price']['fullyBundledPricePerStay'],
                                   'destination_id': i_hotel['id']})
            else:
                for count, i_hotel in enumerate(sorted_data):
                    if count < quan_hotels:
                        hotels.append({'hotel_name': i_hotel['name'],
                                       'address': i_hotel['address']['streetAddress'],
                                       # добавить: как далеко расположен от центра
                                       'price_per_day': i_hotel['ratePlan']['price']['current'],
                                       'full_price': i_hotel['ratePlan']['price']['fullyBundledPricePerStay'],
                                       'destination_id': i_hotel['id']})
                    else:
                        break
            return hotels
        else:
            raise ValueError
    except ValueError:
        return None


def find_photos(id: str):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id}
    headers = {
        "X-RapidAPI-Key": "69aaf56f35msh5d3268f39585685p13490ejsnc32dc9dc8623",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        response = main_request(url=url, headers=headers, params=querystring)
        data = json.loads(response.text)
        write_to_json(data=data, file_name="photos.json")
    except Exception:
        pass


def write_to_json(data, file_name: str):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
