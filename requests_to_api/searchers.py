import re
import json
from config_data.config import headers
from requests_to_api.api_request import main_request
from loguru import logger


logger.add('logs/searchers.log', level='DEBUG')


def find_cites(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    try:
        response = main_request(url=url, headers=headers, params=querystring)
        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, response.text)
        if find:
            suggestions = json.loads(f"{{{find[0]}}}")
            if suggestions != {'entities': []}:
                cities = list()
                for dest_id in suggestions['entities']:
                    caption = dest_id["caption"].split(", ")
                    city_name = dest_id['name']
                    if len(city_name) < 30:
                        if len(f"{city_name} - {caption[-2]}") < 30:
                            city_name += f" - {caption[-2]}"
                            if len(f"{city_name} {caption[-1]}") < 30:
                                city_name += f" {caption[-1]}"
                        cities.append({'city_name': city_name, 'destination_id': dest_id['destinationId']})
                else:
                    return cities
            else:
                raise ValueError(f"Ошибка поиска городов\n"
                                 f"city = '{city}' | find = {find} | response code: {response.status_code}\n")
        else:
            raise ValueError(f"Ошибка поиска городов\n"
                             f"city = '{city}' | find = {find} | response code: {response.status_code}\n")
    except ValueError as exp:
        logger.debug(exp)
        return None
    except Exception as exp:
        logger.debug(exp)
        return None


def find_hotels(id, checkIn, checkOut, quan_hotels, sorting):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": id, "pageNumber": "1", "pageSize": "25",
                   "checkIn": checkIn, "checkOut": checkOut, "adults1": "1",
                   "sortOrder": sorting, "locale": "en_US", "currency": "USD"}
    hotels = list()

    try:
        response = main_request(url=url, headers=headers, params=querystring)
        pattern = r'(?<=,)"results":.+?(?=,"pagination")'
        find = re.search(pattern, response.text)
        if find:
            data = json.loads(f"{{{find[0]}}}")
            if data['results']:
                quan_day = (checkOut - checkIn).days
                for i_hotel in data['results']:
                    if len(hotels) < quan_hotels and "streetAddress" in i_hotel["address"].keys():
                        hotels.append({"hotel_name": i_hotel["name"],
                                       "address": i_hotel["address"]["streetAddress"],
                                       # добавить: как далеко расположен от центра
                                       "price_per_day": i_hotel["ratePlan"]["price"]["current"],
                                       "full_price": int(i_hotel["ratePlan"]["price"]["exactCurrent"] * quan_day),
                                       "quan_day": quan_day,
                                       "destination_id": i_hotel["id"]})
            else:
                raise ValueError(f"Ошибка поиска отелей\n"
                                 f"destinationId: {id} | find = {find} | response code: {response.status_code}\n")
        else:
            raise ValueError(f"Ошибка поиска отелей\n"
                             f"destinationId: {id} | find = {find} | response code: {response.status_code}\n")
    except ValueError as exp:
        logger.debug(exp)
    except Exception as exp:
        logger.debug(exp)
    finally:
        return hotels


def find_photos(hotel: dict, quan_photo: int):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    hotels_url = list()

    try:
        querystring = {"id": hotel["destination_id"]}
        response = main_request(url=url, headers=headers, params=querystring)
        find = json.loads(response.text)
        if find["hotelImages"]:
            for photo in find["hotelImages"]:
                if len(hotels_url) < quan_photo:
                    url = photo["baseUrl"].replace("{size}", "w")
                    hotels_url.append(url)
                else:
                    break
        else:
            raise ValueError(f"Ошибка поиска фотографий\n"
                             f"hotel = {hotel} | find = {find} | response code: {response.status_code}\n")
    except ValueError as exp:
        logger.debug(exp)
    except Exception as exp:
        logger.debug(exp)
    finally:
        return hotels_url
