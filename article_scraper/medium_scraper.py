import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Attach to running browser session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# Create directory for saving data
os.makedirs("data", exist_ok=True)

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

articles_to_scrape = 10000  # Change this to scrape more or fewer articles

for category in categories:
    try:
        url = f"https://medium.com/tag/{category.lower().replace(' ', '-')}"
        driver.get(url)
        print(f"Opened Medium category: {category}")

        see_more_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//a[contains(@href, '/tag/{category.lower().replace(' ', '-')}/recommended')]",
                )
            )
        )
        see_more_button.click()
        print(f"Clicked 'See more recommended stories' for {category}")
        time.sleep(3)

        articles_data = []

        for i in range(1, articles_to_scrape + 1):
            try:
                print(f"\nScraping article {i} in category {category}...")

                article_xpath = f"(//article[@data-testid='post-preview'])[{i}]"
                article_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, article_xpath))
                )
                driver.execute_script("arguments[0].scrollIntoView();", article_element)
                article_element.click()
                time.sleep(4)

                # Extract h1
                h1_text = ""
                try:
                    h1_element = driver.find_element(
                        By.XPATH, "//h1[@data-testid='storyTitle']"
                    )
                    h1_text = h1_element.text.strip()
                except:
                    print("H1 Element Not Found")

                # Extract h2 or first p
                h2_text = ""
                try:
                    h2_element = driver.find_element(
                        By.XPATH, "(//h2[@data-selectable-paragraph])[1]"
                    )
                    h2_text = h2_element.text.strip()
                except:
                    try:
                        p_element = driver.find_element(
                            By.XPATH, "(//p[@data-selectable-paragraph])[1]"
                        )
                        h2_text = p_element.text.strip()
                        print("No <h2> found. Using first <p> instead.")
                    except:
                        print("No <h2> or <p> found.")

                # Extract image
                img_url = ""
                try:
                    img_element = driver.find_element(
                        By.XPATH,
                        "(//img[@role='presentation' and @loading='eager'])[1]",
                    )
                    img_url = img_element.get_attribute("src")
                except:
                    try:
                        more_image = driver.find_element(
                            By.XPATH, "(//img[@role='presentation' and @loading])[1]"
                        )
                        img_url = more_image.get_attribute("src")
                        print("No <h2> found. Using first <p> instead.")
                    except:
                        print("No <image> or <more image> found.")

                # Scrape all image URLs
                sub_images = []
                try:
                    img_elements = driver.find_elements(
                        By.XPATH, "//img[@role='presentation' and @loading]"
                    )
                    for img in img_elements:
                        src = img.get_attribute("src")
                        if src and src not in sub_images:
                            sub_images.append(src)
                except:
                    print("No images found.")

                articles_data.append(
                    {
                        "category": category,
                        "article_number": i,
                        "title": h1_text,
                        "subtitle": h2_text,
                        "image_url": img_url,
                        "sub_images": sub_images,
                    }
                )

                # Save data after each article
                with open(
                    f"data/{category.lower().replace(' ', '_')}.json",
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(articles_data, f, ensure_ascii=False, indent=2)

                print(f"Saved article {i} for {category}")

                driver.back()
                time.sleep(2)

            except Exception as article_error:
                print(f"Failed to scrape article {i} in {category}: {article_error}")
                driver.back()
                time.sleep(3)

    except Exception as e:
        print(f"Error loading category {category}: {e}")

time.sleep(5)
# driver.quit()
