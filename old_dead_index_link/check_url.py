from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

input_file = r"C:\Users\PcHelps\Documents\Python\old_dead_index_link\dead_links.json"
output_file = r"C:\Users\PcHelps\Documents\Python\old_dead_index_link\error_pages.json"

with open(input_file, "r") as f:
    urls = json.load(f)


chrome_options = Options()
chrome_options.add_argument("--headless")  # run without opening a window
chrome_options.add_argument("--disable-gpu")

# Adjust path if chromedriver is not in PATH
driver = webdriver.Chrome(options=chrome_options)


error_urls = []

for url in urls:
    try:

        driver.get(url)

        # Wait a bit if your page takes time to load content
        # driver.implicitly_wait(5)
        time.sleep(2)

        page_content = driver.page_source.lower()

        if (
            "application error" in page_content
            or "server-side exception" in page_content
            or "digest:" in page_content
        ):
            print(f"❌ URL ERROR PAGE (Next.js error): {url}")
            error_urls.append(url)
        else:
            print(f"✅ URL OK: {url}")

    except Exception as e:
        print(f"⚠️ Error accessing {url}: {str(e)}")
        error_urls.append(url)

# Save bad URLs to a new JSON file
with open(output_file, "w") as f:
    json.dump(error_urls, f, indent=4)

print(f"\n✅ Done. {len(error_urls)} error URLs saved to {output_file}")

driver.quit()
