import collections
import os
import json
import re
import argparse
import logging
from datetime import datetime

handler = logging.FileHandler(
    f"logs/{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.log")
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]%(name)s:%(levelname)s - %(message)s"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def find_missing(counter: collections.Counter, config_file_extensions):
    all_extensions_pass = True
    log = ""
    for extension in config_file_extensions:
        if counter[extension['name']] < extension['amount']:
            log += (
                f"Got {counter[extension['name']]} {extension['name']} files "
                f"instead of {str(extension['amount'])}")
            all_extensions_pass = False
    if all_extensions_pass:
        logger.info("Submission is okay")
    else:
        logger.warning("Submission might have some files missing: ")
        logger.warning(log)


def check_student_directory(stu_directory: str, file_extensions: list):
    stu_file_extensions = []
    stu_files = []
    logger.info(f"directory = {stu_directory}")
    for root, subdirs, files in os.walk(stu_directory):
        logger.debug(f"dir = {root}")
        logger.debug(f"subdirs = {subdirs}")
        if len(subdirs) == 0:
            if len(files) > 0:
                stu_files += files
                stu_file_extensions += [
                    os.path.splitext(file)[1] for file in files
                ]
    logger.info(f"files: {stu_files}")
    find_missing(counter=collections.Counter(stu_file_extensions),
                 config_file_extensions=file_extensions)


def find_student_directories(base_directory: str,
                             submission_name_regex: str) -> list:
    base_directories = []
    for root, subdirs, files in os.walk(base_directory):
        identifier = root.split(os.path.sep)[-1]
        if re.match(submission_name_regex, identifier):
            base_directories.append(root)
    return base_directories


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Checks if each subdirectory has required files.")
    parser.add_argument("-c",
                        "--config",
                        help="""Specify the config file location.
        Please refer to config_template.txt for configuration help.""",
                        default="config.json")
    args = parser.parse_args()

    with open(args.config, mode="r", encoding="utf-8") as f:
        config = json.load(f)
        logger.debug(
            f"Base directory (relative) = '{config['base_directory']}'")

    logger.debug(
        f"Base directory (absolute) = '{os.path.abspath(config['base_directory'])}'"
    )

    student_directories = find_student_directories(
        base_directory=os.path.abspath(config['base_directory']),
        submission_name_regex=config['submission_name_regex'])
    logger.debug(f"Student directories: {student_directories}")
    for student_directory in student_directories:
        check_student_directory(student_directory, config['file_extensions'])
