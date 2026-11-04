import os
import glob
import re
from html import escape
from datetime import datetime
from bs4 import BeautifulSoup

CATEGORIES = {
    "Physics": [
        "qMech",
        "qMechMath",
        "dynamics",
        "ehrenfest",
        "bec",
        "electromagnetism",
        "relativity",
        "enggPhysics",
        "physicsFreeBooks",
        "physicsExperiments",
        "dimensionalAnalysis",
        "timesArrow",
        "loschmidtParadox",
        "statMechReadingMaterial",
        "statMechCourse",
        "phaseDiagram",
        "nld",
        "complexity",
        "saw",
        "mathematicalMethods",
        "biophysics",
    ],
    "Mathematics": [
        "linearAlgebra",
        "combinatorics",
        "statistics",
        "statPython",
        "bayesian",
        "simpsonsParadox",
    ],
    "Machine Learning and AI": [
        "machinelearning",
        "ai",
        "deepLearning",
        "learnability",
        "clustPerformance",
        "geneticAlgorithm",
        "symbolicRegression",
        "subgroupDiscovery",
    ],
    "Other Sciences": [
        "biology",
        "hydrophobicity",
        "chemistry",
    ],
    "Programming": [
        "python",
        "rProgramming",
        "hpc",
        "softwareTools",
        "openSource",
        "visualization",
        "excelShortcuts",
    ],
    "Writing and Knowledge Management": [
        "latex",
        "plainText",
        "pkm",
        "writing",
        "stationery",
        "wellWrittenPapers",
        "dictionary",
    ],
    "Academia, Teaching, and Learning": [
        "teaching",
        "teaching-ai",
        "learning",
        "academicAdvice",
        "academiaIssues",
        "academiaFeatures",
        "biography",
    ],
    "Philosophy and Religion": [
        "philosophyResources",
        "philosophyOfScience",
        "stoicism",
        "religions",
        "logic",
        "advaitaVedanta",
        "silence",
        "melancholia",
        "stupidity"
    ],
    "Language and Literature": [
        "fiction",
        "poetry",
        "leguin",
        "cSLewis",
        "german",
        "sanskrit",
        "bookNLibrary",
        "blogs",
    ],
    "Arts and Culture": [
        "art",
        "music",
        "indian-classical-music",
        "western-classical-music",
        "history",
        "society",
        "foodNDrink",
        "funny"
    ],
}
UNCATEGORIZED = "Uncategorized"

# Reverse lookup: file stem -> category
STEM_TO_CATEGORY = {
    stem: category for category, stems in CATEGORIES.items() for stem in stems
}


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
    except Exception:
        return os.path.basename(file_path)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def group_files_by_category(files):
    """Return {category: [files]} keeping the incoming (mtime-desc) order."""
    grouped = {category: [] for category in CATEGORIES}
    grouped[UNCATEGORIZED] = []

    for file in files:
        stem = os.path.splitext(os.path.basename(file))[0]
        grouped[STEM_TO_CATEGORY.get(stem, UNCATEGORIZED)].append(file)

    # Warn about stale names in CATEGORIES (typos or deleted files)
    existing = {os.path.splitext(os.path.basename(f))[0] for f in files}
    for stem, category in STEM_TO_CATEGORY.items():
        if stem not in existing:
            print(f"Warning: '{stem}' is listed under '{category}' but has no file.")

    if grouped[UNCATEGORIZED]:
        names = ", ".join(os.path.basename(f) for f in grouped[UNCATEGORIZED])
        print(f"Note: uncategorized files -> {names}")

    return grouped


def generate_index_html(files, output_file="notebooks.html"):
    grouped = group_files_by_category(files)
    visible = [(cat, fs) for cat, fs in grouped.items() if fs]

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
    A collection of notes and annotated bibliographies, inspired by <a href="http://bactra.org/notebooks/">Cosma Shalizi's notebooks</a>. Some entries are detailed, others just placeholders. The aim is to keep track of ideas I’ve explored or hope to explore and online resources that I've found useful. As these notes are mostly for my own use, they contain gaps (and a few mistakes). If you spot one, please let me know: arghya.d@srmap.edu.in
</p>

<input type="text" id="searchBox" onkeyup="searchSite()" placeholder="Search">
<ul id="searchResults"></ul>

<script src="search.js"></script>

"""

    # Table of contents linking to each category
    html_content += "    <nav>\n    <p>\n"
    html_content += " &middot;\n".join(
        f'        <a href="#{slugify(cat)}">{escape(cat)}</a> ({len(fs)})'
        for cat, fs in visible
    )
    html_content += "\n    </p>\n    </nav>\n\n"

    # One section per category
    for category, category_files in visible:
        html_content += f'    <h2 id="{slugify(category)}">{escape(category)}</h2>\n'
        html_content += "    <dl>\n"
        for file in category_files:
            mtime = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%B %d, %Y")
            filename = os.path.basename(file)
            title = escape(extract_title_from_html(file))
            html_content += (
                f'    <dt><a href="notebooks/{filename}">{title}</a> ({mtime})</dt>\n'
            )
        html_content += "    </dl>\n\n"

    html_content += """</body>
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
