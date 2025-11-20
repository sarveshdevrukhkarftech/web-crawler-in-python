- fetchData.py

```fetchData.py
import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com"
path = "scraped-data/bbc_news.html"  # Path of the file to save Scraped Data.


def fetch_and_save_data(url, path):
    try:
        response = requests.get(url, timeout=5)  # Making API Call.
        response.raise_for_status()  # raises an error for 4xx/5xx if occurred.
        print("Data Fetched Successfully!")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Error during request: {error}")

    # Creating new file with fetched response.
    with open(path, "w") as file:
        file.write(response.text)
        print("Data successfully saved in file!")


# Function Calling: Main Execution
fetch_and_save_data(url, path)

"""Code """

readFilePath = "scraped-data/bbc_news.html"  # Path of the file to Scrap Data.


def scrap_and_save_data(readFilePath):
    with open(readFilePath, "r") as file:
        html_doc = file.read()

    soup = BeautifulSoup(html_doc, "html.parser")

    script_tag = soup.find(id="__NEXT_DATA__").get_text(strip=True)
    print(type(script_tag))


# Function Calling: Main Execution
scrap_and_save_data(readFilePath)

```

- scrapeData.py

```scrapeData.py
from bs4 import BeautifulSoup

readFilePath = "scraped-data/bbc_news.html"  # Path of the file to Scrap Data.


def scrap_and_save_data(readFilePath):
    with open(readFilePath, "r") as file:
        html_doc = file.read()

    soup = BeautifulSoup(html_doc, "html.parser")

    script_tag = soup.find(id="__NEXT_DATA__").get_text(strip=True)
    print(type(script_tag))


# Function Calling: Main Execution
scrap_and_save_data(readFilePath)
```
