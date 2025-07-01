import requests
from logger import warn, info
from mappers import  map_address_to_string

def geolocation(address, api_key):
    url = "https://geocode.search.hereapi.com/v1/geocode"
    filter = map_address_to_string(address)
    if not filter:
        warn(f"Filter is empty.Request will not executed")
        return None

    params = {
        "q": filter,
        "apiKey": api_key
    }

    param_log = params.copy()
    param_log.pop('apiKey')
    info(f'Send Request with Params ={param_log}')
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    items = data.get("items", [])
    if not items:
        warn(f"Address={address}. No results found.")
        return None

    position = items[0].get("position", {})

    lat = position.get('lat')
    lng = position.get('lng')

    if lat is None or lng is None:
        warn(f"Invalid coordinates for address={address}")
        return None

    return {
        'id': address.get('id'),
        'coordinates': {
           'longitude': lng,
            'latitude': lat
        }
    }
