import pandas as pd


# ============================================================
# 1. LOAD FINAL INTEGRATED DATA
# ============================================================

input_file = "final_integrated_results.csv"

df = pd.read_csv(input_file)

print("=" * 70)
print("LOADED FINAL INTEGRATED DATA")
print("=" * 70)

print("Rows:", len(df))
print("Columns:", list(df.columns))


# ============================================================
# 2. CLEAN BASIC COLUMNS
# ============================================================

df["gene_symbol"] = (
    df["gene_symbol"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df["pollutant"] = (
    df["pollutant"]
    .astype(str)
    .str.strip()
)

df["Pathway"] = df["Pathway"].fillna("No KEGG pathway annotation")


# ============================================================
# 3. USE THE "OVERALL" GROUP FOR GENE-LEVEL DASHBOARD DATA
# ============================================================
#
# Your dataset contains Overall, Female and Male rows.
# For the main dashboard we use the Overall result so that
# one gene is not counted three times.
#

overall_df = df[
    df["group"].astype(str).str.strip().str.lower() == "overall"
].copy()

print("\nOverall gene records:", len(overall_df))


# ============================================================
# 4. ASSOCIATED GENES TABLE
# ============================================================

genes_df = overall_df[
    [
        "pollutant",
        "gene_symbol",
        "log2FC",
        "p_value",
        "expression_status",
        "study_id",
        "evidence_type"
    ]
].copy()


# Direction of expression change
def get_direction(value):

    if value > 0:
        return "Upregulated"

    elif value < 0:
        return "Downregulated"

    else:
        return "No change"


genes_df["Direction"] = genes_df["log2FC"].apply(get_direction)


# Save
genes_df.to_csv(
    "dashboard_genes.csv",
    index=False
)


# ============================================================
# 5. KEY PATHWAYS TABLE
# ============================================================

pathways_df = overall_df[
    overall_df["Pathway"] != "No KEGG pathway annotation"
][
    [
        "pollutant",
        "gene_symbol",
        "KEGG_ID",
        "Pathway_ID",
        "Pathway"
    ]
].drop_duplicates()


pathways_df.to_csv(
    "dashboard_pathways.csv",
    index=False
)


# ============================================================
# 6. BIOMARKER EVIDENCE SCORING
# ============================================================
#
# Prototype evidence score:
#
# 1 point = p-value < 0.05
# 1 point = |log2FC| >= 1
# 1 point = KEGG pathway available
#
# Maximum = 3
#
# This is a PROJECT EVIDENCE SCORE.
# It is NOT a clinical biomarker validation score.
#

overall_df["Statistical_Evidence"] = (
    overall_df["p_value"] < 0.05
).astype(int)


overall_df["Fold_Change_Evidence"] = (
    overall_df["log2FC"].abs() >= 1
).astype(int)


overall_df["Pathway_Evidence"] = (
    overall_df["Pathway"] != "No KEGG pathway annotation"
).astype(int)


overall_df["Biomarker_Score"] = (
    overall_df["Statistical_Evidence"]
    +
    overall_df["Fold_Change_Evidence"]
    +
    overall_df["Pathway_Evidence"]
)


# ============================================================
# 7. EVIDENCE CLASSIFICATION
# ============================================================

def classify_evidence(score):

    if score == 3:
        return "Strong evidence"

    elif score == 2:
        return "Moderate evidence"

    elif score == 1:
        return "Limited evidence"

    else:
        return "Insufficient evidence"


overall_df["Evidence"] = (
    overall_df["Biomarker_Score"]
    .apply(classify_evidence)
)


# ============================================================
# 8. BIOMARKER STATUS
# ============================================================
#
# We classify score >= 2 as a "potential candidate biomarker"
# for the prototype.
#
# This does NOT mean clinically validated biomarker.
#

overall_df["Biomarker"] = overall_df.apply(
    lambda row:
        row["gene_symbol"]
        if row["Biomarker_Score"] >= 2
        else "Not classified",
    axis=1
)


# ============================================================
# 9. BIOMARKER TABLE
# ============================================================

biomarkers_df = overall_df[
    [
        "pollutant",
        "gene_symbol",
        "Biomarker",
        "Biomarker_Score",
        "Evidence",
        "log2FC",
        "p_value",
        "Pathway"
    ]
].copy()


biomarkers_df.to_csv(
    "dashboard_biomarkers.csv",
    index=False
)


# ============================================================
# 10. EVIDENCE SUMMARY
# ============================================================

evidence_df = (
    overall_df
    .groupby(
        ["pollutant", "Evidence"]
    )
    .size()
    .reset_index(
        name="Gene_Count"
    )
)


evidence_df.to_csv(
    "dashboard_evidence.csv",
    index=False
)


# ============================================================
# 11. OVERALL IMPACT SCORE
# ============================================================
#
# Prototype score based on average evidence score.
#
# This is NOT a clinical risk score.
#

if len(overall_df) > 0:

    average_score = (
        overall_df["Biomarker_Score"].mean()
    )

    impact_score = round(
        (average_score / 3) * 100
    )

else:

    impact_score = 0


print("\n")
print("=" * 70)
print("PROTOTYPE IMPACT SCORE")
print("=" * 70)

print(
    "Average evidence score:",
    round(overall_df["Biomarker_Score"].mean(), 2)
)

print(
    "Overall impact score:",
    impact_score,
    "/ 100"
)


# ============================================================
# 12. DISPLAY RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("ASSOCIATED GENES")
print("=" * 70)

print(
    genes_df[
        [
            "pollutant",
            "gene_symbol",
            "log2FC",
            "p_value",
            "Direction"
        ]
    ].to_string(index=False)
)


print("\n")
print("=" * 70)
print("KEY PATHWAYS")
print("=" * 70)

print(
    pathways_df.to_string(index=False)
)


print("\n")
print("=" * 70)
print("BIOMARKER TABLE")
print("=" * 70)

print(
    biomarkers_df.to_string(index=False)
)


print("\n")
print("=" * 70)
print("EVIDENCE SUMMARY")
print("=" * 70)

print(
    evidence_df.to_string(index=False)
)


print("\n")
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print("1. dashboard_genes.csv")
print("2. dashboard_pathways.csv")
print("3. dashboard_biomarkers.csv")
print("4. dashboard_evidence.csv")