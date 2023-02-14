#!/usr/bin/env python
import json
import os
from pathlib import Path


def load_files(directory):
    """
    Load files in a subdirectory
    :param directory: subdirectory
    :return: list of files found in a subdirectory and its subdirectories
    """
    files_list = []  # list of files found in the subdirectory and its subdirectories
    for path, directories, files in os.walk(directory):  # walk through the subdirectory
        for file in files:  # each file in the subdirectory and its subdirectories
            files_list.append(os.path.join(path, file))  # is added in the list
    return files_list


def replace_extension(file, new_extension):
    """
    Replace file extension with a new one
    :param file: file path
    :param new_extension: new file extension
    :return: None
    """
    return Path(file).with_suffix(new_extension)


def create_file(path):
    """
    Create file from path
    :param path: file path
    :return: None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)  # create directories if they don't already exist
    with open(path, 'w+') as file:  # create the file
        file.close()  # and close it


def write_file(path, content):
    """
    Write file
    :param path: file path
    :param content: file content
    :return: None
    """
    with open(path, 'w+') as file:  # open file
        file.write(content)  # write content
        file.close()  # and close it


def append_file(path, content):
    """
    Append content to file
    :param path: file path
    :param content: file content
    :return:
    """
    with open(path, "a") as file:  # open file
        file.write(content)  # append content
        file.close()


def write_json_file(path, content):
    """
    Write JSON file
    :param path: file path
    :param content: file content
    :return: None
    """
    with open(path, 'w+') as file:  # open file
        json.dump(content, file, indent=4)  # write content and indent JSON file
        file.close()
