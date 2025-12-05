import requests
from bs4 import BeautifulSoup
import json
import re
import sys

""" Utility """

URL = "https://www.bbc.com"


# Function to save visited links into the JSON file.
def save_og_data(og_data):
    with open("og_data.json", "w") as file:
        json.dump(og_data, file, indent=4)


# Function to save visited links into the JSON file.
def save_visited(visited):
    with open("visited.json", "w") as file:
        json.dump(list(visited), file, indent=4)


def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("===== Start =====\nStep 1 - Data Fetched.")
            return response
    except Exception as error:
        print(f"An Error Occurred: {error}")
        sys.exit()


def parse_page(res):
    """Creating soup to extract data."""
    parsed_data = BeautifulSoup(res.text, "html.parser")  # Parsing Soup Data
    all_link_tags = parsed_data.find_all("a")  # Getting all <a> tags.

    """ Function to get meta data. """

    def get_og(tag_name):
        tag = parsed_data.find("meta", property=tag_name)
        return tag.get("content") if tag else "not found"

    """ Storing OG data in dictionary. """
    og_data = {
        "title": get_og("og:title"),
        "description": get_og("og:description"),
        "image_url": get_og("og:image"),
        "image_url_alt": get_og("og:image:alt"),
    }

    print("Step 2 - Data Parsed.")
    return all_link_tags, og_data


def parse_next_urls(all_link_tags):
    next_urls = []

    """ Looping over tags to get 'href' """
    for tag in all_link_tags:
        link = tag.get("href")

        """ Checking 'link' has False value or not. """
        if not link:
            continue

        """ Avoiding invalid links. """
        avoided_url_pattern = [
            "#",
            "mailto:",
            "javascript:",
            "?page=",
            "?search=",
            "&sort=",
            "&filter=",
            "/av/",
        ]
        if any(bad in link for bad in avoided_url_pattern):
            continue

        """ Find only 'article' URL. """
        if re.search("articles", link):
            if link.startswith("/"):
                next_urls.append(URL + link)
            else:
                next_urls.append(link)
    print("Step 3 - Parsed Next URLs.\n===== End =====\n")
    return next_urls


""" Main Code Execution """
frontier = [URL]
visited = set()
results = list()

MAX_PAGES = 500  # Setting limits to visit pages.

while len(frontier) > 0:
    # Max Page Limit
    if len(visited) >= MAX_PAGES:
        print("Reached max page limit. Stopping crawler.")
        break
    current_url = frontier.pop(0)

    if current_url in visited:
        continue
    visited.add(current_url)

    if URL in visited:
        visited.remove(URL)
    save_visited(visited)
    res = fetch_page(current_url)  # Step-1

    # If result not found, stop the crawler.
    if not res:
        sys.exit()

    parsed_data, og_data = parse_page(res)  # Step-2
    results.append(og_data)  # Appending Data into List.
    save_og_data(results)  # Saving List of Data into JSON.
    next_urls = parse_next_urls(parsed_data)  # Step-3

    # Add only URLs that are not visited.
    for url in next_urls:
        if url not in visited:
            frontier.append(url)
