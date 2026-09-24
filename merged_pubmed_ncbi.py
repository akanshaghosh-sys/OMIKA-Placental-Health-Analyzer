import os
import pandas as pd

print("Current folder:", os.getcwd())

for filename in ["pubmed_dataset.csv", "geo_dataset.csv"]:
    print("\nChecking:", filename)

    if not os.path.exists(filename):
        print("❌ File not found!")
    else:
        print("File size:", os.path.getsize(filename), "bytes")

        try:
            df = pd.read_csv(filename)
            print("Rows and columns:", df.shape)
            print("Column names:", df.columns.tolist())
            print(df.head(3))

        except pd.errors.EmptyDataError:
            print("❌ This CSV is empty or has no readable columns.")
import pandas as pd
import numpy as np

# -----------------------------------
# STEP 1: Load both datasets
# -----------------------------------

pubmed = pd.read_csv("pubmed_dataset.csv")
geo = pd.read_csv("geo_dataset.csv")

print("PubMed columns:")
print(pubmed.columns.tolist())

print("\nGEO columns:")
print(geo.columns.tolist())


# -----------------------------------
# STEP 2: Clean column names
# -----------------------------------

pubmed.columns = pubmed.columns.str.strip()
geo.columns = geo.columns.str.strip()


# -----------------------------------
# STEP 3: Identify the gene column
# -----------------------------------

# Change these if your CSV uses different names
pubmed_gene_col = "gene_symbol"
geo_gene_col = "gene_symbol"

# Make gene symbols consistent
pubmed[pubmed_gene_col] = (
    pubmed[pubmed_gene_col]
    .astype("string")
    .str.strip()
    .str.upper()
)

geo[geo_gene_col] = (
    geo[geo_gene_col]
    .astype("string")
    .str.strip()
    .str.upper()
)


# -----------------------------------
# STEP 4: Calculate GEO fold change
# -----------------------------------

geo["average_fpkm_con"] = pd.to_numeric(
    geo["average_fpkm_con"], errors="coerce"
)

geo["average_fpkm_p"] = pd.to_numeric(
    geo["average_fpkm_p"], errors="coerce"
)

# Avoid division by zero
geo["fold_change"] = np.where(
    geo["average_fpkm_con"] > 0,
    geo["average_fpkm_p"] / geo["average_fpkm_con"],
    np.nan
)

# Calculate log2 fold change
geo["log2FC"] = np.log2(geo["fold_change"])

# Classify expression changes
geo["expression_status"] = np.select(
    [
        geo["log2FC"] >= 1,
        geo["log2FC"] <= -1
    ],
    [
        "Upregulated",
        "Downregulated"
    ],
    default="No significant fold-change threshold reached"
)


# -----------------------------------
# STEP 5: Keep one GEO row per gene
# -----------------------------------

# Keep the row with the largest absolute log2FC
geo["abs_log2FC"] = geo["log2FC"].abs()

geo_unique = (
    geo.sort_values("abs_log2FC", ascending=False)
       .drop_duplicates(subset=[geo_gene_col])
       .copy()
)


# -----------------------------------
# STEP 6: Merge PubMed and GEO
# -----------------------------------

merged = pd.merge(
    pubmed,
    geo_unique,
    left_on=pubmed_gene_col,
    right_on=geo_gene_col,
    how="left",
    suffixes=("_pubmed", "_geo")
)


# -----------------------------------
# STEP 7: Check matching genes
# -----------------------------------

matched = merged[geo_gene_col].notna()

print("\nTotal PubMed rows:", len(pubmed))
print("Rows with a GEO match:", matched.sum())

print("\nMatched genes:")
print(merged.loc[matched, pubmed_gene_col].unique())


# -----------------------------------
# STEP 8: Save the merged dataset
# -----------------------------------

merged.to_csv("pubmed_ncbi_merged.csv", index=False)

print("\nMerged dataset saved as pubmed_ncbi_merged.csv")