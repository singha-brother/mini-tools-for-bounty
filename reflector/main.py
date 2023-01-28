from lib import Searcher, get_args, get_unique_urls, bc, print_color
import os
import json


def main():
    args = get_args()
    filepath = args.file
    timeout = args.timeout
    threads = args.threads
    if args.proxy:
        proxy = {"http": args.proxy, "https": args.proxy}
    else:
        proxy = {}

    print()
    print_color("--- Finding Unique URLs with query parameter ---",
                bc.HEADER + bc.BOLD)

    urls = get_unique_urls(filepath)
    if len(urls) == 0:
        print_color("[x] No url found!", bc.FAIL, bc.BOLD)
        exit()
    print_color(f"[!] Found {len(urls)} urls!", bc.OKCYAN + bc.BOLD)

    print()
    print_color("----- Start Searching -----", bc.HEADER + bc.BOLD)

    searcher = Searcher(timeout=timeout,
                        proxies=proxy)
    searcher.start(threads, urls)

    if len(searcher.found) > 1:
        os.makedirs("./reflect", exist_ok=True)
        with open(f"./reflect/{args.out}", "w") as f:
            json_obj = json.dumps(searcher.found, indent=4)
            f.write(json_obj)


if __name__ == '__main__':
    main()
