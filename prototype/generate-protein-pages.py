import os
import pandas as pd

# Paths
excel_path = "assets/e3systems-small.xlsx"
output_dir = "protein_pages"

# Clean output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    # Remove old HTML files
    for f in os.listdir(output_dir):
        if f.endswith(".html"):
            os.remove(os.path.join(output_dir, f))

# Load data
df = pd.read_excel(excel_path)

# Filter: Only where e3_cat is TRUE
filtered_df = df[df['e3_cat'] == True]

# Iterate and generate HTML
for _, row in filtered_df.iterrows():
    uniprot_id = row['upt_acc']
    name = row['upt_id'].replace("_HUMAN", "")
    length = row['length']
    confidence = row['db_confidence']
    group = str(row['class'])

    filename = f"{group}_{uniprot_id}.html"
    filepath = os.path.join(output_dir, filename)

    uniprot_url = f"https://www.uniprot.org/uniprotkb/{uniprot_id}"
    interpro_url = f"https://www.ebi.ac.uk/interpro/protein/UniProt/{uniprot_id}"

    # HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{name}</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h1>{name}</h1>
    <ul>
        <li><strong>UniProt ID for {name}:</strong> <a href="{uniprot_url}" target="_blank">{uniprot_id}</a></li>
        <li><strong>Protein length:</strong> {length}</li>
        <li><strong>Database Confidence:</strong> {confidence}</li>
        <li><a href="{interpro_url}" target="_blank">InterPro entry</a></li>
    </ul>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

print("Individual Protein pages generated successfully.")
