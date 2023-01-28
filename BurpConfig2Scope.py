from rich.console import Console
from rich.table import Table
import json
import sys
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--filename',
        help="Path to Burp Configuration JSON File",
        required=True,
        type=str
    )
    parser.add_argument(
        '-s',
        '--save',
        help="Save Files",
        required=False,
        action="store_true"
    )
    args = parser.parse_args()
    return args


def print_table(data, title):
    count = 0
    colors = ["cyan", "green", "yellow", "magenta", "white"]
    header = []
    rows = []
    for item in data:
        if count == 0:
            header = list(item.keys())
            count += 1
        rows.append(list(item.values()))

    table = Table(title=title)
    for h, color in zip(header, colors):
        table.add_column(h, style=color, no_wrap=True)

    for row in rows:
        table.add_row(str(row[0]), row[1], row[2], row[3], row[4])

    console.print(table)


def format_domains(data, isInclude=True):
    text = ""
    hosts = []
    if data:
        for item in data:
            host = item["host"]
            if isInclude:
                if host not in hosts:
                    hosts.append(host)
            else:
                host = "!" + host
                if host not in hosts:
                    hosts.append(host)
        for host in hosts:
            text += host + "\n"
    return text


if __name__ == '__main__':
    console = Console()
    args = get_parser()
    print(args)
    filename = args.filename
    with open(filename, "r") as f:
        file = json.loads(f.read())

    exclude = file["target"]["scope"]["exclude"]
    include = file["target"]["scope"]["include"]
    if exclude:
        print_table(exclude, "Exclude Domains")
    if include:
        print_table(include, "Include Domains")
    if args.save:
        domains = format_domains(include)
        domains += format_domains(exclude, isInclude=False)
        with open(".scope", "w") as f:
            f.write(domains)
