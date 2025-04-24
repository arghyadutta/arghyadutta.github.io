import os
import pandas as pd

# Paths
excel_path = "assets/e3systems-small.xlsx"
protein_dir = "protein_pages"
index_path = "index.html"

# Load data
df = pd.read_excel(excel_path)
df = df[df['e3_cat'] == True]  # Filter Catalytic E3s

# Start HTML structure
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>E3 Ligome</title>
    <link rel="stylesheet" href="assets/style.css">
    <script src="search.js" defer></script>
</head>
<body>
    <h1>Human E3 Ligome</h1>

    <input type="text" id="searchBox" onkeyup="searchSite()" placeholder="Search">
    <ul id="searchResults"></ul>

    <hr>
"""

# Group and add links
grouped = df.groupby('class')
for group, subdf in grouped:
    html += f"<h2>{group}</h2>\n<ul>\n"
    for _, row in subdf.iterrows():
        uniprot_id = row['upt_acc']
        name = row['upt_id'].replace("_HUMAN", "")
        filename = f"{uniprot_id}.html"
        filepath = os.path.join(protein_dir, filename)
        if os.path.exists(filepath):  # Only link if file was created
            html += f'<li><a href="{filepath}">{name} ({uniprot_id})</a></li>\n'
    html += "</ul>\n"

html += """
</body>
</html>
"""

# Write index.html
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Main index.html generated.")
