from bs4 import BeautifulSoup
import requests


def extract_first_image(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    first_img = soup.find("img")
    if first_img and first_img.has_attr("src"):
        return first_img["src"]
    return None


def clean_chatgpt_response(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        unwanted_spans = soup.find_all("span", class_="text-token-text-tertiary")
        for span in unwanted_spans:
            parent_p_tag = span.find_parent(
                "p"
            )  # Find the <p> tag that contains the <span>
            if parent_p_tag:
                parent_p_tag.decompose()

    # print("soup", soup)

    return str(soup)  # Return cleaned HTML as a string


def post_to_api(
    title, slug, shortDescription, mainDescription, section, categories, images
):
    api_url = "https://articlenest.vercel.app/api/article"  # Replace with your actual API URL https://articlenest.vercel.app/api/article

    # Prepare data to send
    data = {
        "title": title,
        "slug": slug,
        "shortDescription": shortDescription,
        "mainDescription": mainDescription,
        "section": section,
        "categories": categories,
        "images": images,
    }

    # Headers with Content-Type
    headers = {"Content-Type": "application/json"}
    # print("Data being sent:", data)
    # Make POST request
    try:
        response = requests.post(api_url, json=data, headers=headers)

        # Log response status and content for debugging
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)
        print("Response Content:", response.content)

        # Check for successful response
        if response.status_code == 200:
            if response.text.strip():  # Check if the response text is not empty
                try:
                    # Attempt to parse the response as JSON
                    return response.json()
                except requests.exceptions.JSONDecodeError:
                    print("Invalid JSON response.")
                    return None
            else:
                print("Empty response received.")
                return None
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle exceptions like connection issues or timeout
        print(f"Request failed: {e}")
        return None


def process_and_post():
    # 1. Extract image src from scraped_article.html
    image_src = extract_first_image("scraped_article.html")
    if not image_src:
        print("No image found in scraped_article.html")
        return

    # 2. Clean chatgpt_response.html
    cleaned_html = clean_chatgpt_response("chatgpt_response.html")
    if not cleaned_html:
        print("No image found in chatgpt_response.html")
        return

    # print("Clean Html", cleaned_html)

    # 3. Prepare data to send to API
    title = "Article Title"  # Example, set your actual values
    slug = "article-slu-1g"
    shortDescription = "This is a short description"
    mainDescription = cleaned_html  # Main description is the cleaned HTML
    section = "technology"
    categories = "category2"
    images = image_src  # List of image sources

    # 4. Send data to Next.js API
    api_response = post_to_api(
        title, slug, shortDescription, mainDescription, section, categories, images
    )

    print("API Response:", api_response)


# Run the function
process_and_post()
