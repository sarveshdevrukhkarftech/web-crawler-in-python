import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.bbc.com"


def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        print("===== Start =====")
        print("Step 1 - Fetching Data Successful!")
        return response
    except Exception as error:
        print(f"An Error Occurred: {error}")


def parse_page(res):
    # Creating soup to extract data.
    parsed_data = BeautifulSoup(res.text, "html.parser")  # Parsing Soup Data
    all_link_tags = parsed_data.find_all("a")  # Getting all <a> tags.

    # ----------
    title_tag = parsed_data.find("meta", property="og:title")
    if title_tag:
        og_title = title_tag.get("content")
    else:
        og_title = "not found"

    description_tag = parsed_data.find("meta", property="og:description")
    if description_tag:
        og_description = description_tag.get("content")
    else:
        og_description = "not found"

    image_tag = parsed_data.find("meta", property="og:image")
    if image_tag:
        og_image = image_tag.get("content")
    else:
        og_image = "not found"

    image_alt_tag = parsed_data.find("meta", property="og:image:alt")
    if image_alt_tag:
        og_image_alt = image_alt_tag.get("content")
    else:
        og_image_alt = "not found"

    print("OG Title:", og_title)
    print("OG Description:", og_description)
    print("OG Image URL:", og_image)
    print("OG Image Alt Text:", og_image_alt)
    print("---------------------------------------------------")
    # ----------

    print("Step 2 - Parsing Data Successful!")
    return all_link_tags


def parse_next_urls(all_link_tags):
    next_urls = []

    # Looping over tags to get 'href'
    for tag in all_link_tags:
        link = tag.get("href")

        # Checking 'link' has False value or not.
        if not link:
            continue

        # Avoid invalid links.
        avoid_list = [
            "#",
            "mailto:",
            "javascript:",
            "?page=",
            "?search=",
            "&sort=",
            "&filter=",
            "/av/",
        ]
        if any(bad in link for bad in avoid_list):
            continue

        # Absolute BBC links
        if link.startswith("https://www.bbc.com/news/"):
            next_urls.append(link)

        # Internal links
        elif link.startswith("/"):
            next_urls.append(URL + link)

    print("Step 3 - Parsing Next URLs Data Successful!")
    print("===== End =====\n\n")
    return next_urls


# Function to save visited links into the JSON file.
def save_visited(visited):
    with open("visited.json", "w") as file:
        json.dump(list(visited), file, indent=4)


frontier = ["https://www.bbc.com/news"]
visited = set()
MAX_PAGES = 500  # Setting limits to visit pages.

while len(frontier) > 0:
    # Max Page Limit
    if len(visited) >= MAX_PAGES:
        print("Reached max page limit. Stopping crawler.")
        break

    current_url = frontier.pop(0)

    # Crawl only particular pages.
    if not current_url.startswith("https://www.bbc.com/news"):
        continue

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
