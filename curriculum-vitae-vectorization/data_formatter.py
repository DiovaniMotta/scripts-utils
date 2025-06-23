from dateutils import calculate_diff_dates_as_string
from mappers import *
import re


def format_period(period):
    if not period:
        return ''

    parts = []
    if period.get('years') and period['years'] > 0:
        parts.append(f"{period['years']} ano{'s' if period['years'] != 1 else ''}")
    if period.get('months') and period['months'] > 0:
        parts.append(f"{period['months']} {'meses' if period['months'] != 1 else 'mês'}")

    if parts:
        return f"({' e '.join(parts)})"
    return ''

def format_year(start_date, end_date):
    start_year = start_date[0:4]
    end_year = end_date[0:4] if end_date else 'Presente'
    return f'{start_year} - {end_year}'

def format_year_education(start_date, end_date):
    start_year = start_date[0:4]
    end_year = end_date[0:4]
    if not start_year:
        return ''
    if not end_date:
        return ''
    return f'({start_year} - {end_year})'

def format_candidate_info(candidate):
    if not candidate:
        return ''
    lines = [f"Nome: {candidate.get('name', '')}\n"]
    if candidate.get('email'):
        lines.append(f"E-mail: {candidate['email']}\n")
    header_parts = [
        candidate.get('about_you'),
        candidate.get('professional_goal'),
        candidate.get('professional_summary')
    ]
    header = ' '.join(part for part in header_parts if part)
    if header:
        lines.append(f"{header}\n")
    return ''.join(lines)


def format_address_info(address):
    if not address:
        return ''
    parts = [address.get(key) for key in ('city', 'state', 'country') if address.get(key)]
    return 'Endereço: '+ f"{', '.join(parts)}\n" if parts else ''


def format_professional_experience(professional_experience):
    if not professional_experience:
        return ''
    lines = []
    for row in professional_experience:
        experience = map_to_professional_experience(row)
        lines.append(f"\tEmpresa: {experience.get('company_name', '')}\n")

        start_date = experience.get('start_date')
        end_date = experience.get('end_date')
        period = {}
        if start_date and end_date:
            period = calculate_diff_dates_as_string(
                experience.get('start_date'),
                experience.get('end_date')
            )
        lines.append(f"\tPeriodo: ({format_year(experience.get('start_date'), experience.get('end_date'))})\n")
        lines.append(f"\tCargo: {experience.get('job_position_name', '')} {format_period(period)}\n")
        if experience.get('description'):
            lines.append(f"\tDescrição:{experience['description']}\n")
        lines.append(f'\n')
    return '- Experiências profissionais:\n'+ ''.join(lines) if lines else ''

def format_education(educations):
    if not educations:
        return ''

    lines = []
    for row in educations:
        education = map_to_education(row)
        parts = []

        institution_name = education.get('institution_name')
        if institution_name:
            parts.append(f"\tInstituição de ensino: {institution_name}")

        course_name = education.get('course_name')
        if course_name:
            parts.append(f"\tCurso: {course_name} {format_year_education(education.get('start_date'), education.get('end_date'))}")

        if parts:
            lines.extend([part + '\n' for part in parts])
        lines.append(f'\n')

    return "- Formação acadêmica:\n" + ''.join(lines) if lines else ''

def format_language_info(languages):
    if not languages:
        return ''

    lines = []
    for row in languages:
        language = map_to_language(row)
        name = language.get('language')
        proficiency = language.get('type_proficiency')

        if not name:
            continue

        line = f"\t- {name}"
        if proficiency:
            line += f" ({proficiency})"
        lines.append(line + '\n')

    return "- Idiomas:\n" + ''.join(lines) if lines else ''

def format_abilities_info(abilities):
    if not abilities:
        return ''

    lines = []
    for row in abilities:
        ability = map_to_abilities(row)
        description = ability.get('description')
        if description:
            lines.append(f"\t- {description}\n")

    return "- Competências:\n" + ''.join(lines) if lines else ''


def format_achievements_info(achievements):
    if not achievements:
        return ''

    lines = []
    for row in achievements:
        achievement = map_to_achievement(row)
        achievement_type = achievement.get('achievements_type')
        title = achievement.get(f'\ttitle')
        period = format_year_education(
            achievement.get('start_date'),
            achievement.get('end_date')
        )
        description = achievement.get('description')
        parts = []
        if achievement_type or title or period:
            parts.append(f"\t{achievement_type or ''}: {title or ''} {period}".strip())

        if description:
            parts.append(description)

        if parts:
            lines.extend([part + '\n' for part in parts])

    return "- Cursos e certificados:\n" + ''.join(lines) if lines else ''


def format_position_sought_info(position_sought):
    if not position_sought:
        return ''

    lines = []
    for row in position_sought:
        position = map_to_position_sought(row)

        intended_area = position.get('intended_area')
        intended_job = position.get('intended_job')

        if intended_area:
            lines.append(f"\tÁrea: {intended_area}\n")
        if intended_job:
            lines.append(f"\tCargo: {intended_job}\n")

    return "- Cargos e Áreas desejadas:\n" + ''.join(lines) if lines else ''


def format_phone_contact_info(contacts):
    if not contacts:
        return ''
    lines = []
    for row in contacts:
        phone = map_to_phone_contact(row)
        if phone:
            lines.append(f' \t- {phone}\n')
    return '- Contatos telefônicos:\n'+ ''.join(lines) if lines else ''

def sanitize_content(raw):
    content = re.sub(r"[\[\],]", "", ''.join(raw))
    content = content.replace('\n', ' ')
    content = content.replace('\t', ' ')
    content = content.strip()
    return content