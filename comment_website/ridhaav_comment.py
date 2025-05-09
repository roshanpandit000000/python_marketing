import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
# API URL
api_url = "https://bellahararo.com/api/products"

# List of Indian girl names
western_girl_names = [
    "Ariana A.",
    "Aria G.",
    "Caroline H.",
    "Josephine E.",
    "Leah F.",
    "Grace E.",
    "Nevaeh E.",
    "Ariana D.",
    "Arianna C.",
    "Eliana C.",
    "Emery E.",
    "Clara E.",
    "Riley D.",
    "Adeline G.",
    "Genesis F.",
    "Brielle E.",
    "Hailey H.",
    "Scarlett A.",
    "Ella F.",
    "Autumn C.",
    "Quinn F.",
    "Lydia H.",
    "Genesis",
    "Emily K.",
    "Abigail G.",
    "Everly G.",
    "Ruby D.",
    "Bella C.",
    "Zoey A.",
    "Brooklyn C.",
    "Isabella E.",
    "Naomi K.",
    "Piper E.",
    "Isla A.",
    "Allison",
    "Brooklyn A.",
    "Delilah J.",
    "Bella G.",
    "Skylar E.",
    "Layla B.",
    "Melanie B.",
    "Sadie H.",
    "Brooklyn F.",
    "Sophie K.",
    "Brooklyn G.",
    "Zoey F.",
    "Hannah",
    "Reagan C.",
    "Sophia K.",
    "Lily B.",
    "Cora C.",
    "Isabella D.",
    "Vivian G.",
    "Addison F.",
    "Avery H.",
    "Rylee B.",
    "Valentina F.",
    "Jade",
    "Gianna F.",
    "Sophie B.",
    "Samantha",
    "Emilia G.",
    "Adeline E.",
    "Sophie D.",
    "Everly C.",
    "Peyton E.",
    "Lily K.",
    "Brielle K.",
    "Emily D.",
    "Alexa",
    "Valentina A.",
    "Zoe F.",
    "Nevaeh B.",
    "Ellie J.",
    "Layla F.",
    "Sadie C.",
    "Gianna",
    "Mia D.",
    "Willow D.",
    "Peyton G.",
    "Aubrey C.",
    "Arianna",
    "Zoe",
    "Addison J.",
    "Ellie A.",
    "Melanie H.",
    "Vivian K.",
    "Violet B.",
    "Kinsley J.",
    "Eliana E.",
    "Sadie G.",
    "Rylee E.",
    "Caroline C.",
    "Charlotte",
    "Camila J.",
    "Ella H.",
    "Eliana B.",
    "Adalynn",
    "Natalie B.",
    "Samantha H.",
    "Isla D.",
    "Savannah D.",
    "Gabriella",
    "Rylee D.",
    "Madelyn E.",
    "Riley E.",
    "Olivia H.",
    "Isabella A.",
    "Lydia A.",
    "Aaliyah H.",
    "Gabriella A.",
    "Josephine B.",
    "Hadley G.",
    "Hazel K.",
    "Grace J.",
    "Reagan B.",
    "Kennedy K.",
    "Melanie D.",
    "Aria E.",
    "Brielle D.",
    "Audrey G.",
    "Naomi D.",
    "Maya F.",
    "Allison H.",
    "Eliana",
    "Sarah A.",
    "Violet",
    "Sadie K.",
    "Abigail J.",
    "Nora K.",
    "Addison D.",
    "Naomi B.",
    "Olivia C.",
    "Madelyn F.",
    "Kennedy E.",
    "Adalynn J.",
    "Emilia F.",
    "Willow A.",
    "Chloe K.",
    "Vivian H.",
    "Kennedy F.",
    "Violet F.",
    "Addison G.",
    "Audrey A.",
    "Willow B.",
    "Mia K.",
    "Olivia G.",
    "Lily D.",
    "Audrey F.",
    "Abigail",
    "Aubrey H.",
    "Allison C.",
    "Quinn K.",
    "Anna A.",
    "Ivy K.",
    "Clara D.",
    "Brooklyn B.",
    "Savannah E.",
    "Camila C.",
    "Reagan H.",
    "Camila G.",
    "Samantha B.",
    "Lillian G.",
    "Layla K.",
    "Isla E.",
    "Ruby J.",
    "Hailey E.",
    "Ariana H.",
    "Savannah A.",
    "Kennedy J.",
    "Hailey K.",
    "Stella C.",
    "Ellie G.",
    "Eva J.",
    "Quinn J.",
    "Julia G.",
    "Vivian A.",
    "Avery B.",
    "Piper B.",
    "Mackenzie H.",
    "Scarlett F.",
    "Sarah F.",
    "Madeline",
    "Nova K.",
    "Allison K.",
    "Camila E.",
    "Reagan",
    "Bella F.",
    "Aubrey D.",
    "Jade G.",
    "Reagan K.",
    "Julia D.",
    "Eliana J.",
    "Violet H.",
    "Eva F.",
    "Olivia K.",
    "Jade E.",
    "Aubrey B.",
    "Quinn",
    "Isabella",
    "Lily F.",
    "Lily A.",
    "Quinn D.",
    "Brielle B.",
    "Cora E.",
    "Hadley F.",
    "Hailey J.",
    "Bella E.",
    "Lillian K.",
    "Willow C.",
    "Piper H.",
    "Addison A.",
    "Reagan G.",
    "Arianna B.",
    "Ellie B.",
    "Sarah K.",
    "Adeline K.",
    "Autumn H.",
    "Lillian C.",
    "Adeline H.",
    "Vivian D.",
    "Aaliyah K.",
    "Lucy K.",
    "Elena D.",
    "Kaylee J.",
    "Eliana F.",
    "Nevaeh J.",
    "Evelyn F.",
    "Gabriella H.",
    "Brooklyn E.",
    "Aubrey A.",
    "Elena J.",
    "Maya D.",
    "Adeline B.",
    "Scarlett C.",
    "Nova E.",
    "Valentina G.",
    "Savannah",
    "Violet G.",
    "Genesis K.",
    "Julia H.",
    "Adalynn K.",
    "Autumn K.",
    "Savannah C.",
    "Emery D.",
    "Julia A.",
    "Sofia E.",
    "Mia E.",
    "Olivia B.",
    "Mackenzie B.",
    "Aria",
    "Jade D.",
    "Sofia D.",
    "Nova J.",
    "Anna C.",
    "Valentina C.",
    "Lucy C.",
    "Grace G.",
]
# List of hair-extension-related comments
hair_comments = [
    "The quality is just out of this world! No one can even tell I'm wearing extensions. A total game-changer.",
    "These extensions are absolutely stunning! They hold curls beautifully. Five stars all the way!",
    "Incredibly smooth and blends perfectly. No tangling or shedding at all! Definitely buying more.",
    "Hands down, the best hair extensions out there. Blends so well with my natural hair. Bella Hararo nailed it.",
    "Truly the best extensions I've ever tried! They feel like silk in my hands. A must-have for anyone using extensions.",
    "Incredibly smooth and blends perfectly. So natural and soft. Highly recommend to anyone!",
    "So soft and realistic — amazing quality. Feels and looks just like my real hair. Exceeded my expectations.",
    "Truly the best extensions I've ever tried! No tangling or shedding at all! A must-have for anyone using extensions.",
    "Incredibly smooth and blends perfectly. I get compliments every time I wear them. A must-have for anyone using extensions.",
    "Truly the best extensions I've ever tried! Super lightweight and comfortable to wear. A must-have for anyone using extensions.",
    "Totally worth it — feels like my real hair. They hold curls beautifully. Bella Hararo nailed it.",
    "These extensions are absolutely stunning! They hold curls beautifully. Five stars all the way!",
    "Absolutely love how these feel and look. I get compliments every time I wear them. Will tell all my friends about this.",
    "I'm blown away by how natural these look. No one can even tell I'm wearing extensions. Will tell all my friends about this.",
    "Hands down, the best hair extensions out there. Feels and looks just like my real hair. A must-have for anyone using extensions.",
    "Totally worth it — feels like my real hair. They feel like silk in my hands. Exceeded my expectations.",
    "The quality is just out of this world! No tangling or shedding at all! Five stars all the way!",
    "Absolutely love how these feel and look. They hold curls beautifully. A must-have for anyone using extensions.",
    "Totally worth it — feels like my real hair. They hold curls beautifully. Five stars all the way!",
    "Unbelievably soft and beautiful. Blends so well with my natural hair. A must-have for anyone using extensions.",
    "I'm blown away by how natural these look. No one can even tell I'm wearing extensions. Five stars all the way!",
    "Unbelievably soft and beautiful. No one can even tell I'm wearing extensions. Definitely buying more.",
    "Hands down, the best hair extensions out there. Blends so well with my natural hair. A must-have for anyone using extensions.",
    "These extensions are absolutely stunning! No tangling or shedding at all! Couldn’t be happier!",
    "These extensions are absolutely stunning! No one can even tell I'm wearing extensions. I’m never going back to other brands.",
    "Truly the best extensions I've ever tried! Blends so well with my natural hair. I’m never going back to other brands.",
    "The quality is just out of this world! No tangling or shedding at all! Exceeded my expectations.",
    "I'm blown away by how natural these look. They feel like silk in my hands. A must-have for anyone using extensions.",
    "Hands down, the best hair extensions out there. Perfect match for my hair color and texture. A total game-changer.",
    "Hands down, the best hair extensions out there. Blends so well with my natural hair. Will tell all my friends about this.",
    "Unbelievably soft and beautiful. Super lightweight and comfortable to wear. Exceeded my expectations.",
    "Hands down, the best hair extensions out there. They hold curls beautifully. A total game-changer.",
    "These extensions are absolutely stunning! So natural and soft. Exceeded my expectations.",
    "Truly the best extensions I've ever tried! Feels and looks just like my real hair. Will tell all my friends about this.",
    "Truly the best extensions I've ever tried! I get compliments every time I wear them. A total game-changer.",
    "These extensions are absolutely stunning! No tangling or shedding at all! Highly recommend to anyone!",
    "Absolutely love how these feel and look. Perfect match for my hair color and texture. A must-have for anyone using extensions.",
    "Absolutely love how these feel and look. Super lightweight and comfortable to wear. A total game-changer.",
    "Absolutely love how these feel and look. Perfect match for my hair color and texture. A must-have for anyone using extensions.",
    "The quality is just out of this world! No tangling or shedding at all! Highly recommend to anyone!",
    "Totally worth it — feels like my real hair. Perfect match for my hair color and texture. Couldn’t be happier!",
    "Incredibly smooth and blends perfectly. Super lightweight and comfortable to wear. Five stars all the way!",
    "These extensions are absolutely stunning! Perfect match for my hair color and texture. Will tell all my friends about this.",
    "Incredibly smooth and blends perfectly. I get compliments every time I wear them. Five stars all the way!",
    "Truly the best extensions I've ever tried! So natural and soft. Will tell all my friends about this.",
    "Absolutely love how these feel and look. So natural and soft. A total game-changer.",
    "These extensions are absolutely stunning! No one can even tell I'm wearing extensions. Definitely buying more.",
    "Truly the best extensions I've ever tried! They feel like silk in my hands. I’m never going back to other brands.",
    "So soft and realistic — amazing quality. Super lightweight and comfortable to wear. Five stars all the way!",
    "So soft and realistic — amazing quality. Blends so well with my natural hair. Couldn’t be happier!",
    "So soft and realistic — amazing quality. No tangling or shedding at all! Highly recommend to anyone!",
    "These extensions are absolutely stunning! So natural and soft. Couldn’t be happier!",
    "Unbelievably soft and beautiful. They hold curls beautifully. I’m never going back to other brands.",
    "Unbelievably soft and beautiful. Feels and looks just like my real hair. A must-have for anyone using extensions.",
    "These extensions are absolutely stunning! I get compliments every time I wear them. Couldn’t be happier!",
    "These extensions are absolutely stunning! Blends so well with my natural hair. Exceeded my expectations.",
    "The quality is just out of this world! Super lightweight and comfortable to wear. Couldn’t be happier!",
    "Totally worth it — feels like my real hair. Super lightweight and comfortable to wear. Bella Hararo nailed it.",
    "Incredibly smooth and blends perfectly. Perfect match for my hair color and texture. Exceeded my expectations.",
    "Absolutely love how these feel and look. Super lightweight and comfortable to wear. Five stars all the way!",
    "I'm blown away by how natural these look. So natural and soft. Will tell all my friends about this.",
    "Unbelievably soft and beautiful. No one can even tell I'm wearing extensions. I’m never going back to other brands.",
    "I'm blown away by how natural these look. Perfect match for my hair color and texture. Five stars all the way!",
    "Absolutely love how these feel and look. Perfect match for my hair color and texture. Highly recommend to anyone!",
    "Truly the best extensions I've ever tried! Super lightweight and comfortable to wear. Will tell all my friends about this.",
    "Totally worth it — feels like my real hair. Super lightweight and comfortable to wear. Bella Hararo nailed it.",
    "So soft and realistic — amazing quality. Perfect match for my hair color and texture. Couldn’t be happier!",
    "Truly the best extensions I've ever tried! Super lightweight and comfortable to wear. Bella Hararo nailed it.",
    "Totally worth it — feels like my real hair. No tangling or shedding at all! Couldn’t be happier!",
    "Hands down, the best hair extensions out there. I get compliments every time I wear them. Will tell all my friends about this.",
    "I'm blown away by how natural these look. Feels and looks just like my real hair. Five stars all the way!",
    "So soft and realistic — amazing quality. So natural and soft. Couldn’t be happier!",
    "Incredibly smooth and blends perfectly. I get compliments every time I wear them. I’m never going back to other brands.",
    "So soft and realistic — amazing quality. Feels and looks just like my real hair. Couldn’t be happier!",
    "The quality is just out of this world! Perfect match for my hair color and texture. A total game-changer.",
    "Truly the best extensions I've ever tried! Feels and looks just like my real hair. Exceeded my expectations.",
    "Absolutely love how these feel and look. They hold curls beautifully. Definitely buying more.",
    "These extensions are absolutely stunning! No one can even tell I'm wearing extensions. Will tell all my friends about this.",
    "These extensions are absolutely stunning! I get compliments every time I wear them. Couldn’t be happier!",
    "The quality is just out of this world! Blends so well with my natural hair. Definitely buying more.",
    "The quality is just out of this world! So natural and soft. Bella Hararo nailed it.",
    "Absolutely love how these feel and look. Super lightweight and comfortable to wear. Bella Hararo nailed it.",
    "So soft and realistic — amazing quality. I get compliments every time I wear them. Exceeded my expectations.",
    "I'm blown away by how natural these look. Feels and looks just like my real hair. Five stars all the way!",
    "Unbelievably soft and beautiful. So natural and soft. A total game-changer.",
    "These extensions are absolutely stunning! So natural and soft. I’m never going back to other brands.",
    "Incredibly smooth and blends perfectly. Perfect match for my hair color and texture. I’m never going back to other brands.",
    "Totally worth it — feels like my real hair. Feels and looks just like my real hair. Couldn’t be happier!",
    "The quality is just out of this world! No tangling or shedding at all! A must-have for anyone using extensions.",
    "So soft and realistic — amazing quality. I get compliments every time I wear them. Will tell all my friends about this.",
    "Unbelievably soft and beautiful. They feel like silk in my hands. A total game-changer.",
    "So soft and realistic — amazing quality. They feel like silk in my hands. Exceeded my expectations.",
    "Truly the best extensions I've ever tried! No one can even tell I'm wearing extensions. Bella Hararo nailed it.",
    "So soft and realistic — amazing quality. I get compliments every time I wear them. A must-have for anyone using extensions.",
    "So soft and realistic — amazing quality. Blends so well with my natural hair. Exceeded my expectations.",
    "Totally worth it — feels like my real hair. Perfect match for my hair color and texture. A total game-changer.",
    "Totally worth it — feels like my real hair. Super lightweight and comfortable to wear. A total game-changer.",
    "Hands down, the best hair extensions out there. Feels and looks just like my real hair. Bella Hararo nailed it.",
    "These extensions are absolutely stunning! They hold curls beautifully. I’m never going back to other brands.",
    "Hands down, the best hair extensions out there. Blends so well with my natural hair. Five stars all the way!",
    "These extensions are absolutely stunning! They hold curls beautifully. A must-have for anyone using extensions.",
    "Totally worth it — feels like my real hair. No one can even tell I'm wearing extensions. Bella Hararo nailed it.",
    "The quality is just out of this world! I get compliments every time I wear them. Exceeded my expectations.",
    "These extensions are absolutely stunning! Super lightweight and comfortable to wear. A must-have for anyone using extensions.",
    "Incredibly smooth and blends perfectly. Blends so well with my natural hair. Exceeded my expectations.",
    "These extensions are absolutely stunning! Feels and looks just like my real hair. Bella Hararo nailed it.",
    "Totally worth it — feels like my real hair. I get compliments every time I wear them. Bella Hararo nailed it.",
    "Hands down, the best hair extensions out there. They feel like silk in my hands. A must-have for anyone using extensions.",
    "Truly the best extensions I've ever tried! So natural and soft. Definitely buying more.",
    "Totally worth it — feels like my real hair. No one can even tell I'm wearing extensions. Bella Hararo nailed it.",
    "Hands down, the best hair extensions out there. Feels and looks just like my real hair. Exceeded my expectations.",
    "Unbelievably soft and beautiful. Perfect match for my hair color and texture. Five stars all the way!",
    "Incredibly smooth and blends perfectly. Super lightweight and comfortable to wear. Will tell all my friends about this.",
    "Incredibly smooth and blends perfectly. No one can even tell I'm wearing extensions. Couldn’t be happier!",
    "So soft and realistic — amazing quality. No tangling or shedding at all! Will tell all my friends about this.",
    "Hands down, the best hair extensions out there. No one can even tell I'm wearing extensions. A must-have for anyone using extensions.",
    "These extensions are absolutely stunning! Perfect match for my hair color and texture. A total game-changer.",
    "These extensions are absolutely stunning! Perfect match for my hair color and texture. A total game-changer.",
    "Totally worth it — feels like my real hair. I get compliments every time I wear them. A must-have for anyone using extensions.",
    "The quality is just out of this world! They hold curls beautifully. Definitely buying more.",
    "Truly the best extensions I've ever tried! Super lightweight and comfortable to wear. Definitely buying more.",
    "Unbelievably soft and beautiful. They hold curls beautifully. Highly recommend to anyone!",
    "So soft and realistic — amazing quality. No tangling or shedding at all! Will tell all my friends about this.",
    "So soft and realistic — amazing quality. No one can even tell I'm wearing extensions. I’m never going back to other brands.",
    "Absolutely love how these feel and look. So natural and soft. Couldn’t be happier!",
    "Unbelievably soft and beautiful. No one can even tell I'm wearing extensions. Exceeded my expectations.",
    "These extensions are absolutely stunning! Super lightweight and comfortable to wear. Couldn’t be happier!",
    "The quality is just out of this world! I get compliments every time I wear them. A must-have for anyone using extensions.",
    "Absolutely love how these feel and look. No one can even tell I'm wearing extensions. A must-have for anyone using extensions.",
    "I'm blown away by how natural these look. So natural and soft. A total game-changer.",
    "So soft and realistic — amazing quality. No one can even tell I'm wearing extensions. Exceeded my expectations.",
    "These extensions are absolutely stunning! So natural and soft. Five stars all the way!",
    "Unbelievably soft and beautiful. They hold curls beautifully. I’m never going back to other brands.",
    "These extensions are absolutely stunning! I get compliments every time I wear them. A must-have for anyone using extensions.",
    "I'm blown away by how natural these look. Blends so well with my natural hair. Definitely buying more.",
    "The quality is just out of this world! Feels and looks just like my real hair. A total game-changer.",
    "Totally worth it — feels like my real hair. No tangling or shedding at all! A total game-changer.",
    "The quality is just out of this world! So natural and soft. Will tell all my friends about this.",
    "These extensions are absolutely stunning! Perfect match for my hair color and texture. A must-have for anyone using extensions.",
    "The quality is just out of this world! Super lightweight and comfortable to wear. A must-have for anyone using extensions.",
    "Totally worth it — feels like my real hair. I get compliments every time I wear them. Bella Hararo nailed it.",
    "The quality is just out of this world! So natural and soft. A must-have for anyone using extensions.",
    "The quality is just out of this world! So natural and soft. Five stars all the way!",
    "So soft and realistic — amazing quality. Super lightweight and comfortable to wear. Bella Hararo nailed it.",
    "Incredibly smooth and blends perfectly. So natural and soft. A must-have for anyone using extensions.",
    "The quality is just out of this world! Feels and looks just like my real hair. A total game-changer.",
    "Absolutely love how these feel and look. They feel like silk in my hands. I’m never going back to other brands.",
    "Totally worth it — feels like my real hair. No tangling or shedding at all! Bella Hararo nailed it.",
    "Totally worth it — feels like my real hair. Super lightweight and comfortable to wear. Five stars all the way!",
    "Incredibly smooth and blends perfectly. They feel like silk in my hands. Five stars all the way!",
    "Incredibly smooth and blends perfectly. So natural and soft. Highly recommend to anyone!",
    "The quality is just out of this world! No one can even tell I'm wearing extensions. Bella Hararo nailed it.",
    "Truly the best extensions I've ever tried! They feel like silk in my hands. Exceeded my expectations.",
    "Totally worth it — feels like my real hair. They hold curls beautifully. A must-have for anyone using extensions.",
    "I'm blown away by how natural these look. So natural and soft. A total game-changer.",
    "Hands down, the best hair extensions out there. Feels and looks just like my real hair. Couldn’t be happier!",
    "Truly the best extensions I've ever tried! Blends so well with my natural hair. Couldn’t be happier!",
    "The quality is just out of this world! I get compliments every time I wear them. Highly recommend to anyone!",
    "These extensions are absolutely stunning! Perfect match for my hair color and texture. Definitely buying more.",
    "I'm blown away by how natural these look. No one can even tell I'm wearing extensions. A total game-changer.",
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
    name_comment_pairs = list(zip(western_girl_names, hair_comments))
    total_pairs = len(name_comment_pairs)
    pair_index = 0
    for index, slug in enumerate(
        product_slugs[186:], start=186
    ):  # Only review the first 3 products
        product_url = f"https://bellahararo.com/shop/{slug}"
        driver.get(product_url)
        time.sleep(1)

        for _ in range(5):  # Write 5 reviews per product
            if pair_index >= total_pairs:
                print("All name/comment pairs used. Stopping.")
                driver.quit()
                exit()
            # Step 1: Click "Write a Review" button
            current_name, current_comment = name_comment_pairs[pair_index]
            pair_index += 1

            review_button = driver.find_element(
                By.XPATH, "//button[.//p[text()='Write a review']]"
            )
            review_button.click()
            time.sleep(1)

            # Step 2: Fill "Your Name" input field with a unique name
            name_input = driver.find_element(By.ID, "text")
            name_input.clear()
            name_input.send_keys(current_name)
            # time.sleep(1)

            # Step 3: Select a 4-star rating
            stars = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'cursor-pointer') and contains(@class, 'text-3xl')][ancestor::form]",
            )
            if len(stars) >= 5:
                random_index = random.randint(2, 4)
                selected_star = stars[random_index]
                actions = ActionChains(driver)
                actions.move_to_element(selected_star).pause(1).click().perform()
                # print(f"{unique_name} selected a 4-star rating!")
            else:
                print("Star rating elements not found!")

            # time.sleep(1)

            # Step 4: Fill in the comment textarea with a unique review
            comment_box = driver.find_element(By.ID, "message-2")
            comment_box.clear()
            comment_box.send_keys(current_comment)
            # print(f"{unique_name} commented: {unique_comment}")

            # time.sleep(1)

            # Step 5: Click the "Comment" button
            comment_button = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Comment')]"
            )
            comment_button.click()
            print(f"Comment submitted!")

            time.sleep(1)  # Wait before writing another review

        print(f"Finished 5 reviews for product {index}: {slug}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
