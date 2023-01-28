import os
import json
from urllib.parse import urlparse
from .util import bcolors, print_color, url_to_filename


def save_lines(directory, filename, data):
    path_to_save = os.path.join(directory, filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(path_to_save):
        with open(path_to_save, "r") as f:
            lines = f.readlines()
            for qkey in [f"{q}\n" for q in data]:
                if qkey not in lines:
                    lines.append(qkey)
        with open(path_to_save, "w") as f:
            f.writelines(lines)
    else:
        with open(path_to_save, "w") as f:
            f.writelines([f"{q}\n" for q in data])
    print_color(bcolors.OKBLUE,
                f"[!] Data saved at <{path_to_save}> successfully!")


def save_json(directory, filename, data):
    path_to_save = os.path.join(directory, filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path_to_save, "w") as f:
        f.write(json.dumps(data))
    print_color(bcolors.OKBLUE,
                f"[!] Data saved at <{path_to_save}> successfully!")


def save_files(directory, data_arr, ext):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for data in data_arr:
        filename = url_to_filename(data["url"], data["method"], ext)
        filepath = os.path.join(directory, filename)
        with open(filepath, "w") as f:
            f.write(data["text"])
        print_color(bcolors.OKGREEN, f"[!] File saved at <{filepath}>!")
