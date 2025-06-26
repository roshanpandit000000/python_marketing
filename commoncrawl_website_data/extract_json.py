import gzip

path = r"C:\Users\PcHelps\Documents\Python\commoncrawl_website_data\downloads\cdx-00000.gz"

with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
    for i in range(20):
        print(f"LINE {i+1}:", f.readline().strip())
