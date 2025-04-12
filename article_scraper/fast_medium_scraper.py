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
    # "Programming",
    # "Self-Improvement",
    # "Sexuality",
    # "Writing",
    # "Data-Science",
    # "relationships",
    # "technology",
    # "cryptocurrency",
    # "politics",
    # "productivity",
    # "machine-Learning",
    # "money",
    # "psychology",
    # "pthon",
    # "health",
    # "business",
    # "science",
    # "software-Development",
    # "design",
    # "life",
    # "mental-Health",
    # "startup",
    # "film",
    # "photography",
    # "sports",
    # "travel",
    # "cybersecurity",
    # "climate-Change",
    # "world",
    # "creativity",
    # "education",
    # "blockchain",
    # "culture",
    # "javaScript",
    
]

articles_to_scrape = 10000  # Change this to scrape more or fewer articles

for category in categories:
    try:
        url = f"https://medium.com/tag/{category.lower().replace(' ', '-')}"
        driver.get(url)
        print(f"Opened Medium category: {category}")
        time.sleep(2)

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

        scroll_pause_time = 2
        max_scroll_attempts = 10  # safety limit to avoid infinite loop
        scroll_attempt = 0
        last_article_count = 0

        while scroll_attempt < max_scroll_attempts:
            # Store current article count
            before_scroll_count = len(
                driver.find_elements(By.XPATH, "//article[@data-testid='post-preview']")
            )

            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                # Wait up to 10s until new articles are loaded (count increases)
                WebDriverWait(driver, 10).until(
                    lambda d: len(
                        d.find_elements(
                            By.XPATH, "//article[@data-testid='post-preview']"
                        )
                    )
                    > before_scroll_count
                )
            except:
                print("No more articles loaded or timeout reached.")
                break

            scroll_attempt += 1
            current_count = len(
                driver.find_elements(By.XPATH, "//article[@data-testid='post-preview']")
            )
            print(f"Scrolled {scroll_attempt} times, found {current_count} articles...")

        article_elements = driver.find_elements(
            By.XPATH, "//article[@data-testid='post-preview']"
        )
        print(f"Found {len(article_elements)} articles on the page.")

        for i, article in enumerate(article_elements[:articles_to_scrape], start=1):
            try:
                print(f"\nScraping article {i} in category {category}...")

                # Extract h1
                h1_text = ""
                try:
                    h1_element = article.find_element(By.XPATH, ".//h2")
                    h1_text = h1_element.text.strip()
                except:
                    print("H1 Element Not Found")

                # Extract h2 or first p
                h2_text = ""
                try:
                    h2_element = article.find_element(By.XPATH, ".//h3")
                    h2_text = h2_element.text.strip()
                except:
                    print("No <h2> or <p> found.")

                # Extract image
                img_url = []
                try:
                    img_element = article.find_element(By.XPATH, ".//img[@width='160']")
                    img_url = img_element.get_attribute("src")
                except:
                    print("No images with width='160' found.")

                articles_data.append(
                    {
                        "category": category,
                        "article_number": i,
                        "title": h1_text,
                        "subtitle": h2_text,
                        "image_url": img_url,
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

                time.sleep(1)

            except Exception as article_error:
                print(f"Failed to scrape article {i} in {category}: {article_error}")
                driver.back()
                time.sleep(3)

    except Exception as e:
        print(f"Error loading category {category}: {e}")

time.sleep(5)
driver.quit()
