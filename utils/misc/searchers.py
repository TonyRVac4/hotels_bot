from config_data.config import headers, url, querystring
from utils.misc.api_request import request_to_api
import re
import json


def city_founding(city):
    querystring.update(query=city)
    response = request_to_api(url=url, headers=headers, querystring=querystring)

    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

        cities = list()
        for dest_id in suggestions['entities']:
            cities.append({'city_name': dest_id['name'], 'destination_id': dest_id['destinationId']})
        return cities
    else:
        return None
