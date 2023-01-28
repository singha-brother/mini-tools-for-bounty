from urllib.parse import urlparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_color(color, text):
    print(color + text + bcolors.ENDC)


def compare_array(a, b):
    if len(a) != len(b):
        return False

    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False

    return True


def url_to_filename(url, method, extension):
    urlpath = urlparse(url)
    path = urlpath.path.replace("/", "_")
    if path.endswith("."+extension):
        return method + path

    filename = method + path + "." + extension
    return filename
