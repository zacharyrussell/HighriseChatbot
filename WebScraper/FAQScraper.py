import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

from ArticleToJSON import getDataframeforURL
# Accesses the Highrise FAQ page and scrapes questions and their corresponding answers


FAQ_url = "https://support.highrise.game/en/"

# The XPATH that points to the array of urls for different FAQ topics
div_XPATH = "/html/body/div[1]/div/main/div/section/section/div/div"



# Fetch the HTML content of the page
response = requests.get(FAQ_url)

response.raise_for_status()  # Ensure the request was successful

# Parse the HTML using lxml
tree = html.fromstring(response.content)
# Find the container
container = tree.xpath(div_XPATH)

collections = []
# Check if the container exists
if container:
    # Extract all <a> elements within the container
    a_elements = container[0].xpath(".//a")  # Use `.//a` to find <a> elements inside the container

    # Get the href attributes
    urls = [a.get('href') for a in a_elements if a.get('href')]

    print("Extracted URLs:")
    for url in urls:
        print(url)
        collections.append(url)
else:
    print(f"Container not found for XPath: {div_XPATH}")

all_articles = []
for collection in collections:
    # grab the url for each article
    collection_url = collection
    article_group_XPATH = "/html/body/div[1]/div/main/div/section/div[2]/div[2]/section"

    # Fetch the HTML content of the page
    response = requests.get(collection_url)

    response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML using lxml
    tree = html.fromstring(response.content)
    # Find the container
    container = tree.xpath(article_group_XPATH)
    if container:
        a_elements = container[0].xpath(".//a")  # Use `.//a` to find <a> elements inside the container

        # Get the href attributes
        urls = [a.get('href') for a in a_elements if a.get('href')]

        print("Extracted URLs:")
        for url in urls:
            print(url)
            all_articles.append(url)
    else:
        print(f"Container not found for XPath: {div_XPATH}")

dfs = []
for article in all_articles:
    print(article)
    dfs.append(getDataframeforURL(article))
result = pd.concat(dfs, ignore_index=True)
result.to_csv("aggregateDF.csv", sep='\t', index = False)

