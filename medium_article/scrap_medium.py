from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import requests  # Import for API requests
import json
import re

# Set up Chrome to use an existing session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=chrome_options)  # Attach to existing browser

API_URL = "https://articlenest.vercel.app/api/article"

categories = [
    "Programming",
    "Self-Improvement",
    "Writing",
    "Data-Science",
    "Relationships",
    "Technology",
    "Cryptocurrency",
    "Politics",
    "Productivity",
    "Machine-Learning",
    "Money",
    "Psychology",
    "Python",
    "Health",
    "Business",
    "Science",
    "Software-Development",
    "Design",
    "Life",
    "Mental-Health",
    "Startup",
    "Film",
    "Photography",
    "Sports",
    "Travel",
    "Cybersecurity",
    "Climate-Change",
    "World",
    "Creativity",
    "Education",
    "Blockchain",
    "Culture",
    "JavaScript",
]

for category in categories:
    url = f"https://medium.com/tag/{category.lower().replace(' ', '-')}"
    driver.get(url)  # Open Medium category page
    print(f"Opened Medium category: {category}")
    time.sleep(3)  # Wait for page to load

    # Click the "See more recommended stories" button dynamically based on category
    try:
        see_more_button = driver.find_element(
            By.XPATH,
            f"//a[contains(@href, '/tag/{category.lower().replace(' ', '-')}/recommended')]",
        )
        see_more_button.click()
        print(f"Clicked 'See more recommended stories' for {category}!")
        time.sleep(4)
    except Exception as e:
        print(f"Error clicking button for {category}: {e}")

    # Select first Article
    try:
        click_article_button = driver.find_element(
            By.XPATH,
            "(//article[@data-testid='post-preview'])[1]",
        )
        click_article_button.click()
        print("Select First Article")
        time.sleep(4)
    except Exception as e:
        print(f"Click first Article error: {e}")

    h1_text = ""
    try:
        # Find the <h1> tag with 'data-testid' attribute
        h1_element = driver.find_element(By.XPATH, "//h1[@data-testid='storyTitle']")
        h1_text = h1_element.text.strip()

        slug = re.sub(r"[^\w\s-]", "", title).strip().lower().replace(" ", "-")

        # Save the main title text
        with open("data/scraped_text.txt", "w", encoding="utf-8") as file:
            file.write(h1_text)

        print("Title successfully saved to scraped_text.txt")

        # Scrape <h2> text (Subtitle)
        h2_text = ""
        try:
            h2_element = driver.find_element(
                By.XPATH, "(//h2[@data-selectable-paragraph])[1]"
            )  # Try default XPath
            h2_text = h2_element.text.strip()
        except:
            try:
                # If the first XPath fails, try this alternative
                print("H2 Element Not Found try frist paragraph tag")
                h2_element = driver.find_element(
                    By.XPATH, "(//h2[@data-selectable-paragraph])[1]"
                )
                h2_text = h2_element.text.strip()
            except:
                try:
                    # If no <h2> found, extract the first <p> instead
                    p_element = driver.find_element(
                        By.XPATH, "(//p[@data-selectable-paragraph])[1]"
                    )
                    h2_text = p_element.text.strip()
                    print("No <h2> found. Using first <p> as subtitle instead.")
                except:
                    print("No <h2> or <p> found.")

        # Save the extracted subtitle (either <h2> or <p>) to a file
        if h2_text:
            with open("data/subtitle_data.txt", "w", encoding="utf-8") as file:
                file.write(h2_text)

            print("Subtitle successfully saved to data/subtitle_data.txt")
        else:
            print("No subtitle found to save.")

        # Scrape Image URL (if available)
        img_url = ""
        try:
            img_element = driver.find_element(
                By.XPATH, "(//img[@role='presentation' and @loading='eager'])[1]"
            )  # Modify XPath if needed
            img_url = img_element.get_attribute("src")

            with open("data/image_url.txt", "w", encoding="utf-8") as file:
                file.write(img_url)

            print("Image URL successfully saved to data/image_url.txt")

        except:
            print("No image found with the specified class.")

            # Step 2: Open ChatGPT in a New Tab and Input the Title
        driver.execute_script(
            "window.open('https://chat.openai.com/', '_blank');"
        )  # Open ChatGPT in a new tab
        time.sleep(5)  # Wait for the ChatGPT page to load

        # Switch to the new tab (last opened tab)
        driver.switch_to.window(driver.window_handles[-1])
        print("open ChatGPT in New Tab Succesfull")
        # Find the input field and send the scraped title
        try:
            wait = WebDriverWait(driver, 20)
            input_box = driver.find_element(
                By.XPATH, "//div[@id='prompt-textarea']"
            )  # ChatGPT input field
            input_box.send_keys(f"Write an article about: {h1_text} in sandbox")
            time.sleep(3)
            input_box.send_keys(Keys.ENTER)  # Press Enter to submit
            print("Title sent to ChatGPT.")

            time.sleep(5)
            while True:
                try:
                    completion_element = driver.find_element(
                        By.XPATH,
                        "//button[@data-testid='composer-speech-button']",
                    )
                    time.sleep(5)
                    break  # Exit loop when found
                except:
                    time.sleep(7)  # Keep checking until found

            print("article write successfull")

            # Scrape the ChatGPT response
            try:
                chatgpt_response = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class, '_main_5jn6z_1') and contains(@class, 'markdown') and contains(@class, 'ProseMirror')]",
                ).get_attribute("outerHTML")

                soup = BeautifulSoup(chatgpt_response, "html.parser")
                # Define inline CSS for headings
                inline_css = "color: black; font-size: 20px; font-weight: bold;"

                # Apply inline CSS to all heading tags
                for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                    existing_style = heading.get("style", "")  # Get existing styles
                    heading["style"] = (
                        f"{existing_style} {inline_css}".strip()
                    )  # Append new styles

                # Add <br> tag after each <p> tag
                for p in soup.find_all("p"):
                    br_tag = soup.new_tag("br")  # Create a new <br> tag
                    p.insert_after(br_tag)  # Insert after each paragraph

                # Save modified HTML
                with open("data/description.html", "w", encoding="utf-8") as file:
                    file.write(str(soup))

                print(
                    "Modified ChatGPT response successfully saved to data/description.html"
                )

            except:
                print("Failed to scrape ChatGPT response.")

        except:
            print("Failed to send input to ChatGPT.")

    except Exception as e:
        print(f"⚠ Error Extract Data: {e}")

    # Inside the loop, after saving the data:
    try:
        # Load saved data
        with open("data/scraped_text.txt", "r", encoding="utf-8") as file:
            title = file.read().strip()

        with open("data/subtitle_data.txt", "r", encoding="utf-8") as file:
            subtitle = file.read().strip()

        with open("data/image_url.txt", "r", encoding="utf-8") as file:
            image_url = file.read().strip()

        with open("data/description.html", "r", encoding="utf-8") as file:
            description = file.read().strip()

        payload = {
            "title": title,
            "slug": slug,
            "shortDescription": subtitle,
            "mainDescription": description,
            "section": "section",
            "categories": category,
            "images": image_url,
        }

        # Send POST request
        response = requests.post(
            API_URL, json=payload, headers={"Content-Type": "application/json"}
        )

        # Check response status
        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Data successfully sent to API for category!")
        else:
            print(
                f"❌ Failed to send data. Status: {response.status_code}, Response: {response.text}"
            )

    except Exception as e:
        print(f"⚠ Error sending data to API: {e}")

    time.sleep(5)  # Wait for content to load
