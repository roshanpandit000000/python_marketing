from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time


options = Options()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Prevent GPU rendering issues
options.add_argument("--window-size=1920x1080")  # Set a default window size
options.add_argument("--no-sandbox")  # Bypass OS security model (useful for Linux)
options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
options.add_argument(
    "--disable-software-rasterizer"
)  # Disable WebGL software rendering fallback
options.add_argument("--log-level=3")  # Reduce Chrome log output

# Initialize WebDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


category = "lifestyle"
url = (
    f"https://www.hindustantimes.com/{category}"  # Replace with the actual article URL
)
driver.get(url)
wait = WebDriverWait(driver, 15)
print("✅ Page loaded successfully!")

try:
    wait = WebDriverWait(driver, 10)
    print("✅ First Article Find successfull...")
    links = driver.find_element(By.XPATH, "(//a[@class='storyLink articleClick'])[1]")
    links.click()
    print("✅ First Article clicked successfully!")

    # Check if redirected to a Google Vignette Ad
    time.sleep(3)  # Wait briefly to allow redirection
    if "#google_vignette" in driver.current_url:
        print("⚠ Google Vignette Ad detected! Going back and retrying...")
        driver.back()  # Go back to category page
        time.sleep(2)  # Wait for the page to load again
        first_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//a[@class='storyLink articleClick'])[1]")
            )
        )
        first_link.click()  # Click again
        print("✅ First Article clicked Again successfully!")
        # Wait for the actual article page to load
        time.sleep(2)

    wait.until(EC.presence_of_element_located((By.XPATH, "(//h1[@class='hdg1'])[1]")))

    print("✅ Article page loaded successfully!")

    h1_html = driver.find_element(By.XPATH, "(//h1[@class='hdg1'])[1]").get_attribute(
        "outerHTML"
    )

    print("✅ H1 HTML extracted successfully!")

    h2_html = driver.find_element(
        By.XPATH, "(//h2[@class='sortDec'])[1]"
    ).get_attribute("outerHTML")

    print("✅ H2 HTML extracted successfully!")

    full_url = driver.current_url
    base_url = "https://www.hindustantimes.com"
    relative_url = full_url.replace(base_url, "")

    print("✅ Relative URL extracted successfully!")

    detail_div = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//div[@class='detail ' and @dataid='{relative_url}']")
        )
    )

    print("✅ Detail div found successfully!")

    # Extract full detail_div HTML
    detail_html = detail_div.get_attribute("outerHTML")

    print("✅ Detail HTML extracted successfully!")

    # Combine <h1> and <h2> HTML
    article_html = f"{h1_html}\n{h2_html}\n{detail_html}"

    print("✅ Article HTML combined successfully!")

    # Save to an HTML file
    with open("scraped_article.html", "w", encoding="utf-8") as file:
        file.write(article_html)

    print("✅ Article HTML saved successfully!")

    driver.quit()
    print("✅ Browser closed successfully!")

except Exception as e:
    print(f"❌ Error {e}")
finally:
    driver.quit()
