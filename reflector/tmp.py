import sys
import os
from urllib.parse import urlparse


directories = set()
files = set()
keys = set()
kvs = set()
extensions = set()
tmp_urls = set()
urls = []

OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def url_analyse(url):
    global directories
    global files
    global keys
    global extensions
    global tmp_urls
    global kvs

    p = urlparse(url)
    scheme = p.scheme
    netloc = p.netloc
    path = p.path
    query = p.query

    dirs = path.split("/")
    length = len(dirs)
    if length > 0:
        for idx, directory in enumerate(dirs):
            if idx+1 == length and "." in directory and not directory.endswith("."):
                ext = directory.split(".")[-1]
                if len(ext) < 7:
                    files.add(directory)
                    extensions.add(directory.split(".")[-1])
            elif directory != "":
                directories.add((idx, directory))

    key_c = []
    if query != "" or "&" in query:
        queries = query.strip("&").split("&")
        queries.sort()
        for q in queries:
            kvs.add(q)
            try:
                key, _ = q.split("=", maxsplit=1)
                keys.add(key)
                key_c.append(key)
            except:
                pass

    tmp_key = "@&@".join(key_c)
    tmp_url = scheme + netloc + path + tmp_key
    if tmp_url not in tmp_urls:
        urls.append(url)
    tmp_urls.add(tmp_url)


def write_lines(filename, data):
    with open(filename, "w") as f:
        f.writelines("\n".join(data))


def print_color(color, message):
    print(f"{color}{message}{ENDC}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_color(FAIL, "[x] whturlparse urls.txt")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print_color(FAIL, "[x] No file found ")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        print_color(OKCYAN, "[!] URL Parsing ... ")
        for line in lines:
            line = line.strip()
            url_analyse(line)

    directory_levels = {}
    print_color(OKGREEN, "[!] Analysing directories ... ")
    for directory in directories:
        directory_levels.setdefault(directory[0], []).append(directory[1])

    if not os.path.exists("url_analyse/dirs"):
        os.makedirs("url_analyse/dirs")

    print_color(OKGREEN, "[!] Saving into text files ... ")
    write_lines("url_analyse/urls.txt", urls)
    write_lines("url_analyse/keys.txt", keys)
    write_lines("url_analyse/kvs.txt", kvs)
    write_lines("url_analyse/extensions.txt", extensions)
    write_lines("url_analyse/files.txt", files)

    for lvl, directory in directory_levels.items():
        write_lines(f"url_analyse/dirs/level_{lvl}.txt", directory)
