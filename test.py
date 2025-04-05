import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def task_1():
    driver = setup_driver()
    driver.get("https://www.medium.com")
    print("Opened Medium")
    driver.quit()


def task_2():
    driver = setup_driver()
    driver.get("https://www.linkedin.com")
    print("Opened LinkedIn")
    driver.quit()


# Run both functions at the same time
thread1 = threading.Thread(target=task_1)
thread2 = threading.Thread(target=task_2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Both tasks completed!")
