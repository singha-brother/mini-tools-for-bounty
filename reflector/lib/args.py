import argparse
from .misc import is_valid_file


def get_args():
    parser = argparse.ArgumentParser(
        description="Simple Tool that can extract unique urls with parameters from text file and find reflection.")
    parser.add_argument(
        "-f",
        "--file",
        help="text file that contains urls",
        type=lambda x: is_valid_file(parser, x),
        required=True
    )
    parser.add_argument(
        "-t",
        "--threads",
        help="Number of threads",
        required=False,
        type=int,
        default=10
    )
    parser.add_argument(
        "-p",
        "--proxy",
        help="Proxy host: eg - http://127.0.0.1:8080",
        required=False
    )
    parser.add_argument(
        "-T",
        "--timeout",
        help="Connection timeout for each request",
        required=False,
        default=10,
        type=int
    )
    parser.add_argument(
        "-o",
        "--out",
        help="Filename of the output json",
        required=False,
        default="out.json",
        type=str
    )
    return parser.parse_args()
