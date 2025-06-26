import json
import pandas as pd

# Paths
json_path = (
    r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\social_links.json"
)
excel_path = r"C:\Users\PcHelps\Documents\Python\youtube_channel_scraper\social_links_formatted.xlsx"

# Load JSON data
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Transform into row format where each social platform is a column
rows = []
for channel_url, links in data.items():
    row = {"YouTube Channel": channel_url}
    for link in links:
        platform = link.get("platform", "").strip()
        url = link.get("url", "")
        if platform:  # Avoid empty platform names
            row[platform] = url
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Optional: Sort columns (YouTube Channel first, rest alphabetically)
cols = ["YouTube Channel"] + sorted(
    [col for col in df.columns if col != "YouTube Channel"]
)
df = df[cols]

# Save to Excel
df.to_excel(excel_path, index=False)

print(f"✅ Excel saved at: {excel_path}")
