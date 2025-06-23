import psycopg2

schema = {
   'name': 'public'
}

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
        except psycopg2.Error as e:
            print(f"Error creating database connection: {e}")

    def insert_candidate_vector(self, record):
        cursor = self.connection.cursor()
        insert_command = f"""
            INSERT INTO {self.schema}.candidate_resume_vector (candidate, content_resume, embedding) VALUES(%s, %s, %s);
        """
        content = str(record.get("content")).replace('\n', ' ')
        values = (record.get("candidateId"), content, record.get("embedding"))
        cursor.execute(insert_command, values)
        self.connection.commit()

    def get_candidates(self):
        sql = f"""
            SELECT id, name, email, about_you, professional_goal, professional_summary  
            FROM {self.schema}.candidate
            ORDER BY id  
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows

    def get_candidate_address(self, candidate_id):
        sql = f"""
            SELECT address, neighborhood, city, state, country
            FROM {self.schema}.candidate_address ca 
            INNER JOIN {self.schema}.candidate_address_candidates cac 
            ON ca.id = cac.candidate_address_id
            INNER JOIN {self.schema}.candidate c 
            ON c.id = cac.candidates_id
            WHERE c.id= %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            if rows:
                return rows[0]
        return None

    def get_candidate_professional_experience(self, candidate_id):
        sql = f"""
              SELECT
              cpe.company_name,
              cpe.start_date,
              cpe.end_date,
              cpe.job_position_name,
              cpe.description 
              FROM {self.schema}.candidate_professional_experience cpe
              WHERE cpe.candidate = %s
              ORDER BY cpe.start_date DESC
           """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_education(self, candidate_id):
        sql = f"""
              SELECT
              ce.institution_name ,
              ce.course_name,
              ce.conclusion_year,
              ce.start_date,
              ce.end_date,
              ce.type_situation
              FROM {self.schema}.candidate_education ce
              WHERE ce.candidate = %s
              ORDER BY ce.conclusion_year DESC, ce.start_date DESC, ce.end_date  
           """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_language(self, candidate_id):
        sql = f"""
              SELECT 
              cl.language,
              cl.type_language, 
              cl.type_proficiency
              FROM {self.schema}.candidate_language cl 
              WHERE cl.candidate = %s
              ORDER BY cl.created_date DESC   
              """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_knowledge(self, candidate_id):
        sql = f"""
              SELECT 
              ck.description
              FROM {self.schema}.candidate_knowledge ck 
              WHERE ck.candidate = %s
              ORDER BY ck.created_date DESC   
              """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_ability(self, candidate_id):
        sql = f"""
              SELECT 
              ca.description
              FROM {self.schema}.candidate_ability ca 
              WHERE ca.candidate = %s
              ORDER BY ca.created_date DESC    
              """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_achievements(self, candidate_id):
        sql = f"""
              SELECT 
              ca.title,
              ca.achievements_type,
              ca.description,
              ca.start_date,
              ca.end_date
              FROM {self.schema}.candidate_achievements ca
              WHERE ca.candidate = %s
              ORDER BY ca.start_date DESC  
              """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_position_sought(self, candidate_id):
        sql = f"""
              SELECT 
              cps.intended_area,
              cps.intended_job
              FROM {self.schema}.candidate_position_sought cps
              WHERE cps.candidate = %s
              ORDER BY cps.created_date DESC  
              """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def get_candidate_phone_contact(self, candidate_id):
        sql = f"""
              SELECT 
              CASE 
                WHEN coalesce(cpc.country_code, 0) > 0 
                THEN '+' || coalesce(cpc.country_code::text, '0') || ' (' || cpc.local_code::text || ') ' || cpc."number"::text
                ELSE '(' || cpc.local_code::text || ') ' || cpc."number"::text
              END AS phone
              FROM {self.schema}.candidate_phone_contact cpc 
              WHERE cpc.candidate = %s
              ORDER BY cpc.created_date; 
              """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (candidate_id,))
            rows = cursor.fetchall()
            return rows

    def close(self):
        self.connection.close()