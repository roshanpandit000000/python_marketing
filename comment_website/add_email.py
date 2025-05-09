import json

# Load comment data
with open(
    r"C:\Users\PcHelps\Documents\Bella Hararo MongoDB Database\test.comments.json", "r"
) as f:
    comments_data = json.load(f)

# Only update userEmail
for comment in comments_data:
    commentname = comment.get("commentname", "user")
    cleaned_name = commentname.strip().replace(" ", "").lower()
    comment["userEmail"] = f"{cleaned_name}@gmail.com"

# Save back to the same file (overwrites safely)
with open("test.comments.json", "w") as f:
    json.dump(comments_data, f, indent=4)

print(f"✅ Updated userEmail for {len(comments_data)} comments.")
