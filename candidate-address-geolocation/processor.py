import argparse
from mappers import map_to_settings, map_to_address
from database import AddressRepository
from logger import info,error
from geolocation import geolocation

def process(configs):
    try:
        db_configs = configs.get('database')
        api_key = configs.get('api_key')
        repository = AddressRepository(db_configs)
        info('Get All address records...')
        rows = repository.find_all_address()
        for index, row in enumerate(rows):
            address = map_to_address(row)
            info(f"Address founded: {address}")
            location = geolocation(address, api_key)
            if location:
                address_id = location.get('id')
                coordinates = location.get('coordinates')
                info(f"Geolocation founded: {coordinates}")
                repository.update_coordinates(address_id, coordinates)
                info(f"Update {address_id} record completed")

        info("Finished geolocation searching...")
    except Exception as e:
       error(f'an error occurred while processing the geolocation query for addresses: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument(
        "-H", "--host",
        type=str,
        required=True,
        help="Host where the PostgreSQL server is running (e.g., localhost)"
    )
    parser.add_argument(
        "-P", "--port",
        type=int,
        default=5432,
        help="Port number for the PostgreSQL server (default: 5432)"
    )
    parser.add_argument(
        "-d", "--database",
        type=str,
        required=True,
        help="Name of the PostgreSQL database"
    )
    parser.add_argument(
        "-u", "--user",
        type=str,
        required=True,
        help="PostgreSQL database user"
    )
    parser.add_argument(
        "-p", "--password",
        type=str,
        required=True,
        help="Password for the PostgreSQL user"
    )
    parser.add_argument(
        "-s", "--schema_name",
        type=str,
        required=True,
        help="Name of the PostgreSQL schema to use"
    )
    parser.add_argument(
        "-k", "--geolocation_key",
        type=str,
        required=True,
        help="API key from HERE platform (https://platform.here.com/portal/)"
    )

    args = parser.parse_args()
    settings = map_to_settings(args)

    process(settings)