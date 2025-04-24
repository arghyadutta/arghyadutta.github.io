import pandas as pd
import os
import shutil

# === Configuration ===
INPUT_FILE = "assets/e3systems-small.xlsx"
HTML_DIR = "protein_pages"
ASSETS_CSS = "../assets/style.css"

# Create/clean output directory
if os.path.exists(HTML_DIR):
    shutil.rmtree(HTML_DIR)
os.makedirs(HTML_DIR)

# Load data
df = pd.read_excel(INPUT_FILE)

# Filter for E3 proteins
e3_df = df[df["e3_cat"] == True]

# Helper functions
def build_uniprot_link(acc):
    return f"https://www.uniprot.org/uniprotkb/{acc}/entry"

def build_interpro_link(acc):
    return f"https://www.ebi.ac.uk/interpro/protein/UniProt/{acc}"

def make_cytoscape_elements(protein_id, substrate_list):
    protein_node = f"{{ data: {{ id: '{protein_id}', label: '{protein_id}' }} }}"
    substrate_nodes = []
    edges = []

    for substrate in substrate_list:
        sub_id = substrate.strip()
        if not sub_id:
            continue
        substrate_nodes.append(f"{{ data: {{ id: '{sub_id}', label: '{sub_id}' }} }}")
        edges.append(f"{{ data: {{ source: '{protein_id}', target: '{sub_id}' }} }}")

    return (
        protein_node,
        ",\n".join(substrate_nodes),
        ",\n".join(edges),
    )

for _, row in e3_df.iterrows():
    acc = row["upt_acc"]
    name = str(row["upt_id"]).replace("_HUMAN", "")
    length = int(row["length"]) if not pd.isna(row["length"]) else "--"
    confidence = row["db_confidence"] if not pd.isna(row["db_confidence"]) else "N/A"
    substrates = (
        str(row["substrates"]).split(",")
        if "substrates" in row and not pd.isna(row["substrates"])
        else []
    )

    # BUILD cytoscape elements first
    protein_node, substrate_nodes, edges = make_cytoscape_elements(name, substrates)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
    <title>{name}</title>
    <link rel="stylesheet" href="{ASSETS_CSS}">
</head>
<body>
    <h1>{name}</h1>
    <ul>
        <li><strong>UniProt ID for {name}:</strong> <a href="{build_uniprot_link(acc)}" target="_blank">{acc}</a></li>
        <li><strong>Protein length:</strong> {length}</li>
        <li><strong>Database Confidence:</strong> {confidence}</li>
        <li><a href="{build_interpro_link(acc)}" target="_blank">InterPro entry</a></li>
    </ul>
"""

    if substrates:
        html_content += "<h2>Known Substrates</h2><ul>"
        for substrate in substrates:
            html_content += f"<li>{substrate.strip()}</li>\n"
        html_content += "</ul>"

    html_content += f"""
<h2>Protein–Substrate Interaction Network</h2>
<div id="cy" style="width: 100%; height: 400px; border: 1px solid #ccc;"></div>

<script>
    document.addEventListener("DOMContentLoaded", function () {{
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: [
{protein_node},
{substrate_nodes},
{edges}
            ],
            style: [
                {{
                    selector: 'node',
                    style: {{
                        'label': 'data(label)',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'font-size': '12px',
                        'color': '#ffffff',
                        'background-color': '#0074D9',
                        'width': '40px',
                        'height': '40px',
                        'text-outline-width': 2,
                        'text-outline-color': '#0074D9'
                    }}
                }},
                {{
                    selector: 'node[id = "{name}"]',
                    style: {{
                        'background-color': '#FF4136',
                        'width': '50px',
                        'height': '50px',
                        'font-size': '14px',
                        'text-outline-color': '#FF4136'
                    }}
                }},
                {{
                    selector: 'edge',
                    style: {{
                        'width': 2,
                        'line-color': '#888',
                        'target-arrow-color': '#888',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier'
                    }}
                }}
            ],
            layout: {{
                name: 'cose',
                animate: true,
                padding: 20,
                fit: true,
                nodeRepulsion: 8000,
                edgeElasticity: 200,
                gravity: 0.25,
                numIter: 1000
            }}
        }});
    }});
</script>
</body>
</html>
"""

    filename = f"{acc}.html"
    with open(os.path.join(HTML_DIR, filename), "w", encoding="utf-8") as f:
        f.write(html_content)
