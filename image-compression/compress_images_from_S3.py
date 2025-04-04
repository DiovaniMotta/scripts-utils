import io
import os

import cv2
import boto3
import logging
import argparse
import tempfile
from PIL import ImageOps, Image, ImageFile
from pathlib import Path
import dask.dataframe as dd
from datetime import datetime
from botocore.exceptions import ClientError

BUCKET_NAME = ''
TEMP_PATH = ''
PERCENT_COMPRESS_QUALITY = 0

s3 = boto3.client("s3")

logging.basicConfig(
    filename=f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def bytes_to_mb(bytes_value):
    return round(bytes_value / (1024 ** 2), 3)

def read_csv(filepath):
    df = dd.read_csv(filepath, dtype={
        'path': 'string'
    })
    summary = df.compute()
    return summary.reset_index(drop=True)

def get_file_size(file_path):
    return os.stat(file_path).st_size

def extract_filename_from_path(path):
    parts = path.split("/")
    return parts[-1] if len(parts) > 1 else path

def valid_file(path):
    return cv2.imread(path)

def download_file_from_s3(path):
    logging.info(f'Downloading object {path} from AWS S3.')
    file_name = extract_filename_from_path(path)
    absolute_path = os.path.join(TEMP_PATH, file_name)
    s3.download_file(BUCKET_NAME, path, absolute_path)
    size_in_bytes = get_file_size(absolute_path)
    size_in_mbs = bytes_to_mb(size_in_bytes)
    logging.info(f'File saved in {absolute_path} with size: {size_in_mbs} MB')

def delete_temp_file(path):
    file_name = extract_filename_from_path(path)
    absolute_path = Path(os.path.join(TEMP_PATH, file_name))
    if absolute_path.exists():
        absolute_path.unlink()
        logging.info(f"File {absolute_path} was deleted.")
    else:
        raise Exception(f"File {absolute_path} not found.")


def upload_file_from_s3(path, content):
    if content is None or content.getbuffer().nbytes == 0:
        logging.warning(f"[INVALID_CONTENT] - Failed to upload {path}: No content provided (compression might have failed).")
        return
    size_in_bytes = content.getbuffer().nbytes
    size_in_mb = bytes_to_mb(size_in_bytes)
    logging.info(f'Upload object {path} for bucket {BUCKET_NAME} with size {size_in_mb} MB')
    s3.put_object(Bucket=BUCKET_NAME, Key=path, Body=content)

def compress_image(path):
    try:
        file_name = extract_filename_from_path(path)
        absolute_path = os.path.join(TEMP_PATH, file_name)

        if valid_file(absolute_path) is None:
            logging.warning(f'[CORRUPT_FILE] - Object: {path} is corrupt. It will be ignored!')
            return io.BytesIO()

        with Image.open(absolute_path) as img:
            buffer = io.BytesIO()
            match img.format:
                case "PNG":
                    logging.info(f'Compressing {absolute_path} object as PNG file')
                    img = img.convert("P" if img.mode != "P" else img.mode)
                    img.save(buffer, format="PNG", optimize=True)
                case "JPEG" | "JPG" | "MPO":
                    logging.info(f'Compressing {absolute_path} object as JPEG/JPG file')
                    fixed_image = ImageOps.exif_transpose(img)
                    fixed_image.save(buffer, format="JPEG", quality=PERCENT_COMPRESS_QUALITY, optimize=True)
                case "WEBP":
                    logging.info(f'Compressing {absolute_path} object with format WEBP to JPEG/JPG file')
                    img.save(buffer, format="WEBP", quality=PERCENT_COMPRESS_QUALITY, optimize=True)
                case _:
                    logging.warning(f'[INVALID_EXTENSION] - Format {img.format} does not support by compression process. File: {path} will be ignored!')
            buffer.seek(0)
            return buffer

    except Exception as e:
        logging.critical(f"Error compressing object: {path}: {e}")
        return None

def process(filepath):
    try:
        logging.info(f'Reading dataset from file: {filepath}')
        data_set = read_csv(filepath)
        logging.info(f'Amount of objects read from CSV file: {data_set.shape[0]}')
        for _, row in data_set.iterrows():
            path = row['path']
            logging.info(f'Start processing object: {path}')
            try:
                download_file_from_s3(path)
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    logging.warning(f'[FILE_DELETED] - Object {path} was removed from bucket. It will be ignored!')
                    continue
                else:
                    raise
            buffer_compress_file = compress_image(path)
            upload_file_from_s3(path, buffer_compress_file)
            delete_temp_file(path)
            logging.info(f'End object processing: {path}')
        logging.info("Finished processment...")
    except Exception as e:
        logging.critical(f"Error generic during compression process: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument("--max_image_pixels", type=int, default=1000000000, help="Maximum image size in pixels")
    parser.add_argument("--perc_compression_quality", type=int, default=80, help="Quality percentage that must be suspended in the image enlargement process (Range possible values: 0-100)")
    parser.add_argument("--ignore_trunc", type=bool, default=True, help="Indicates whether truncation errors (corrupt files) should be ignored.")
    parser.add_argument("--temp_dir", type=str, default=tempfile.gettempdir(), help="Temporary existing directory for downloading files to be compressed")
    parser.add_argument("--bucket_name", type=str, required=True, help="S3 bucket name")
    parser.add_argument("--csv_path", type=str, required=True, help="CSV file path")

    args = parser.parse_args()

    Image.MAX_IMAGE_PIXELS = args.max_image_pixels
    ImageFile.LOAD_TRUNCATED_IMAGES = args.ignore_trunc
    BUCKET_NAME = args.bucket_name
    TEMP_PATH = args.temp_dir
    PERCENT_COMPRESS_QUALITY = args.perc_compression_quality

    logging.info(f"Settings:\n - Max Image Pixels: {Image.MAX_IMAGE_PIXELS}\n - Ignored Truncated Image:{ImageFile.LOAD_TRUNCATED_IMAGES}\n - Compression Quality Percentage: {PERCENT_COMPRESS_QUALITY} %\n - Bucket Name: {BUCKET_NAME}\n - Temp Dir: {TEMP_PATH}\n - CSV Path: {args.csv_path}")

    process(args.csv_path)
