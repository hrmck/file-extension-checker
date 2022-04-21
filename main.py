import collections
import os
import json
import re
import argparse
import logging
from datetime import datetime
import sys

current = datetime.now().strftime('%Y-%m-%d_%H%M%S')

log_handler = logging.FileHandler(f"logs/{current}.log")
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(
    logging.Formatter("[%(asctime)s]%(name)s:%(levelname)s - %(message)s"))

file_handler = logging.FileHandler(f"test_output/{current}.txt")
file_handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)
logger.addHandler(file_handler)

ignore_folders = ["__MACOSX"]


def find_missing(submission_extensions_counter: collections.Counter,
                 required_extensions):
    for extension in required_extensions:
        if submission_extensions_counter[
                extension['name']] != extension['amount']:
            logger.warning(
                f"Got {submission_extensions_counter[extension['name']]} {extension['name']} files "
                f"instead of {str(extension['amount'])}")


def check_student_directory(stu_directory: str, file_extensions: list):
    stu_file_extensions = []
    stu_files = []
    logger.info(f"checking directory: {stu_directory}")
    for root, _, files in os.walk(top=stu_directory):
        if any(ignore_folder in root for ignore_folder in ignore_folders):
            continue

        logger.debug(f"dir: {root}")
        stu_files.extend(files)
        stu_file_extensions.extend(
            [os.path.splitext(file)[1] for file in files])
    logger.debug(f"files: {stu_files}")
    logger.debug(f"extensions: {stu_file_extensions}")
    find_missing(
        submission_extensions_counter=collections.Counter(stu_file_extensions),
        required_extensions=file_extensions)


def find_student_directories(base_directory: str,
                             submission_name_regex: str) -> list:
    base_directories = []
    for root, _, _ in os.walk(base_directory):
        folder_name = root.split(os.path.sep)[-1]
        if re.search(submission_name_regex, folder_name):
            base_directories.append(root)
    return base_directories


def main():
    parser = argparse.ArgumentParser(
        description="Checks if each targeted subdirectory has required files.")
    parser.add_argument(
        "-c",
        "--config",
        help="""Specify the config file location (default is config.json).
        Please refer to config_template.txt for configuration help.""",
        default="config.json")
    args = parser.parse_args()

    with open(args.config, mode="r", encoding="utf-8") as f:
        config = json.load(f)

    student_directories = find_student_directories(
        base_directory=os.path.abspath(config['base_directory']),
        submission_name_regex=config['submission_name_regex'])
    logger.debug(f"detected student directories: {student_directories}")
    for student_directory in student_directories:
        check_student_directory(student_directory, config['file_extensions'])


if __name__ == '__main__':
    sys.exit(main())
