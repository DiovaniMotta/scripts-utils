import argparse
from database_functions import *
from logger import info
from resume_vector_poc.data_formatter import *
from resume_vector_poc.mappers import *
from resume_vector_poc.vectors import BedrockClient


def process(config):
    db_config = config.get('database')
    aws_config = config.get('aws')
    client = BedrockClient(aws_config)
    repository = Repository(db_config)
    candidate_records = repository.get_candidates()
    for row in candidate_records:
        resume_content = []
        candidate = map_to_candidate(row)
        candidate_id = candidate.get('id')
        info(f'Starting processing candidate {candidate_id}...')
        candidate_info = format_candidate_info(candidate)
        resume_content.append(candidate_info)
        info(f'Reading address from candidate')
        address_row = repository.get_candidate_address(candidate_id)
        if address_row:
            address = map_to_address(address_row)
            address_info = format_address_info(address)
            if address_info:
                resume_content.append(address_info)
        info(f'Reading professional experience from candidate')
        professional_experiences = repository.get_candidate_professional_experience(candidate_id)
        professional_experience_info = format_professional_experience(professional_experiences)
        if professional_experience_info:
            resume_content.append(professional_experience_info)
        info(f'Reading education from candidate')
        educations = repository.get_candidate_education(candidate_id)
        educations_info = format_education(educations)
        if educations_info:
            resume_content.append(educations_info)
        info(f'Reading languages from candidate')
        languages = repository.get_candidate_language(candidate_id)
        languages_info = format_language_info(languages)
        if languages_info:
            resume_content.append(languages_info)
        info(f'Reading abilities from candidate')
        abilities = repository.get_candidate_ability(candidate_id)
        abilities_info = format_abilities_info(abilities)
        if not abilities_info:
            info(f'Reading knowledge from candidate')
            abilities = repository.get_candidate_knowledge(candidate_id)
            abilities_info = format_abilities_info(abilities)
            if abilities_info:
                resume_content.append(abilities_info)
        else:
            resume_content.append(abilities_info)
        info(f'Reading achievements from candidate')
        achievements = repository.get_candidate_achievements(candidate_id)
        achievements_info = format_achievements_info(achievements)
        if achievements_info:
            resume_content.append(achievements_info)
        info(f'Reading position sought from candidate')
        position_sought = repository.get_candidate_position_sought(candidate_id)
        position_sought_info = format_position_sought_info(position_sought)
        if position_sought_info:
            resume_content.append(position_sought_info)
        info(f'Reading phone contact from candidate')
        phone_contact = repository.get_candidate_phone_contact(candidate_id)
        phone_contact_info = format_phone_contact_info(phone_contact)
        if phone_contact_info:
            resume_content.append(phone_contact_info)
        info(f'Resume done for send vectorization:\n{''.join(resume_content)}')
        info('Generate embedding for resume...')
        embedding = client.generate_embedding(resume_content)
        resume = {
            'candidateId': candidate_id,
            'content': str(resume_content),
            'embedding': embedding
        }
        print(resume)
        #repository.insert_candidate_vector(resume)
        info(f'Finished process for candidate {candidate_id}...\n')
    repository.close()
    info('Process finished...')

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
        "-k", "--aws_key",
        type=str,
        required=False,
        help="AWS access key ID"
    )
    parser.add_argument(
        "-a", "--aws_secret",
        type=str,
        required=False,
        help="AWS secret access key"
    )
    parser.add_argument(
        "-r", "--aws_region",
        type=str,
        default="sa-east-1",
        help="AWS region name (default: sa-east-1)"
    )

    args = parser.parse_args()
    settings = map_to_settings(args)

    process(settings)
