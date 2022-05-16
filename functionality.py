import json
import re

import requests
from bs4 import BeautifulSoup

config_url = "https://nekretninecrikvenica.net/listings/results?id_transaction={transaction}&location={location}"
# domain_url = 'https://nekretninecrikvenica.net'


def get_loc_from_json(json_content, parent_key=False):
    """Return a list of locations(If parent_key==True --> return a list of head locations)

    json_content: JSON content of locations
    parent_key: boolean key to pull all/main locations(optional attribute)
    """
    loc_list = []
    if parent_key:
        for element in json_content:
            if not element['parent_location']:
                loc_list.append(element['name'].replace(' ', '+'))
    else:
        return [element['name'].replace(' ', '+') for element in json_content]
    return loc_list


def urls_generator(loc_list):
    """Return a final JSON construction of urls

    loc_list: list of locations
    """
    sale_strict, rent_strict = [], []
    for location in loc_list:
        sale_strict.append(
            {
                "url": config_url.format(transaction=1, location=location),
                "meta": {
                    "type": "sale_strict",
                    "location_ids": ["CONSTANT"]
                }
            })
        rent_strict.append(
            {
                "url": config_url.format(transaction=2, location=location),
                "meta": {
                    "type": "rent_strict",
                    "location_ids": ["CONSTANT"]
                }
            })
    return sale_strict + rent_strict


def get_urls(domain):
    response = requests.get(domain)
    soup = BeautifulSoup(response.content, 'html.parser')

    loc_in_script = soup.find("script", text=re.compile("mydropdowns")).string
    loc_raw_json = re.search(r'data:([^\]]+\])', loc_in_script).group(1)
    loc_json = json.loads(loc_raw_json)
    locations = get_loc_from_json(loc_json)
    raw_json = urls_generator(locations)

    return json.dumps(raw_json, indent=4)
