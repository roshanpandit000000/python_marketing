from bs4 import BeautifulSoup
import pandas as pd

# Load the extracted HTML
with open("h3_data.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract h3 tag data
data = []
for h3 in soup.find_all("h3"):
    profile_link = h3.find("a")["href"] if h3.find("a") else "N/A"
    profile_name = h3.get_text(strip=True)
    data.append(
        {
            "Profile Name": profile_name,
            "Profile Link": f"https://www.instagram.com{profile_link}",
        }
    )

# Create DataFrame and export to Excel
df = pd.DataFrame(data)
df.to_csv("filtered_data.csv", index=False)

print("Data exported successfully to 'filtered_data.csv'")
