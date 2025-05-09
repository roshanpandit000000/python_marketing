import json

# Load Pinterest image URLs
with open("pinterest_images.json", "r") as f:
    pinterest_urls = json.load(f)

# Load comment data
with open(
    r"C:\Users\PcHelps\Documents\Bella Hararo MongoDB Database\test.comments.json", "r"
) as f:
    comments_data = json.load(f)

# Replace userProfile with Pinterest URLs
for i, comment in enumerate(comments_data):
    if i < len(pinterest_urls):
        comment["userProfile"] = pinterest_urls[i]
    else:
        break  # Stop if there are more comments than image URLs

# Save updated data
with open("test.comments.json", "w") as f:
    json.dump(comments_data, f, indent=4)

print(
    f"✅ Updated {min(len(comments_data), len(pinterest_urls))} comments with Pinterest image URLs."
)
