import json
import os


def load_json_file(path_relative_to_root):
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    file_path = os.path.join(root_path, path_relative_to_root + '.json')

    if not os.path.isfile(file_path):
        return {}

    with open(file_path) as data_file:
        return json.load(data_file)
