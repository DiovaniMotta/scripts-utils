import os
import re
import csv
import argparse

def create_csv_report_file(file_name, records):
    file_exists = os.path.exists(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not file_exists:
            writer.writerow(["candidate", "tokens"])
        writer.writerows(records)

def save_report_file(output_csv, records_dict):
    if records_dict:
        records = list(records_dict.values())
        create_csv_report_file(output_csv, records)

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def extract_number_of_tokens(line):
    match = re.search(r'\[TOKENS\]:\s*(\d+)', line)
    if match:
        return int(match.group(1))

def extract_candidate_id(line):
    match = re.search(r'candidate\s+([0-9a-fA-F-]{36})', line)
    if match:
       return match.group(1)

def parse_log_file(log_file, output_csv):
    records_dict = {}
    lines = read_file(log_file)

    candidate_id = None

    for line in lines:
        if '- Starting processing candidate' in line:
           candidate_id = extract_candidate_id(line)
        if "[TOKENS]:" in line:
           token_number = extract_number_of_tokens(line)
           if candidate_id not in records_dict:
              records_dict[candidate_id] = [
                  candidate_id,
                  token_number
              ]
    save_report_file(output_csv, records_dict)

def read_file_logs(directory, report_file):
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
           absolute_path =  os.path.join(directory, filename)
           parse_log_file(absolute_path, report_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument("-d","--directory_logs", type=str, required=True, help="Directories where the processing log files are located")
    parser.add_argument("-r","--report_file_path", type=str, required=True, help="Report file in csv format with the results obtained")

    args = parser.parse_args()

    read_file_logs(args.directory_logs, args.report_file_path)