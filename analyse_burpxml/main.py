#!/usr/bin/env python3
import os
import sys
import json
from lib import (
    AnalyseBurp,
    save_lines,
    save_json,
    save_files,
    args,
    bcolors,
    print_color)


DATA_DIR = os.path.join(args.output_folder, "analyse_burp", "data")
FILE_DIR = os.path.join(args.output_folder, "analyse_burp", "post_headers")
URL_DIR = os.path.join(args.output_folder, "analyse_burp", "urls")

if __name__ == '__main__':
    burp = AnalyseBurp(args.input_file)
    all_urls, urls_with_query = burp.get_urls()

    if args.normal_flow:
        all_files, all_directories, all_queries, qkeys = burp.analyse_urls()
        req_headers, req_header_lines, post_headers_for_save = burp.analyse_get_request_headers()
        res_headers, res_header_lines = burp.analyse_get_response_headers()

        save_lines(DATA_DIR, "file_ext.txt", all_files)
        save_lines(DATA_DIR, "dirs.txt", all_directories)
        save_lines(DATA_DIR, "querieskv.txt", all_queries)
        save_lines(DATA_DIR, "querykeys.txt", qkeys)
        save_lines(DATA_DIR, "req_header_params.txt", req_headers)
        save_lines(DATA_DIR, "res_header_params.txt", res_headers)
        save_lines(DATA_DIR, "req_headers.txt", req_header_lines)
        save_lines(DATA_DIR, "res_headers.txt", res_header_lines)
        save_files(FILE_DIR, post_headers_for_save, "txt")
        save_json(URL_DIR, "all_urls.json", all_urls)
        save_json(URL_DIR, "urls_with_query.json", urls_with_query)
        for method, urls in all_urls.items():
            save_lines(URL_DIR, method + "_urls.txt", urls)
        for method, urls in urls_with_query.items():
            save_lines(URL_DIR, method + "_urls_with_query.txt", urls)

    print_color(bcolors.HEADER, "Total Urls from file")
    for method, urls in all_urls.items():
        print_color(bcolors.OKCYAN, f"[!] {method} -> {len(urls)}")

    print_color(bcolors.HEADER, "Total Urls with queries")
    for method, urls in urls_with_query.items():
        print_color(bcolors.OKCYAN, f"[!] {method} -> {len(urls)}")

    if args.saved_exts:
        print("\nAvailable extensions in this website:")
        for i, ext in enumerate(burp.extensions):
            print(f'[{i}] {ext}')

        input_exts = input("Enter extension to save [comma separated]: ")
        exts = [ext.strip() for ext in input_exts.split(',')]
        for ext in exts:
            if ext not in burp.extensions:
                print_color(
                    bcolors.FAIL, f"[x] File extension '{ext}' not exists!")
                sys.exit()
            files = burp.save_files(ext)
            EXT_DIR = os.path.join(args.output_folder, "analyse_burp", ext)
            save_files(EXT_DIR, files, ext)
