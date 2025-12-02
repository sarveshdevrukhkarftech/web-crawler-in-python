import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.bbc.com"


def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        # response.raise_for_status()
        print("===== Start =====")
        print("Step 1 - Fetching Data Successful!")
        return response
    # except requests.exceptions.Timeout:
    #     print("Request timed out")
    # except requests.exceptions.HTTPError as error:
    #     print(f"HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Error during request: {error}")


def parse_page(res):
    # Creating soup to extract data.
    parsed_data = BeautifulSoup(res.text, "html.parser")  # Parsing Soup Data
    print("Step 2 - Parsing Data Successful!")
    return parsed_data


"""
def parse_next_urls(parsed_data):
    next_urls = []
    all_link_tags = parsed_data.find_all("a")
    for tag in all_link_tags:
        link = tag.get("href")
        if link is None:
            continue
        print(link)

        # Checking URL is valid or not.
        avoid_list = ["#", "mailto:"]
        for item in avoid_list:
            if link and link.find(item) != -1:
                print("Avoided URL: ", link)
                continue
            elif link.startswith("https"):
                next_urls.append(link)
            elif link.startswith("/"):
                next_urls.append(URL + link)

    # print("Step 3 - Parsing Next URLs Data Successful!")
    print("3--------------------")
    return next_urls
"""


def parse_next_urls(parsed_data):
    next_urls = []
    all_link_tags = parsed_data.find_all("a")

    for tag in all_link_tags:
        link = tag.get("href")
        if not link:
            continue

        # Avoid invalid links
        avoid_list = ["#", "mailto:", "javascript:"]
        if any(bad in link for bad in avoid_list):
            continue

        # Absolute BBC links
        if link.startswith("https://www.bbc.com"):
            next_urls.append(link)

        # Internal links
        elif link.startswith("/"):
            next_urls.append(URL + link)

    print("Step 3 - Parsing Next URLs Data Successful!")
    print("===== End =====\n\n")
    return next_urls


def save_visited(visited):
    with open("visited.json", "w") as file:
        json.dump(list(visited), file, indent=4)


def save_frontier(frontier):
    with open("frontier.json", "w") as file:
        json.dump(frontier, file, indent=4)


frontier = ["https://www.bbc.com"]
visited = set()

"""
while len(frontier) > 0:
    current_url = frontier.pop(0)  # Removing URL from the Frontier List (DFS)
    if current_url in visited:
        continue
    res = fetch_page(current_url)
    parsed_data = parse_page(res)
    next_urls = parse_next_urls(parsed_data)
    frontier.extend(next_urls)
    visited[current_url] = ""  # REMOVE this line.
"""

while len(frontier) > 0:
    save_frontier(frontier)
    current_url = frontier.pop(0)

    if current_url in visited:
        continue
    visited.add(current_url)
    save_visited(visited)

    res = fetch_page(current_url)
    if not res:
        continue

    parsed_data = parse_page(res)
    next_urls = parse_next_urls(parsed_data)

    # Add only URLs that are not visited
    for url in next_urls:
        if url not in visited:
            frontier.append(url)
