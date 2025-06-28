import psycopg2

class CandidateRepository:
    def __init__(self, configs):
        try:
            self.connection = psycopg2.connect(
                host=configs['host'],
                port=configs['port'],
                database=configs['database'],
                user=configs['user'],
                password=configs['password']
            )
            self.schema = configs['schema_name']
        except psycopg2.Error as e:
            print(f"Error creating database connection: {e}")

    def get_resume_content(self, candidate_id):
        sql = f"""
            SELECT ccr.content_resume 
            FROM {self.schema}.candidate_content_resume ccr 
            WHERE ccr.candidate = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            result = cursor.fetchone()
            return result[0] if result else None
