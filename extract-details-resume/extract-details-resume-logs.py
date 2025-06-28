import os
import re
import argparse
from collections import defaultdict
from database import CandidateRepository
from mappers import map_to_settings

MAX_ITEMS = 5

def split_value_from_row(line, separator):
    return line.split(separator)[-1].strip()

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def write_content_resume(grouped_contents, output_dir):
    final_structure = defaultdict(lambda: defaultdict(list))

    for (schema, search_type, filter_text), contents in grouped_contents.items():
        final_structure[(schema, filter_text)][search_type].extend(contents)

    for (schema, filter_text), search_groups in final_structure.items():
        filename = f"{schema} - {filter_text}.txt".replace("/", "_").replace("\\", "_")
        filepath = os.path.join(output_dir, filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"#term = {filter_text}\n\n")
            for search_type, content_list in search_groups.items():
                file.write(f"# {search_type}\n\n")
                for idx, content in enumerate(content_list, start=1):
                    file.write(f"{idx}) {content}\n\n")

def read_resume_content(records, settings):
    base_configs = settings.get('database')
    output_dir = settings.get('directories').get('output')

    grouped_contents = defaultdict(list)

    for (schema, search_type, filter_text), candidates in records.items():
        configs = base_configs.copy()
        configs['schema_name'] = schema
        repository = CandidateRepository(configs)

        for candidate_id in candidates:
            content = repository.get_resume_content(candidate_id)
            if content:
                grouped_contents[(schema, search_type, filter_text)].append(content)

    write_content_resume(grouped_contents, output_dir)

def parse_log_file(log_file, settings):
    records = {}
    lines = read_file(log_file)

    schema = None
    key = None
    candidates = []

    for line in lines:
        if "[SCHEMA] - Processing records from:" in line:
            schema = split_value_from_row(line, '[SCHEMA] - Processing records from:')

        elif "- Filter:" in line:
            if key and candidates:
                records[key] = candidates.copy()
                candidates.clear()

            match = re.search(r"Filter:\s*(.*?),\s*Type:\s*(\w+),\s*Time Spent:\s*([\d.]+)", line)
            if match:
                filter_text = match.group(1).strip()
                search_type = match.group(2).strip()
                key = (schema, search_type, filter_text)

        elif "Candidate:" in line:
            match = re.search(r"Candidate:\s*([a-f0-9-]{36})", line, re.IGNORECASE)
            if match:
                candidate_id = match.group(1)
                if key and len(candidates) < MAX_ITEMS:
                    candidates.append(candidate_id)

    if key and candidates:
        records[key] = candidates.copy()

    read_resume_content(records, settings)

def read_file_logs(settings):
    directories = settings.get('directories')
    input_dir = directories.get('input')

    for filename in os.listdir(input_dir):
        if filename.endswith(".log"):
            absolute_path = os.path.join(input_dir, filename)
            parse_log_file(absolute_path, settings)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument(
        "-l","--directory_logs",
        type=str,
        required=True,
        help="Directory where the processing log files are located"
    )
    parser.add_argument(
        "-o","--directory_output",
        type=str,
        required=True,
        help="Directory where the text files resulting from the process will be saved"
    )

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

    args = parser.parse_args()
    settings = map_to_settings(args)
    read_file_logs(settings)
