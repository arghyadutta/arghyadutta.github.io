import os
import json
from bs4 import BeautifulSoup

HTML_DIR = "./notebooks"

def extract_text_from_tag(tag):
    if tag.name in ["script", "style"]:
        return ""
    return " ".join(tag.stripped_strings)

def extract_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        # Get <h1> as title (fallback to filename if missing)
        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else os.path.basename(file_path)

        # Extract text from <p>, <h2>-<h6>, and <div> tags (ignore script/style)
        tags = soup.find_all(["p", "h2", "h3", "h4", "h5", "h6", "div", "dt", "dd", "li"])
        
        # Use a set to deduplicate content
        unique_content = set(extract_text_from_tag(tag) for tag in tags)
        
        # Join the unique content into a single string
        content = " ".join(unique_content)

        # Debug: Print the content to check for duplicates
        print(f"Extracted content from {file_path}:\n{content}\n")

        return {"title": title, "url": file_path, "content": content[:100000]}

# Generate search index
index_data = []
unique_files = set(os.listdir(HTML_DIR))

for filename in unique_files:
    if filename.lower().endswith(".html") and not filename.startswith('.'):
        file_path = os.path.abspath(os.path.join(HTML_DIR, filename))
        index_data.append(extract_content(file_path))

# Save to search-index.json
with open("search-index.json", "w", encoding="utf-8") as json_file:
    json.dump(index_data, json_file, indent=2, ensure_ascii=False)

print("Search index updated with <h1> titles!")