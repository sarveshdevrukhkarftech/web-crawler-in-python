import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.bbc.com"  # Seed URL


# def fetch_page(url):
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         print("Fetching Successful!")
#         return response
#     except requests.exceptions.Timeout:
#         print("Request timed out")
#     except requests.exceptions.HTTPError as error:
#         print(f"HTTP error: {error}")
#     except requests.exceptions.RequestException as error:
#         print(f"Error during request: {error}")


def parse_page(response):
    path = "scraped-data/bbc_news.html"  # Path of the file to save Scraped Data.
    # texted_res = response.text
    # html_doc = texted_res

    """Creating new file with fetched response."""
    # with open(path, "w") as f:
    #     f.write(response.text)
    #     print("Data successfully saved into the file!")

    # Reading saved data file.
    with open(path, "r") as f:
        html_doc = f.read()

    # Creating soup to extract data.
    soup = BeautifulSoup(html_doc, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__").get_text(strip=True)
    json_soup = json.loads(script_tag)
    news_content_list = json_soup["props"]["pageProps"]["page"]['@"home",']["sections"][
        0
    ]["content"]
    return news_content_list


def parse_next_urls(news_content_data):
    next_urls = []
    for news in news_content_data:
        # half_url = news["href"]
        full_url = URL + news["href"]
        next_urls.append(full_url)
    return next_urls


# print(frontier)
frontier = []
visited = {}

# while len(frontier) > 0:
#     current_url = frontier.pop()  # Removing URL from the Frontier List and
#     if current_url in visited:
#         continue
#     response = fetch_page(current_url)
#     parsed_data = parse_page(response)
#     next_urls = parse_next_urls(response)
#     frontier.extend(next_urls)
#     visited[current_url] = ""

"""Main Code Execution."""
# res = fetch_page(URL)
news_content_data = parse_page()
frontier = [] + parse_next_urls(news_content_data)
current_url = (
    frontier.pop()
)  # Removes and returns the element at the specified position (or the last element if no index is specified).
