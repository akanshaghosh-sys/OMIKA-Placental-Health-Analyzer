import pandas as pd


# ============================================================
# 1. LOAD YOUR EXISTING MERGED GEO + PUBMED DATA
# ============================================================

merged_file = "pubmed_ncbi_merged.csv"

df = pd.read_csv(merged_file)

print("Original merged dataset:")
print(df.head())

print("\nOriginal number of rows:", len(df))


# ============================================================
# 2. LOAD KEGG PATHWAY MAPPING
# ============================================================

pathway_file = "pathway_mapping.csv"

pathway_df = pd.read_csv(pathway_file)

print("\nKEGG pathway mapping:")
print(pathway_df)


# ============================================================
# 3. CLEAN GENE NAMES IN BOTH FILES
# ============================================================

df["gene_symbol"] = (
    df["gene_symbol"]
    .astype(str)
    .str.strip()
    .str.upper()
)

pathway_df["Gene"] = (
    pathway_df["Gene"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ============================================================
# 4. RENAME PATHWAY GENE COLUMN
# ============================================================

pathway_df = pathway_df.rename(
    columns={
        "Gene": "gene_symbol"
    }
)


# ============================================================
# 5. REMOVE DUPLICATE PATHWAY RECORDS
# ============================================================

pathway_df = pathway_df.drop_duplicates(
    subset=[
        "gene_symbol",
        "Pathway_ID"
    ]
)


# ============================================================
# 6. MERGE GEO + PUBMED WITH KEGG PATHWAYS
# ============================================================

final_df = df.merge(
    pathway_df[
        [
            "gene_symbol",
            "KEGG_ID",
            "Pathway_ID",
            "Pathway",
            "Source"
        ]
    ],
    on="gene_symbol",
    how="left"
)


# ============================================================
# 7. SAVE FINAL INTEGRATED DATASET
# ============================================================

output_file = "final_integrated_results.csv"

final_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("FINAL INTEGRATED DATASET CREATED")
print("=" * 70)

print("\nFinal number of rows:", len(final_df))

print("\nFinal columns:")

for column in final_df.columns:
    print(" -", column)


print("\nFinal dataset:")
print(final_df.to_string(index=False))


# ============================================================
# 9. CHECK WHICH GENES GOT PATHWAYS
# ============================================================

print("\n")
print("=" * 70)
print("PATHWAY COVERAGE")
print("=" * 70)

genes_with_pathways = (
    final_df[
        final_df["Pathway"].notna()
    ]["gene_symbol"]
    .unique()
)

genes_without_pathways = (
    final_df[
        final_df["Pathway"].isna()
    ]["gene_symbol"]
    .unique()
)


print("\nGenes with KEGG pathways:")

for gene in genes_with_pathways:
    print(" ✓", gene)


print("\nGenes without KEGG pathway annotation:")

for gene in genes_without_pathways:
    print(" -", gene)


print("\n")
print("Saved as:")
print(output_file)