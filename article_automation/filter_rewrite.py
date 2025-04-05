from bs4 import BeautifulSoup
import re


def clean_html(html_content):
    """Removes unnecessary divs and extracts main content."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove ad-related divs and empty tags
    for tag in soup.find_all(
        ["div", "span"], class_=re.compile("ad|promo|poll|storyAd", re.I)
    ):
        tag.decompose()

    # Extract relevant content (headings, paragraphs, images)
    cleaned_content = ""
    for tag in soup.find_all(["h1", "h2", "p", "img"]):
        if tag.name == "img":
            img_tag = f'<img src="{tag.get("src")}" alt="{tag.get("alt", "")}">\n'
            cleaned_content += img_tag
        else:
            text = tag.get_text(strip=True)
            if text:
                cleaned_content += f"<{tag.name}>{text}</{tag.name}>\n"
        print("✅ Cleaned", cleaned_content)
    return cleaned_content
