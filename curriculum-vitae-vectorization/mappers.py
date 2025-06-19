from resume_vector_poc.dateutils import datetime_to_str


def map_to_candidate(row):
    return {
        'id' : row[0],
        'name': row[1],
        'email': row[2],
        'about_you': row[3],
        'professional_goal': row[4],
        'professional_summary':row[5],
    }

def map_to_address(row):
    return {
        'address': row[0],
        'neighborhood': row[1],
        'city': row[2],
        'state': row[3],
        'country': row[4]
    }

def map_to_professional_experience(row):
    return {
        'company_name': row[0],
        'start_date': datetime_to_str(row[1]),
        'end_date': datetime_to_str(row[2]),
        'job_position_name': row[3],
        'description': row[4]
    }

def map_to_education(row):
    return {
        'institution_name': row[0],
        'course_name': row[1],
        'conclusion_year': row[2],
        'start_date': datetime_to_str(row[3]),
        'end_date': datetime_to_str(row[4]),
        'type_situation': row[5]
    }

def map_to_language(row):
    mapping = {
        'BASIC': 'Básico',
        'INTERMEDIATE': 'Intermediário',
        'ADVANCED': 'Avançado',
        'FLUENT': 'Fluente',
        'NATIVE': 'Nativo'
    }
    return {
       'language': row[0],
       'type_language': row[1],
       'type_proficiency': mapping.get(row[2]),
    }
def map_to_abilities(row):
    return {
       'description': row[0]
    }
def map_to_achievement(row):
    mapping = {
       'CERTIFICATE': 'Certificado',
       'COURSE': 'Curso',
       'AWARD': 'Premiação'
    }
    return {
       'title': row[0],
       'achievements_type': mapping.get(row[1]),
       'description': row[2],
       'start_date': datetime_to_str(row[3]),
       'end_date': datetime_to_str(row[4])
    }

def map_to_position_sought(row):
    return {
       'intended_area': row[0],
       'intended_job': row[1]
    }

def map_to_phone_contact(row):
   return row[0]

def map_to_settings(args):
    database_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password,
        'schema_name': args.schema_name
    }

    aws_config = {
        'key': args.aws_key,
        'secret': args.aws_secret,
        'region': args.aws_region
    }

    return {
        'database': database_config,
        'aws': aws_config
    }
