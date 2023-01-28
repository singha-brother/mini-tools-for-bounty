import xmltodict
import pandas as pd
import os
import sys
import base64
from urllib.parse import urlparse
from .util import compare_array


def read_burpxml(filepath):
    if not os.path.exists(filepath):
        print(f"[x] File \"{filepath}\" not found")
        sys.exit(1)
    with open(filepath, "r") as f:
        xmlfile = f.read()

    result = xmltodict.parse(xmlfile)
    items = result["items"]["item"]
    df = pd.json_normalize(items)
    return df


class AnalyseBurp:

    def __init__(self, filepath) -> None:
        self.df = read_burpxml(filepath)
        self.extensions = self.df["extension"].unique()

    def get_urls(self):
        all_urls = {}
        urls_with_query = {}
        exclude_extensions = ["css", "png", "jpg", "jpeg", "svg"]
        exclude_status_codes = ["304", "404"]

        for method in self.df["method"].unique():
            all_urls[method] = self.df[(self.df["method"] == method) & (~self.df["status"].isin(exclude_status_codes)) & (
                ~self.df["extension"].isin(exclude_extensions))]["url"].sort_values().unique()
            all_urls[method] = all_urls[method].tolist()

        query_seen = {}
        for method, urls in all_urls.items():
            urls_with_query[method] = []
            query_seen = []

            for url in urls:
                parse_url = urlparse(url)
                queries = parse_url.query.strip("&").split("&")
                u = parse_url.scheme + "://" + parse_url.netloc + parse_url.path
                query_arr = [q.split("=")[0] for q in queries] + [u]
                query_arr.sort()

                have_seen = sum([compare_array(query_arr, seen_arr)
                                for seen_arr in query_seen])
                if have_seen == 0 and len(parse_url.query) != 0:
                    urls_with_query[method].append(url)
                    query_seen.append(query_arr)

        return all_urls, urls_with_query

    def extension_check(self, word):
        if "." in word:
            arr = word.split(".")
            if arr[-1] in self.extensions:
                return arr[-1]
        return False

    def analyse_urls(self):
        all_directories = []
        all_queries = []
        all_files = []
        qkeys = []
        for url in self.df["url"].unique():
            urlparts = urlparse(url)
            directories = urlparts.path.strip('/').split('/')
            queries = urlparts.query.strip('&').split('&')
            for directory in directories:
                if self.extension_check(directory):
                    if directory not in all_files:
                        all_files.append(directory)
                else:
                    if directory not in all_directories and len(directory) != 0:
                        all_directories.append(directory)

            # for query in queries:
            #     if query not in all_queries and len(query) != 0:
            #         all_queries.append(query)
            if urlparts.query not in all_queries and len(urlparts.query) != 0:
                all_queries.append(urlparts.query)

            for query in all_queries:
                qlist = query.split("=")
                qkey = qlist[0]
                if qkey not in qkeys:
                    qkeys.append(qkey)

        all_files.sort()
        all_directories.sort()
        all_queries.sort()
        qkeys.sort()
        return all_files, all_directories, all_queries, qkeys

    def analyse_get_request_headers(self):
        req_header_lines = []
        req_headers = []
        post_headers_for_save = []

        url_shown = []

        for _, req in self.df[["url", "request.#text", "method"]].iterrows():

            req_txt = base64.b64decode(req["request.#text"]).decode()
            # print(req_txt)
            header, payload = req_txt.split("\r\n\r\n", maxsplit=1)
            if len(payload) > 3 and req.url not in url_shown:
                url_shown.append(req.url)
                to_save = {
                    "method": req["method"],
                    "url": req["url"],
                    "text": req_txt
                }
                post_headers_for_save.append(to_save)

            for line in header.split('\r\n'):
                if ":" not in line:
                    continue
                if line not in req_header_lines:
                    req_header_lines.append(line)

                hparam = line.split(":")[0]
                if hparam not in req_headers:
                    req_headers.append(hparam)

        req_header_lines.sort()
        req_headers.sort()
        return req_headers, req_header_lines, post_headers_for_save

    def analyse_get_response_headers(self):
        res_header_lines = []
        res_headers = []
        for _, res in self.df[["url", "response.#text"]].iterrows():
            res_txt = base64.b64decode(res["response.#text"]).decode()
            header, _ = res_txt.split("\r\n\r\n", maxsplit=1)

            for line in header.split("\r\n"):
                if ":" not in line:
                    continue
                if line not in res_header_lines:
                    res_header_lines.append(line)
                hparam = line.split(":")[0]
                if hparam not in res_headers:
                    res_headers.append(hparam)

        res_header_lines.sort()
        res_headers.sort()

        return res_headers, res_header_lines

    def save_files(self, extension):
        files = []
        filter_df = self.df[(self.df['extension'] == extension)
                            & (self.df['status'] == '200')]
        for _, res in filter_df[["url", "response.#text", "method"]].iterrows():
            files.append({
                "url": res["url"],
                "method": res["method"],
                "text": base64.b64decode(res["response.#text"]).decode()
            })

        return files
