import psycopg2
import time
from logger import info, warn

class Repository:
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

    def search_using_hnsw(self, orgin_filter, vector):
        sql = f"""
            SELECT ca.id, ca."name" 
            FROM {self.schema}.candidate ca 
            JOIN {self.schema}.candidate_resume_vector_hnswm crv 
            ON crv.candidate = ca.id            
            WHERE crv.embedding <=> %s::vector < 1.0
            ORDER BY crv.embedding <=> %s::vector 
            LIMIT 100;  
        """

        start_time = time.time()
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (vector, vector))
            rows = cursor.fetchall()

        elapsed_time = time.time() - start_time
        warn(f'Filter: {orgin_filter}, Type: HNSW, Time Spent: {elapsed_time:.4f} seconds')
        return rows


    def search_using_ivfflat(self, orgin_filter, vector):
        sql = f"""
            SELECT ca.id, ca."name" 
            FROM {self.schema}.candidate ca 
            JOIN {self.schema}.candidate_resume_vector_ivfflat crv 
            ON crv.candidate = ca.id            
            WHERE crv.embedding <=> %s::vector < 1.0
            ORDER BY crv.embedding <=> %s::vector   
            LIMIT 100;
            """
        start_time = time.time()
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (vector, vector))
            rows = cursor.fetchall()

        elapsed_time = time.time() - start_time
        warn(f'Filter: {orgin_filter}, Type: IVFFlat, Time Spent: {elapsed_time:.4f} seconds')
        return rows

    def search_using_ts_vector(self, filter):
        sql = f"""
            SELECT ca.id, ca."name", 
            ts_rank_cd(crv.tokens, plainto_tsquery('portuguese', %s)) AS rank
            FROM {self.schema}.candidate ca 
            JOIN {self.schema}.candidate_resume_token crv 
            ON crv.candidate = ca.id 
            WHERE crv.tokens @@ plainto_tsquery('portuguese', %s) 
            AND ts_rank_cd(crv.tokens, plainto_tsquery('portuguese', %s)) > 0
            ORDER BY rank DESC 
            LIMIT 100;
        """
        start_time = time.time()
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (filter, filter, filter))
            rows = cursor.fetchall()

        elapsed_time = time.time() - start_time
        warn(f'Filter: {filter}, Type: ts_vector, Time Spent: {elapsed_time:.4f} seconds')
        return rows

