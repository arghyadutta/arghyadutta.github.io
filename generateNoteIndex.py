import os
import glob
from datetime import datetime
from bs4 import BeautifulSoup

def get_files_sorted_by_mtime(directory, extension=".html"):
    files = glob.glob(os.path.join(directory, f"*{extension}"))
    files = [f for f in files if os.path.basename(f) != "template.html"]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files


def extract_title_from_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            title = soup.find("h1")
            return title.text.strip() if title else os.path.basename(file_path)
    except Exception as e:
        return os.path.basename(file_path)


def generate_index_html(files, output_file="notebooks.html"):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notebooks</title>
    <meta name="description" content="Digital garden, tended by Arghya">
    <link rel="apple-touch-icon" sizes="180x180" href="../assets/favicon_io/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon_io/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../assets/favicon_io/favicon-16x16.png">
    <link rel="manifest" href="../assets/favicon_io/site.webmanifest">
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<em><a href="../index.html">Homepage</a></em>
    <h1>Notebooks</h1>
<blockquote>
    "I sometimes find, and I am sure you know the feeling, that I simply have too many thoughts and memories crammed into my mind. At these times, I use the Pensieve. One simply siphons the excess thoughts from one’s mind, pours them into the basin, and examines them at one’s leisure. It becomes easier to spot patterns and links, you understand, when they are in this form."—Albus Dumbledore (Harry Potter and the Goblet of Fire)
</blockquote>
<p>
    A collection of resources and notes maintained by Arghya. The depth of content varies; some are just placeholders. The aim is to maintain a public, annotated bibliography of things I've explored, or plan to explore. The idea came from Cosma Shalizi's extensive <a href="http://bactra.org/notebooks/">notebooks</a>.
</p>

<p>
    If you've suggestions, please send me an email: arghya.d@srmap.edu.in
</p>
    <dl>
"""
    for file in files:
        mtime = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%B %d, %Y")
        filename = os.path.basename(file)
        title = extract_title_from_html(file)
        html_content += (
            f'<dt><a href="notebooks/{filename}">{title}</a> ({mtime})</dt>\n'
        )

    html_content += """
    </dl>

    <hr>

<p>
    Basic search function, with coding almost entirely done using LLMs. It looks bad, but seems to work.
</p>

<input type="text" id="searchBox" onkeyup="searchSite()" placeholder="Search">
<ul id="searchResults"></ul>

<script src="search.js"></script>

<hr>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    directory = "notebooks"
    output_file = "notebooks.html"  # Place index file in the outer folder
    files = get_files_sorted_by_mtime(directory)
    generate_index_html(files, output_file)
    print(f"Index file generated: {output_file}")


if __name__ == "__main__":
    main()
