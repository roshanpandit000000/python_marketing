import json
import pandas as pd

# File paths
json_path = (
    r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\social_links.json"
)
excel_path = r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\filtered_social_links.xlsx"

# Platforms to include
desired_platforms = {"Facebook page", "Instagram", "Twitter", "whatsapp"}

# Load data
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Format into rows
rows = []
for channel_url, links in data.items():
    row = {"YouTube Channel": channel_url}
    for link in links:
        platform = link.get("platform", "").strip()
        url = link.get("url", "")
        if platform in desired_platforms:
            row[platform] = url
    rows.append(row)

# Create DataFrame with consistent column order
columns = ["YouTube Channel", "Facebook page", "Instagram", "Twitter", "whatsapp"]
df = pd.DataFrame(rows, columns=columns)

# Save to Excel
df.to_excel(excel_path, index=False)

print(f"✅ Excel saved at: {excel_path}")
