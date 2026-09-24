import pandas as pd
import requests
import time


# ============================================================
# 1. LOAD YOUR MERGED GEO + PUBMED DATA
# ============================================================

input_file = "pubmed_ncbi_merged.csv"

df = pd.read_csv(input_file)

# Get unique gene symbols
genes = (
    df["gene_symbol"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .unique()
)

print("Number of unique genes:", len(genes))


# ============================================================
# 2. FIND KEGG HUMAN GENE ID
# ============================================================

def find_kegg_gene(gene):

    url = f"https://rest.kegg.jp/find/hsa/{gene}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    text = response.text.strip()

    if not text:
        return None

    for line in text.split("\n"):

        parts = line.split("\t")

        if len(parts) < 2:
            continue

        kegg_id = parts[0]
        description = parts[1]

        # Only human KEGG genes
        if not kegg_id.startswith("hsa:"):
            continue

        # Check whether our gene symbol appears
        if gene in description.upper():

            return kegg_id

    return None


# ============================================================
# 3. GET PATHWAYS FOR KEGG GENE
# ============================================================

def get_pathways(kegg_id):

    url = f"https://rest.kegg.jp/link/pathway/{kegg_id}"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    text = response.text.strip()

    if not text:
        return []

    pathways = []

    for line in text.split("\n"):

        parts = line.split("\t")

        if len(parts) >= 2:

            pathway_id = parts[1]

            if pathway_id not in pathways:

                pathways.append(pathway_id)

    return pathways


# ============================================================
# 4. GET PATHWAY NAME
# ============================================================

def get_pathway_name(pathway_id):

    # KEGG gives IDs like:
    #
    # path:hsa00512
    #
    # Remove "path:"
    clean_id = pathway_id.replace("path:", "")

    # IMPORTANT:
    # Use GET, NOT LIST
    url = f"https://rest.kegg.jp/get/{clean_id}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    text = response.text.strip()

    if not text:
        return None

    # Look for the NAME field in KEGG's flat-file entry
    for line in text.split("\n"):

        if line.startswith("NAME"):

            # Remove "NAME"
            name = line[12:].strip()

            # Remove organism suffix if present
            name = name.replace(
                " - Homo sapiens (human)",
                ""
            )

            return name

    return None


# ============================================================
# 5. PROCESS ALL UNIQUE GENES
# ============================================================

results = []

for i, gene in enumerate(genes, start=1):

    print()
    print(f"Processing {i}/{len(genes)}: {gene}")


    # --------------------------------------------------------
    # Find KEGG gene ID
    # --------------------------------------------------------

    kegg_id = find_kegg_gene(gene)

    if kegg_id is None:

        print("  ❌ KEGG gene ID not found")

        results.append({
            "Gene": gene,
            "KEGG_ID": None,
            "Pathway_ID": None,
            "Pathway": None,
            "Source": "KEGG - gene not found"
        })

        continue


    print(f"  ✓ KEGG ID: {kegg_id}")


    # --------------------------------------------------------
    # Find pathways
    # --------------------------------------------------------

    pathways = get_pathways(kegg_id)

    if not pathways:

        print("  ⚠ No KEGG pathway found")

        results.append({
            "Gene": gene,
            "KEGG_ID": kegg_id,
            "Pathway_ID": None,
            "Pathway": None,
            "Source": "KEGG - no pathway"
        })

        continue


    print(f"  ✓ {len(pathways)} pathway(s) found")


    # --------------------------------------------------------
    # Get pathway names
    # --------------------------------------------------------

    for pathway_id in pathways:

        pathway_name = get_pathway_name(pathway_id)

        print(
            f"     {pathway_id} → {pathway_name}"
        )

        results.append({
            "Gene": gene,
            "KEGG_ID": kegg_id,
            "Pathway_ID": pathway_id,
            "Pathway": pathway_name,
            "Source": "KEGG"
        })

        # Avoid excessive API requests
        time.sleep(0.4)


    time.sleep(0.4)


# ============================================================
# 6. CREATE DATAFRAME
# ============================================================

pathway_df = pd.DataFrame(results)


# ============================================================
# 7. SAVE CSV
# ============================================================

output_file = "pathway_mapping.csv"

pathway_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print()
print("=" * 70)
print("PATHWAY MAPPING COMPLETED")
print("=" * 70)

print()

print(pathway_df.to_string(index=False))

print()

print("Saved as:")
print(output_file)