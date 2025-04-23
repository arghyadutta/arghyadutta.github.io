import os
import json
from bs4 import BeautifulSoup

# Directory containing the generated protein HTML files
HTML_DIR = "./protein_pages"

# Base URL for local development or prototype testing
BASE_URL = "./protein_pages/"

def extract_text_from_tag(tag):
    if tag.name in ["script", "style"]:
        return ""
    return " ".join(tag.stripped_strings)

def extract_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else os.path.basename(file_path)

        tags = soup.find_all(["p", "h2", "h3", "h4", "h5", "h6", "div", "li", "a"])
        unique_content = set(extract_text_from_tag(tag) for tag in tags)
        content = " ".join(unique_content)

        relative_path = os.path.relpath(file_path, start=os.path.dirname(HTML_DIR))
        url = relative_path.replace("\\", "/")

        return {
            "title": title,
            "url": url,
            "content": content[:100000]
        }

# Collect HTML files and build the index
index_data = []
for filename in os.listdir(HTML_DIR):
    if filename.lower().endswith(".html") and not filename.startswith('.'):
        file_path = os.path.join(HTML_DIR, filename)
        index_data.append(extract_content(file_path))

# Save the index
with open("search-index.json", "w", encoding="utf-8") as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)

print("search-index.json created successfully.")
