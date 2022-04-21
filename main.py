import collections
import os
import json
import re
import argparse


def find_missing(counter: collections.Counter, config_file_extensions):
    all_extensions_pass = True
    log = ""
    for extension in config_file_extensions:
        if counter[extension['name']] < extension['amount']:
            log += "Got " + str(
                counter[extension['name']]) + " " + extension['name']
            log += " files instead of " + str(extension['amount']) + "\n"
            all_extensions_pass = False
    if all_extensions_pass:
        print("Submission is okay")
    else:
        print("Submission might have some files missing: ")
        print(log)


def check_student_directory(stu_directory: str, file_extensions: list):
    stu_file_extensions = []
    stu_files = []
    print("--\ndirectory = " + stu_directory)
    for root, subdirs, files in os.walk(stu_directory):
        if len(subdirs) == 0:
            if len(files) > 0:
                stu_files += files
                stu_file_extensions += [
                    os.path.splitext(file)[1] for file in files
                ]
    print('files: \n' + '\n'.join(map(str, stu_files)) + '\n')
    occurrences = collections.Counter(stu_file_extensions)
    find_missing(occurrences, file_extensions)


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
    parser.add_argument(
        "config_file",
        help=
        "Path of the config file. Please refer to config_template.txt for configuration help."
    )
    args = parser.parse_args()

    with open(args.config_file, mode="r", encoding="utf-8") as f:
        config = json.load(f)
        print(config['base_directory'])

    config['base_directory'] = os.path.abspath(config['base_directory'])
    print('base directory (absolute) = ' +
          os.path.abspath(config['base_directory']))

    student_directories = find_student_directories(
        config['base_directory'], config['submission_name_regex'])
    for student_directory in student_directories:
        check_student_directory(student_directory, config['file_extensions'])
