from difflib import SequenceMatcher

title_text = "python is awesome"
alt_samples = [
    "python is great",
    "awesome python coding",
    "learn java easily",
    "python awesome tricks",
    "this is about python",
    "a black cat saying python is everything",
    "how to code in rust",
]


for alt in alt_samples:
    ratio = SequenceMatcher(None, title_text.lower(), alt.lower()).ratio()
    print(f"ALT: {alt}\nSimilarity: {ratio:.2f} {'✅' if ratio >= 0.5 else '❌'}\n")
