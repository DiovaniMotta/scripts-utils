import re
import csv
import os
import argparse

def create_csv_report_file(file_name, records):
    file_exists = os.path.exists(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not file_exists:
            writer.writerow(["execution_date", "bucket_name", "file", "object", "original_size_mb", "compressed_size_mb","perc_compression"])
        writer.writerows(records)

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()

def split_value_from_row(line, separator):
    return line.split(separator)[-1].strip()

def extract_size_file_from_row(line):
    matcher_value = re.search(r"size:?\s([\d\.]+) MB", line)
    return float(matcher_value.group(1)) if matcher_value else None

def parse_log_file(log_file, output_csv):
    records_dict = {}
    lines = read_file(log_file)

    object_id = None
    bucket_name = None
    csv_path = None
    original_size_mb = None

    for line in lines:
        execution_date = extract_date_time_from_row(line)

        if "- Bucket Name:" in line:
            bucket_name = split_value_from_row(line, "- Bucket Name:")

        if "- CSV Path:" in line:
            csv_path = split_value_from_row(line, "- CSV Path:")

        if "Start processing object:" in line:
            object_id = split_value_from_row(line, "Start processing object:")

        if "File saved in" in line:
            original_size_mb = extract_size_file_from_row(line)

        if "Upload object" in line:
            compressed_size_mb = extract_size_file_from_row(line)
            perc_compression = calc_perc_compress(compressed_size_mb, original_size_mb)

            if object_id not in records_dict:
                records_dict[object_id] = [
                    execution_date,
                    bucket_name,
                    csv_path,
                    object_id,
                    original_size_mb,
                    compressed_size_mb,
                    perc_compression
                ]
    save_report_file(output_csv, records_dict)


def save_report_file(output_csv, records_dict):
    records = list(records_dict.values())
    create_csv_report_file(output_csv, records)

def extract_date_time_from_row(line):
    match = re.match(r"(\d{4}-\d{2}-\d{2})", line)
    if match:
        return match.group(1)
    return Exception(f'Execution date {line} not found!')

def calc_perc_compress(compressed_size_mb, original_size_mb):
    if original_size_mb and compressed_size_mb:
        perc_compression = ((original_size_mb - compressed_size_mb) / original_size_mb) * 100
        return round(perc_compression, 3)
    else:
        return None

def read_file_logs(directory, report_file):
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
           absolute_path =  os.path.join(directory, filename)
           parse_log_file(absolute_path, report_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument("--directory_logs", type=str, required=True, help="Directories where the processing log files are located")
    parser.add_argument("--report_file_path", type=str, required=True, help="Report file in csv format with the results obtained")

    args = parser.parse_args()

    read_file_logs(args.directory_logs, args.report_file_path)