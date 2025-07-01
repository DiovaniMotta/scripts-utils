import psycopg2
from logger import info, warn

class AddressRepository:

    def __init__(self, configs):
        try:
            self.connection = psycopg2.connect(
                host=configs['host'],
                port=configs['port'],
                database=configs['database'],
                user=configs['user'],
                password=configs['password']
            )
            print("Database connection created...")
            self.schema = configs['schema_name']
            info(f'[SCHEMA] - Processing records from: {self.schema}')
        except psycopg2.Error as e:
            print(f"Error creating database connection: {e}")

    def find_all_address(self):
        sql = f"""
            SELECT ca.id, ca.address, ca.number, ca.neighborhood, ca.postal_code, ca.city, ca.state, ca.country
            FROM {self.schema}.candidate_address ca 
            WHERE ca.coordinates IS NULL 
            AND (
		        ca.address IS NOT NULL 
		        OR ca."number" IS NOT NULL 
		        OR ca.neighborhood IS NOT NULL 
		        OR ca.postal_code  IS NOT NULL 
		        OR ca.city IS NOT NULL 
		        OR ca.state IS NOT NULL
		        OR ca.country IS NOT NULL
            )
            LIMIT 10000
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def update_coordinates(self, address_id, coordinates):
        sql = f"""
            UPDATE {self.schema}.candidate_address
            SET coordinates = ST_SetSRID(ST_MakePoint(%s, %s), 4326)
            WHERE id = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (
                coordinates['longitude'],
                coordinates['latitude'],
                address_id
            ))
        self.connection.commit()
