import requests
from lxml import html, etree
import pandas as pd

# URL of the webpage

def getDataframeforURL(url):
    # url = "https://support.highrise.game/en/articles/8894948-pinning"
    # url = "https://support.highrise.game/en/articles/8043116-how-do-i-play-highrise-what-is-this-game-about"


    # Fetch the HTML content of the page
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML using lxml
    tree = html.fromstring(response.content)

    # Initialize the data structure
    data = []

    # Extract the second <header> element
    header_elements = tree.xpath("//header")
    if len(header_elements) >= 2:
        header_element = header_elements[1]  # Get the second <header>
        header_text = header_element.text_content().strip()
        header_xpath = etree.ElementTree(tree).getpath(header_element)

        # Extract all <p> elements on the page
        p_elements = tree.xpath("//p")
        paragraphs = [p.text_content().strip() for p in p_elements]

        # Add the second <header> and its paragraphs as a single row
        data.append({
            "Header": header_text,
            "Header XPath": header_xpath,
            "Paragraphs": paragraphs
        })
    else:
        print("Second <header> element not found.")
        exit()

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    # print(df)
    return df