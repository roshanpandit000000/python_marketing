import requests
from bs4 import BeautifulSoup
import re
import time
import random


def get_backlinks(domain):
    """Scrape backlinks using search engine queries."""
    search_url = (
        f'https://www.google.com/search?q=site:{domain}+-site:{domain}+"{domain}"'
    )
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        backlinks = []
        for link in soup.find_all("a", href=True):
            match = re.search(r"(https?://[\w./%-]+)", link["href"])
            if match:
                url = match.group(1)
                if domain not in url and "google.com" not in url:
                    backlinks.append(url)

        if backlinks:
            print(f"Found backlinks for {domain}:")
            for backlink in set(backlinks):
                print(backlink)
        else:
            print(f"No backlinks found for {domain}")

    except Exception as e:
        print(f"Error fetching backlinks: {e}")


def main():
    target_domain = "nishhair.com"  # Replace with your desired domain
    get_backlinks(target_domain)
    time.sleep(random.uniform(2, 5))  # Add delay to avoid getting blocked


if __name__ == "__main__":
    main()
