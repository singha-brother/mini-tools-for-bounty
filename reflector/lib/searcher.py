from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import random
import re
from .misc import bc, print_color


requests.packages.urllib3.disable_warnings()

base_dir = Path(__file__).resolve().parent


class Searcher:
    def __init__(
        self,
        search_pattern=r'\d+qwerasdf',
        timeout=10,
        proxies={},
        headers={},
        urls=[],
    ):
        self.search_pattern = search_pattern
        self.timeout = timeout
        self.proxies = proxies
        self.headers = headers
        self.user_agents = (
            Path(f"{base_dir}/resources/user_agents.txt").read_text().splitlines()
        )
        self._lock = threading.Lock()
        self.found = {}

    def start(self, threads, urls):
        started_threads = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for url_dict in urls:
                started_threads.append(
                    executor.submit(self.send_temper, url_dict))

    def send_temper(self, url_dict):
        user_agent = random.choice(self.user_agents)
        self.headers["User-Agent"] = user_agent
        try:
            r = requests.get(
                url_dict["tempered_url"],
                headers=self.headers,
                verify=False,
                proxies=self.proxies,
                timeout=self.timeout
            )
            text = r.text
            status_code = r.status_code
            r_headers = dict(r.headers)
            self._lock.acquire()
            self.find_reflection(url_dict, text, status_code, r_headers)
            self._lock.release()

        except KeyboardInterrupt:
            exit()
        except:
            pass

    def find_reflection(self, url_dict, text, status_code, header):
        items = re.findall(self.search_pattern, text)
        keys = {x: items.count(x) for x in items}
        if len(items) > 0:
            self.found[url_dict["original_url"]] = {
                "tempered_url": url_dict["tempered_url"],
                "reflect_values": list(set(items)),
                "response_header": header,
                "status_code": status_code,
                "response_body": text
            }
            print_color(
                f'[!] {url_dict["tempered_url"]} [{status_code}]', bc.OKGREEN + bc.BOLD)
            for k, v in keys.items():
                print_color(f'>> {k} for {v} times!', bc.BOLD + bc.FAIL)
