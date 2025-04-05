import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Open window maximized

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# API URL
api_url = "https://ridhaavhairstudio.in/api/products"

# List of Indian girl names
indian_girl_names = [
    "Ananya",
    "Priya",
    "Aaradhya",
    "Ishita",
    "Riya",
    "Meera",
    "Sanya",
    "Diya",
    "Kavya",
    "Tanvi",
    "Sneha",
    "Nisha",
    "Simran",
    "Aditi",
    "Pooja",
    "Shreya",
    "Neha",
    "Avni",
    "Trisha",
    "Swara",
    "Bhavya",
    "Jhanvi",
    "Vanya",
    "Ekta",
    "Charvi",
    "Radhika",
    "Sanvi",
    "Yashasvi",
    "Harini",
    "Muskan",
    "Mitali",
    "Chhavi",
    "Rupali",
    "Suhani",
    "Tisha",
    "Diksha",
    "Vaishnavi",
    "Aparna",
    "Pari",
    "Urvi",
    "Khushi",
    "Manvi",
    "Lavanya",
    "Saumya",
    "Harshita",
    "Sharvani",
    "Bhumi",
    "Rajeshwari",
    "Vibha",
    "Ritika",
]

# List of hair-extension-related comments
hair_comments = [
    "These extensions are absolutely stunning! So natural and soft.",
    "Blends seamlessly with my real hair. Couldn’t be happier!",
    "Amazing quality! The best hair extensions I have ever used.",
    "Super soft and silky. Feels just like real hair.",
    "Adds the perfect volume and length. Love it!",
    "The quality is unmatched. So easy to use and maintain.",
    "Looks completely natural. No one can tell it's an extension.",
    "Worth every penny! The texture is beautiful.",
    "The softness and shine are just perfect. Highly recommend!",
    "Gives my hair a flawless look. Perfect for special occasions.",
    "These extensions are a game-changer. Love the quality!",
    "So comfortable to wear, even for long hours.",
    "Doesn’t shed or tangle. Truly premium quality.",
    "I have tried many brands, but this one is the best!",
    "Very easy to clip in and stays secure all day.",
    "Instantly adds volume and enhances my overall look.",
    "The color matches my natural hair perfectly!",
    "Looks luxurious and feels incredibly soft.",
    "Perfect for styling in different ways. Holds curls well!",
    "The best investment I have made for my hair.",
    "So realistic that even my hairstylist was impressed!",
    "Love how lightweight yet voluminous these extensions are.",
    "Takes my hairstyle to the next level. So beautiful!",
    "The quality is fantastic, and they last a long time.",
    "Adds length and thickness effortlessly. Super happy!",
    "Very natural-looking and easy to maintain.",
    "They don’t feel heavy at all and stay in place perfectly.",
    "Perfect solution for thin hair. Looks so full and beautiful!",
    "Gives my hair a salon-finished look instantly.",
    "So versatile! Works great for both casual and formal looks.",
    "My go-to hair extensions. Never disappoints!",
    "These extensions exceeded my expectations in every way.",
    "Super soft, bouncy, and full of life!",
    "Does not tangle or shed even after multiple uses.",
    "Looks just like my natural hair, but better!",
    "The perfect hair extensions for a glamorous look.",
    "Feels like my own hair, just fuller and more beautiful!",
    "The texture and quality are absolutely top-notch.",
    "So easy to apply and remove without any damage.",
    "Gives a very polished and elegant look instantly.",
    "The hair is so soft and manageable. Totally love it!",
    "Great product! Exactly as described and worth the price.",
    "Stays in place all day without slipping. So secure!",
    "The color selection is amazing. I found my perfect match!",
    "These extensions made my hair look thick and healthy.",
    "Soft, silky, and blends beautifully with my hair.",
    "I get so many compliments whenever I wear them!",
    "Love the volume it adds without looking unnatural.",
    "The best hair extensions for everyday wear!",
    "These extensions have completely transformed my look!",
]

# Fetch product slugs from API
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Ensure request was successful
    products = response.json().get("allproducts", [])  # Extract products array
    product_slugs = [
        product["slug"] for product in products if "slug" in product
    ]  # Get slugs

except requests.exceptions.RequestException as e:
    print(f"Error fetching product data: {e}")
    driver.quit()
    exit()

try:
    for slug in product_slugs[11:50]:  # Only review the first 3 products
        product_url = f"https://ridhaavhairstudio.in/shop/{slug}"
        driver.get(product_url)
        time.sleep(3)

        for _ in range(5):  # Write 5 reviews per product
            # Step 1: Click "Write a Review" button
            review_button = driver.find_element(
                By.XPATH, "//button[.//p[text()='Write a review']]"
            )
            review_button.click()
            time.sleep(2)

            # Step 2: Fill "Your Name" input field with a unique name
            name_input = driver.find_element(By.ID, "text")
            unique_name = random.choice(indian_girl_names)
            name_input.clear()
            name_input.send_keys(unique_name)
            time.sleep(1)

            # Step 3: Select a 4-star rating
            stars = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'cursor-pointer') and contains(@class, 'text-3xl')][ancestor::form]",
            )
            if len(stars) >= 4:
                fourth_star = stars[3]
                actions = ActionChains(driver)
                actions.move_to_element(fourth_star).pause(1).click().perform()
                print(f"{unique_name} selected a 4-star rating!")
            else:
                print("Star rating elements not found!")

            time.sleep(1)

            # Step 4: Fill in the comment textarea with a unique review
            comment_box = driver.find_element(By.ID, "message-2")
            unique_comment = random.choice(hair_comments)
            comment_box.clear()
            comment_box.send_keys(unique_comment)
            print(f"{unique_name} commented: {unique_comment}")

            time.sleep(1)

            # Step 5: Click the "Comment" button
            comment_button = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Comment')]"
            )
            comment_button.click()
            print(f"Comment by {unique_name} submitted!")

            time.sleep(3)  # Wait before writing another review

        print(f"Finished 5 reviews for product: {slug}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
