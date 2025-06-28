import os
import re
import csv
import argparse

def split_value_from_row(line, separator):
    return line.split(separator)[-1].strip()

def create_csv_report_file(file_name, records):
    file_exists = os.path.exists(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not file_exists:
            writer.writerow(["schema", "filter_text", "search_type", "time_spent"])
        writer.writerows(records)

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def parse_log_file(log_file, output_csv):
    records = []
    lines = read_file(log_file)
    schema = None
    for line in lines:
        if "[SCHEMA] - Processing records from:" in line:
           schema =  split_value_from_row(line, '[SCHEMA] - Processing records from:')
        if "- Filter:" in line:
            match = re.search(r"Filter:\s*(.*?),\s*Type:\s*(\w+),\s*Time Spent:\s*([\d.]+)", line)
            if match:
                filter_text = match.group(1).strip()
                search_type = match.group(2).strip()
                time_spent = float(match.group(3))
                records.append([schema, filter_text, search_type, time_spent])
    create_csv_report_file(output_csv, records)

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