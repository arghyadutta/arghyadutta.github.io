import os
import json
from bs4 import BeautifulSoup

HTML_DIR = "./notebooks"

def extract_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        # Get <h1> as title (fallback to filename if missing)
        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else os.path.basename(file_path)

        # Extract text from <p>, <h2>-<h6>, and <div> tags (ignore script/style)
        paragraphs = soup.find_all(["p", "h2", "h3", "h4", "h5", "h6", "div", "dl", "dt", "dd", "li"])
        content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

        return {"title": title, "url": file_path, "content": content[:100000]}

# Generate search index
index_data = []
for filename in os.listdir(HTML_DIR):
    if filename.endswith(".html"):
        file_path = os.path.join(HTML_DIR, filename)
        index_data.append(extract_content(file_path))

# Save to search-index.json
with open("search-index.json", "w", encoding="utf-8") as json_file:
    json.dump(index_data, json_file, indent=2, ensure_ascii=False)

print("Search index updated with <h1> titles!")
