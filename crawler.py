import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com"


def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print("Step 1 - Fetching Data Successful!")
        return response
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Error during request: {error}")


def parse_page(res):
    # Creating soup to extract data.
    parsed_data = BeautifulSoup(res.text, "html.parser")  # Parsing Soup Data
    print("Step 2 - Parsing Data Successful!")
    return parsed_data


def parse_next_urls(parsed_data):
    next_urls = []
    all_link_tags = parsed_data.find_all("a")
    for tag in all_link_tags:
        link = tag.get("href")

        # Checking URL is valid or not.
        if link.startswith("#"):
            continue
        if link.startswith("https://help.bbc.com/hc/"):
            continue
        if link.startswith("https"):
            next_urls.append(link)

        if link.startswith("/"):
            next_urls.append(URL + link)

    print("Step 3 - Parsing Next URLs Data Successful!")
    return next_urls


frontier = ["https://www.bbc.com"]
visited = {}

while len(frontier) > 0:
    current_url = frontier.pop()  # Removing URL from the Frontier List (DFS)
    if current_url in visited:
        continue
    res = fetch_page(current_url)
    parsed_data = parse_page(res)
    next_urls = parse_next_urls(parsed_data)
    frontier.extend(next_urls)
    visited[current_url] = ""  # REMOVE this line.
    # visited.add(current_url)