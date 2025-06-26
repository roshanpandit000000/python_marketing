import gzip
import os
import requests
from tqdm import tqdm
import json


# STEP 1: Extract .paths.gz file
def extract_gz_file(gz_path, out_path):
    with gzip.open(gz_path, "rb") as f_in:
        with open(out_path, "wb") as f_out:
            f_out.write(f_in.read())
    print(f"Extracted to: {out_path}")


# STEP 2: Read .paths file and form URLs
def generate_download_urls(paths_file, limit=2):
    urls = []
    with open(paths_file, "r") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            line = line.strip()
            full_url = "https://data.commoncrawl.org/" + line
            urls.append(full_url)
    return urls


# STEP 3: Download index files
def download_file(
    url,
    output_dir=r"C:\Users\PcHelps\Documents\Python\commoncrawl_website_data\downloads",
):
    os.makedirs(output_dir, exist_ok=True)
    local_filename = os.path.join(output_dir, url.split("/")[-1])
    if os.path.exists(local_filename):
        print(f"Already downloaded: {local_filename}")
        return local_filename

    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    total = int(response.headers.get("content-length", 0))
    with open(local_filename, "wb") as file, tqdm(
        desc=local_filename, total=total, unit="B", unit_scale=True
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    return local_filename


# STEP 4: Read .gz JSON lines and extract URLs/domains
def parse_index_file(gz_file, max_lines=100):
    with gzip.open(gz_file, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            try:
                data = json.loads(line)
                print(data.get("url"))
                # print("Domain:", data.get("url").split("/")[2])
            except Exception as e:
                continue


# RUN SCRIPT
if __name__ == "__main__":
    gz_path = r"C:\Users\PcHelps\Downloads\cc-index.paths.gz"
    extracted_path = "cc-index-table.paths"

    # Step 1: Extract paths
    extract_gz_file(gz_path, extracted_path)

    # Step 2: Get some index URLs (change limit=5 or more if needed)
    urls = generate_download_urls(extracted_path, limit=2)

    # Step 3: Download index files and parse them
    for url in urls:
        downloaded_file = download_file(url)
        print(f"\n--- Parsed URLs from: {downloaded_file} ---")
        parse_index_file(downloaded_file, max_lines=50)
