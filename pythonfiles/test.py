import requests
from bs4 import BeautifulSoup


def extract_text_from_site(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n")

        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None


url = "https://www.geeksforgeeks.org/"


site_text = extract_text_from_site(url)
if site_text:
    with open("file.txt", "w") as f:
        f.write(site_text)
    print(site_text)
