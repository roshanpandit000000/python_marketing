import json

# Load Pinterest image URLs
with open("pinterest_images.json", "r") as f:
    pinterest_urls = json.load(f)

# Load comment data
with open(
    r"C:\Users\PcHelps\Documents\Bella Hararo MongoDB Database\test.comments.json", "r"
) as f:
    comments_data = json.load(f)

# Track used emails to avoid duplicates
used_emails = set()

# Update each comment
for i, comment in enumerate(comments_data):
    # Set userProfile to Pinterest image URL if available
    if i < len(pinterest_urls):
        comment["userProfile"] = pinterest_urls[i]

    # Clean name to make base email
    name = comment.get("commentname", "user").strip().replace(" ", "").lower()
    base_email = name
    email = f"{base_email}@gmail.com"

    # Make sure email is unique
    count = 1
    while email in used_emails:
        email = f"{base_email}{count}@gmail.com"
        count += 1

    used_emails.add(email)
    comment["userEmail"] = email

# Save updated data
with open("test.comments.json", "w") as f:
    json.dump(comments_data, f, indent=4)

print(f"✅ Updated userProfile and userEmail for {len(comments_data)} comments.")
