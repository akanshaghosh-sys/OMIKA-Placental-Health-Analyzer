
import pandas as pd

# 1. Data transcribed from the Phase II qRT-PCR
# table in the article you provided.
data = [
    {
        "gene_symbol": "ABHD3",
        "group": "Overall",
        "beta": -0.23,
        "standard_error": 0.06,
        "p_value": 0.0003
    },
    {
        "gene_symbol": "ABHD3",
        "group": "Female",
        "beta": -0.17,
        "standard_error": 0.06,
        "p_value": 0.07
    },
    {
        "gene_symbol": "ABHD3",
        "group": "Male",
        "beta": -0.27,
        "standard_error": 0.06,
        "p_value": 0.0009
    },
    {
        "gene_symbol": "ATP11A",
        "group": "Overall",
        "beta": 0.23,
        "standard_error": 0.10,
        "p_value": 0.02
    },
    {
        "gene_symbol": "ATP11A",
        "group": "Female",
        "beta": 0.12,
        "standard_error": 0.14,
        "p_value": 0.38
    },
    {
        "gene_symbol": "ATP11A",
        "group": "Male",
        "beta": 0.31,
        "standard_error": 0.15,
        "p_value": 0.04
    },
    {
        "gene_symbol": "PSCA",
        "group": "Overall",
        "beta": 0.31,
        "standard_error": 0.20,
        "p_value": 0.045
    },
    {
        "gene_symbol": "PSCA",
        "group": "Female",
        "beta": 0.10,
        "standard_error": 0.21,
        "p_value": 0.65
    },
    {
        "gene_symbol": "PSCA",
        "group": "Male",
        "beta": 0.47,
        "standard_error": 0.20,
        "p_value": 0.04
    },
    {
        "gene_symbol": "ST6GALNAC4",
        "group": "Overall",
        "beta": 0.30,
        "standard_error": 0.09,
        "p_value": 0.0009
    },
    {
        "gene_symbol": "ST6GALNAC4",
        "group": "Female",
        "beta": 0.28,
        "standard_error": 0.13,
        "p_value": 0.04
    },
    {
        "gene_symbol": "ST6GALNAC4",
        "group": "Male",
        "beta": 0.33,
        "standard_error": 0.12,
        "p_value": 0.006
    },
    {
        "gene_symbol": "CLTCL1",
        "group": "Overall",
        "beta": 0.03,
        "standard_error": 0.10,
        "p_value": 0.77
    },
    {
        "gene_symbol": "CLTCL1",
        "group": "Female",
        "beta": -0.008,
        "standard_error": 0.10,
        "p_value": 0.94
    },
    {
        "gene_symbol": "CLTCL1",
        "group": "Male",
        "beta": 0.10,
        "standard_error": 0.10,
        "p_value": 0.48
    }
]

# 2. Convert the list into a pandas DataFrame
df = pd.DataFrame(data)

# 3. Add article and study information
df["pollutant"] = "PM2.5"
df["study_id"] = "PMC9177798"
df["evidence_type"] = "Phase II qRT-PCR"
df["tissue"] = "Placenta"

# 4. Flag nominal p-values below 0.05
# This is NOT an FDR-adjusted significance result.
df["p_below_005"] = df["p_value"] < 0.05

# 5. Save the data as a CSV file
df.to_csv("pubmed_pm25_placenta.csv", index=False)

# 6. Display the results
print("Research data saved successfully!")
print(df.head())

print("Total records:", len(df))
print("Unique genes:", df["gene_symbol"].nunique())