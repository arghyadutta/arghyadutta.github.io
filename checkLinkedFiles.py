import os
import re

# Paths
notebooks_folder = "./notebooks"
listing_html_file = "notebooks.html"

# Get all .html files in the notebooks folder
notebook_files = {file for file in os.listdir(notebooks_folder) if file.endswith(".html")}

# Read the listing.html file and extract all linked files
with open(listing_html_file, "r", encoding="utf-8") as f:
    listing_content = f.read()

# Use regex to find all href links pointing to the notebooks folder
linked_files = set(re.findall(r'href\s*=\s*["\']notebooks/([^"\']+\.html)["\']', listing_content))

# Check missing and extra files
missing_files = notebook_files - linked_files
extra_links = linked_files - notebook_files

# Print results
if missing_files:
    print("Missing links (files in notebooks/ but not listed in the HTML):")
    for file in missing_files:
        print(f"- {file}")

if extra_links:
    print("⚠️ Extra links (linked in HTML but file not found in notebooks/):")
    for file in extra_links:
        print(f"- {file}")

if not missing_files and not extra_links:
    print("All files are correctly linked!")
