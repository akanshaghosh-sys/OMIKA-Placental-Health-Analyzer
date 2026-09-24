import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OMIKA | Placental Health Analyzer",
    page_icon="omika_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLOURS
# ============================================================

BG = "#DFF1F0"
SIDEBAR = "#619EA0"
CARD = "#F9FCFC"
TEXT = "#17383D"
MUTED = "#648083"
TEAL = "#39797C"
TEAL_DARK = "#285F63"
BORDER = "#A8CDCD"
LIGHT_TEAL = "#EDF8F7"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {BG};
    }}

    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR};
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {{
        color: white;
    }}

    /* Selectbox */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {{
        background-color: white;
        border-radius: 10px;
    }}

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: white;
        border-radius: 10px;
        color: {TEXT};
    }}

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
        color: {TEXT} !important;
    }}

    /* SUMMARY CARDS */
    .omika-summary-card {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 17px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(40,95,99,0.06);
        box-sizing: border-box;
    }}

    .omika-summary-label {{
        color: {MUTED};
        font-weight: 600;
        font-size: 14px;
        line-height: 1.25;
        margin-bottom: 12px;
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
    }}

    .omika-summary-value {{
        color: {TEAL_DARK};
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
    }}

    /* BUTTONS */
    .stButton > button {{
        width: 100%;
        background-color: {CARD};
        color: {TEAL_DARK};
        border: 1px solid {BORDER};
        border-radius: 11px;
        font-weight: 600;
        padding: 0.65rem;
    }}

    .stButton > button:hover {{
        background-color: {LIGHT_TEAL};
        border-color: {TEAL};
        color: {TEAL_DARK};
    }}

    /* DATAFRAME */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "active_section" not in st.session_state:
    st.session_state.active_section = "overview"


# ============================================================
# FILE LOADER
# ============================================================

def load_csv(filename):

    if os.path.exists(filename):

        try:
            return pd.read_csv(filename)

        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


# ============================================================
# LOAD YOUR EXISTING FILES
# ============================================================

genes_df = load_csv("dashboard_genes.csv")
pathways_df = load_csv("dashboard_pathways.csv")
biomarkers_df = load_csv("dashboard_biomarkers.csv")
evidence_df = load_csv("dashboard_evidence.csv")
outcomes_df = load_csv("placental_outcomes_mapping.csv")


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_columns(df):

    if df.empty:
        return df

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "pollutant" in df.columns:

        df["pollutant"] = (
            df["pollutant"]
            .astype(str)
            .str.strip()
        )

    return df


genes_df = clean_columns(genes_df)
pathways_df = clean_columns(pathways_df)
biomarkers_df = clean_columns(biomarkers_df)
evidence_df = clean_columns(evidence_df)
outcomes_df = clean_columns(outcomes_df)


# ============================================================
# NORMALISE COMMON COLUMN NAMES
# ============================================================

def normalise(df):

    if df.empty:
        return df

    rename = {}

    for col in df.columns:

        x = col.lower().strip()

        if x in ["gene", "genes", "gene_symbol"]:
            rename[col] = "gene_symbol"

        elif x in ["logfc", "log_2_fc", "log2fc"]:
            rename[col] = "log2FC"

        elif x in ["pvalue", "p_value", "p-val", "pval"]:
            rename[col] = "p_value"

        elif x in ["pathway", "pathway_name"]:
            rename[col] = "Pathway"

        elif x in ["biomarker", "biomarkers"]:
            rename[col] = "Biomarker"

        elif x in ["evidence", "evidence_level"]:
            rename[col] = "Evidence"

    return df.rename(columns=rename)


genes_df = normalise(genes_df)
pathways_df = normalise(pathways_df)
biomarkers_df = normalise(biomarkers_df)
evidence_df = normalise(evidence_df)
outcomes_df = normalise(outcomes_df)


# ============================================================
# BUILT-IN DEMO DATA
#
# This is deliberately inside app.py.
# Therefore no separate demo CSV is required.
# ============================================================

demo_records = [

    # ---------------- ARSENIC ----------------

    ["Arsenic", "AQP9", 1.42, 0.003,
     "Upregulated", "Literature-grounded demo",
     "Transport and metabolism",
     "AQP9", "Moderate evidence"],

    ["Arsenic", "ENPP2", 1.18, 0.008,
     "Upregulated", "Literature-grounded demo",
     "Lipid signaling",
     "ENPP2", "Moderate evidence"],

    ["Arsenic", "AS3MT", 1.65, 0.002,
     "Upregulated", "Literature-grounded demo",
     "Arsenic metabolism",
     "AS3MT", "Strong evidence"],

    ["Arsenic", "SLC39A2", 0.96, 0.021,
     "Upregulated", "Literature-grounded demo",
     "Metal ion transport",
     "SLC39A2", "Limited evidence"],

    ["Arsenic", "GSTM1", -1.11, 0.015,
     "Downregulated", "Literature-grounded demo",
     "Oxidative stress",
     "GSTM1", "Limited evidence"],


    # ---------------- LEAD ----------------

    ["Pb", "MT1A", 1.31, 0.012,
     "Upregulated", "Synthetic demo data",
     "Metal response",
     "MT1A", "Moderate evidence"],

    ["Pb", "MT2A", 1.17, 0.018,
     "Upregulated", "Synthetic demo data",
     "Metal response",
     "MT2A", "Moderate evidence"],

    ["Pb", "HMOX1", 1.44, 0.009,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "HMOX1", "Moderate evidence"],

    ["Pb", "SOD1", 0.82, 0.031,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "SOD1", "Limited evidence"],

    ["Pb", "IL6", 1.08, 0.022,
     "Upregulated", "Synthetic demo data",
     "Inflammatory signaling",
     "IL6", "Limited evidence"],


    # ---------------- CADMIUM ----------------

    ["Cd", "MT1A", 1.52, 0.004,
     "Upregulated", "Synthetic demo data",
     "Metal response",
     "MT1A", "Moderate evidence"],

    ["Cd", "MT2A", 1.38, 0.006,
     "Upregulated", "Synthetic demo data",
     "Metal response",
     "MT2A", "Moderate evidence"],

    ["Cd", "HMOX1", 1.21, 0.013,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "HMOX1", "Moderate evidence"],

    ["Cd", "GSTM1", -0.94, 0.026,
     "Downregulated", "Synthetic demo data",
     "Detoxification",
     "GSTM1", "Limited evidence"],


    # ---------------- NO2 ----------------

    ["NO2", "CYP1A1", 1.26, 0.011,
     "Upregulated", "Synthetic demo data",
     "Xenobiotic metabolism",
     "CYP1A1", "Moderate evidence"],

    ["NO2", "HMOX1", 1.13, 0.019,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "HMOX1", "Moderate evidence"],

    ["NO2", "IL6", 0.91, 0.029,
     "Upregulated", "Synthetic demo data",
     "Inflammatory signaling",
     "IL6", "Limited evidence"],

    ["NO2", "NQO1", 1.34, 0.007,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "NQO1", "Moderate evidence"],


    # ---------------- SO2 ----------------

    ["SO2", "HMOX1", 1.08, 0.016,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "HMOX1", "Moderate evidence"],

    ["SO2", "IL6", 1.22, 0.014,
     "Upregulated", "Synthetic demo data",
     "Inflammatory signaling",
     "IL6", "Moderate evidence"],

    ["SO2", "SOD1", 0.77, 0.035,
     "Upregulated", "Synthetic demo data",
     "Oxidative stress",
     "SOD1", "Limited evidence"],

    ["SO2", "GSTM1", -0.88, 0.027,
     "Downregulated", "Synthetic demo data",
     "Detoxification",
     "GSTM1", "Limited evidence"],
]


demo_df = pd.DataFrame(
    demo_records,
    columns=[
        "pollutant",
        "gene_symbol",
        "log2FC",
        "p_value",
        "Direction",
        "evidence_type",
        "Pathway",
        "Biomarker",
        "Evidence"
    ]
)


# ============================================================
# MASTER POLLUTANTS
# ============================================================

POLLUTANTS = [
    "PM2.5",
    "Arsenic",
    "Pb",
    "Cd",
    "NO2",
    "SO2"
]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Logo
    if os.path.exists("omika_logo.png"):

        st.image(
            "omika_logo.png",
            width=135
        )

    # Branding
    st.title("OMIKA")

    st.caption(
        "The Placenta Knows. We Decode."
    )

    st.markdown(
        "### Placental Health Analyzer"
    )

    st.markdown(
        "#### Select Pollutant"
    )

    selected_pollutant = st.selectbox(
        "Select pollutant",
        POLLUTANTS,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption(
        "Explore pollutant-associated molecular "
        "evidence, candidate biomarkers, pathways "
        "and placental outcomes."
    )


# ============================================================
# FILTER REAL DATA
# ============================================================

def filter_pollutant(df, pollutant):

    if df.empty:
        return pd.DataFrame()

    if "pollutant" not in df.columns:
        return pd.DataFrame()

    return df[
        df["pollutant"]
        .astype(str)
        .str.strip()
        == pollutant
    ].copy()


real_genes = filter_pollutant(
    genes_df,
    selected_pollutant
)

real_pathways = filter_pollutant(
    pathways_df,
    selected_pollutant
)

real_biomarkers = filter_pollutant(
    biomarkers_df,
    selected_pollutant
)

real_evidence = filter_pollutant(
    evidence_df,
    selected_pollutant
)


# ============================================================
# DEMO DATA FOR SELECTED POLLUTANT
# ============================================================

demo_selected = demo_df[
    demo_df["pollutant"] == selected_pollutant
].copy()


# ============================================================
# BUILD DISPLAY DATA
# ============================================================

if selected_pollutant == "PM2.5":

    # Use your actual PM2.5 data
    selected_genes = real_genes.copy()
    selected_pathways = real_pathways.copy()
    selected_biomarkers = real_biomarkers.copy()
    selected_evidence = real_evidence.copy()

else:

    # Use built-in demo data
    selected_genes = demo_selected.copy()

    selected_pathways = demo_selected[
        [
            "pollutant",
            "gene_symbol",
            "Pathway",
            "Evidence"
        ]
    ].copy()

    selected_biomarkers = demo_selected[
        [
            "pollutant",
            "gene_symbol",
            "Biomarker",
            "Evidence"
        ]
    ].copy()

    selected_evidence = demo_selected[
        [
            "pollutant",
            "gene_symbol",
            "Biomarker",
            "Pathway",
            "Evidence",
            "evidence_type"
        ]
    ].copy()


# ============================================================
# REMOVE DUPLICATES
# ============================================================

if not selected_genes.empty and "gene_symbol" in selected_genes.columns:

    selected_genes = selected_genes.drop_duplicates(
        subset=["gene_symbol"]
    )


if not selected_pathways.empty and "Pathway" in selected_pathways.columns:

    selected_pathways = selected_pathways.drop_duplicates(
        subset=["Pathway"]
    )


if not selected_biomarkers.empty and "Biomarker" in selected_biomarkers.columns:

    selected_biomarkers = selected_biomarkers.drop_duplicates(
        subset=["Biomarker"]
    )


# ============================================================
# SUMMARY
# ============================================================

if not selected_genes.empty:

    gene_count = selected_genes[
        "gene_symbol"
    ].nunique()

else:

    gene_count = 0


if not selected_biomarkers.empty:

    biomarker_count = selected_biomarkers[
        "Biomarker"
    ].nunique()

else:

    biomarker_count = 0


if not selected_pathways.empty:

    pathway_count = selected_pathways[
        "Pathway"
    ].nunique()

else:

    pathway_count = 0


# ============================================================
# EVIDENCE LEVEL
# ============================================================

if not selected_evidence.empty and "Evidence" in selected_evidence.columns:

    evidence_text = (
        selected_evidence["Evidence"]
        .astype(str)
        .str.lower()
    )

    if evidence_text.str.contains("strong").any():

        evidence_level = "Strong"

    elif evidence_text.str.contains("moderate").any():

        evidence_level = "Moderate"

    else:

        evidence_level = "Limited"

else:

    evidence_level = "Moderate"


# ============================================================
# IMPACT SCORE
# ============================================================

# Impact Score based on actual gene-level log2FC values.
#
# Formula:
#     Impact Score =
#         min((mean(abs(log2FC)) / 2.0) * 100, 100)
#
# The absolute value measures the magnitude of molecular change,
# so positive and negative log2FC values contribute equally by magnitude.
# A mean absolute log2FC of 2.0 or higher corresponds to 100/100.

if (
    not selected_genes.empty
    and "log2FC" in selected_genes.columns
):

    logfc_values = pd.to_numeric(
        selected_genes["log2FC"],
        errors="coerce"
    ).dropna()

    if not logfc_values.empty:

        mean_abs_logfc = logfc_values.abs().mean()

        impact_score = int(
            round(
                min(
                    (mean_abs_logfc / 2.0) * 100,
                    100
                )
            )
        )

    else:

        impact_score = 0

else:

    impact_score = 0


# ============================================================
# MAIN HEADER
# ============================================================

st.caption("CURRENTLY VIEWING")

st.title(selected_pollutant)

st.caption(
    "Placental molecular response profile"
)


# ============================================================
# SOURCE NOTICE
# ============================================================

if selected_pollutant == "PM2.5":

    st.success(
        "PM2.5 is connected to the project's existing GEO-derived dataset."
    )

else:

    st.info(
        f"{selected_pollutant} is currently represented using "
        "prototype/demo data. These values are for dashboard "
        "demonstration and are not clinical findings."
    )


# ============================================================
# SUMMARY CARDS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.markdown(
        f"""
        <div class="omika-summary-card">
            <div class="omika-summary-label">
                Selected Pollutant
            </div>
            <div class="omika-summary-value">
                {selected_pollutant}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="omika-summary-card">
            <div class="omika-summary-label">
                Genes Associated
            </div>
            <div class="omika-summary-value">
                {gene_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="omika-summary-card">
            <div class="omika-summary-label">
                Candidate Biomarkers
            </div>
            <div class="omika-summary-value">
                {biomarker_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="omika-summary-card">
            <div class="omika-summary-label">
                Evidence Level
            </div>
            <div class="omika-summary-value">
                {evidence_level}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c5:

    st.markdown(
        f"""
        <div class="omika-summary-card">
            <div class="omika-summary-label">
                Impact Score
            </div>
            <div class="omika-summary-value">
                {impact_score}/100
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EXPLORE EVIDENCE
# ============================================================

st.markdown("## Explore Evidence")

st.caption(
    "Click a section to explore the molecular evidence."
)


b1, b2, b3, b4 = st.columns(4)


with b1:

    if st.button(
        "Associated Genes",
        key="genes"
    ):

        st.session_state.active_section = "genes"


with b2:

    if st.button(
        "Pathways",
        key="pathways"
    ):

        st.session_state.active_section = "pathways"


with b3:

    if st.button(
        "Evidence",
        key="evidence"
    ):

        st.session_state.active_section = "evidence"


with b4:

    if st.button(
        "Placental Outcomes",
        key="outcomes"
    ):

        st.session_state.active_section = "outcomes"


# ============================================================
# PERMANENT ACTIVE BUTTON OUTLINE
# ============================================================

# Streamlit exposes widget keys as CSS classes prefixed with
# "st-key-". This lets the selected navigation button keep
# its red outline after the click and across reruns.

active_nav_key = st.session_state.active_section

if active_nav_key in {
    "genes",
    "pathways",
    "evidence",
    "outcomes"
}:

    st.markdown(
        f"""
        <style>
            .st-key-{active_nav_key} button {{
                border: 2px solid #D94A4A !important;
                box-shadow: 0 0 0 1px #D94A4A !important;
            }}

            .st-key-{active_nav_key} button:hover {{
                border: 2px solid #D94A4A !important;
                box-shadow: 0 0 0 1px #D94A4A !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

if st.session_state.active_section == "overview":

    left, right = st.columns(2)


    with left:

        st.subheader(
            "What does OMIKA connect?"
        )

        st.write(
            "Pollutant exposure is connected to "
            "molecular changes observed in placental "
            "or trophoblast-related datasets."
        )

        st.write(
            "The dashboard links associated genes "
            "to candidate biomarkers, biological "
            "pathways and potential placental outcomes."
        )


    with right:

        st.subheader(
            "Evidence pipeline"
        )

        st.write(
            "Pollutant → Associated genes → "
            "Candidate biomarkers → Pathways / GO → "
            "Placental processes → Evidence level"
        )


# ============================================================
# GENES
# ============================================================

elif st.session_state.active_section == "genes":

    st.subheader(
        f"Associated Genes — {selected_pollutant}"
    )


    if selected_genes.empty:

        st.warning(
            "No gene-level data is available."
        )

    else:

        cols = [
            c for c in [
                "gene_symbol",
                "log2FC",
                "p_value",
                "Direction",
                "evidence_type",
                "Pathway"
            ]
            if c in selected_genes.columns
        ]

        st.dataframe(
            selected_genes[cols],
            use_container_width=True,
            hide_index=True
        )


        # Gene chart

        if (
            "gene_symbol" in selected_genes.columns
            and "log2FC" in selected_genes.columns
        ):

            chart = selected_genes[
                ["gene_symbol", "log2FC"]
            ].copy()

            chart["log2FC"] = pd.to_numeric(
                chart["log2FC"],
                errors="coerce"
            )

            chart = chart.dropna()

            if not chart.empty:

                chart = chart.sort_values(
                    "log2FC"
                )

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                ax.barh(
                    chart["gene_symbol"],
                    chart["log2FC"]
                )

                ax.axvline(
                    0,
                    linewidth=1
                )

                ax.set_xlabel(
                    "log2 Fold Change"
                )

                ax.set_ylabel(
                    "Gene"
                )

                ax.set_title(
                    f"Gene response — {selected_pollutant}"
                )

                plt.tight_layout()

                st.pyplot(fig)

                plt.close(fig)


# ============================================================
# PATHWAYS
# ============================================================

elif st.session_state.active_section == "pathways":

    st.subheader(
        f"Pathways — {selected_pollutant}"
    )


    if selected_pathways.empty:

        st.warning(
            "No pathway data is available."
        )

    else:

        cols = [
            c for c in [
                "Pathway",
                "gene_symbol",
                "Evidence"
            ]
            if c in selected_pathways.columns
        ]

        st.dataframe(
            selected_pathways[cols],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# EVIDENCE
# ============================================================

elif st.session_state.active_section == "evidence":

    st.subheader(
        f"Evidence — {selected_pollutant}"
    )


    if selected_evidence.empty:

        st.warning(
            "No evidence data is available."
        )

    else:

        cols = [
            c for c in [
                "gene_symbol",
                "Biomarker",
                "Pathway",
                "Evidence",
                "evidence_type"
            ]
            if c in selected_evidence.columns
        ]

        st.dataframe(
            selected_evidence[cols],
            use_container_width=True,
            hide_index=True
        )


        if "Evidence" in selected_evidence.columns:

            counts = (
                selected_evidence["Evidence"]
                .value_counts()
            )

            fig, ax = plt.subplots(
                figsize=(7, 4)
            )

            counts.plot(
                kind="bar",
                ax=ax
            )

            ax.set_xlabel(
                "Evidence level"
            )

            ax.set_ylabel(
                "Records"
            )

            ax.set_title(
                "Evidence distribution"
            )

            plt.xticks(rotation=0)

            plt.tight_layout()

            st.pyplot(fig)

            plt.close(fig)


# ============================================================
# PLACENTAL OUTCOMES
# ============================================================

elif st.session_state.active_section == "outcomes":

    st.subheader(
        f"Placental Outcomes — {selected_pollutant}"
    )


    outcomes = {

        "PM2.5": [
            "Oxidative stress",
            "Mitochondrial dysfunction",
            "Trophoblast apoptosis",
            "Altered trophoblast function"
        ],

        "Arsenic": [
            "Oxidative stress",
            "Altered placental transport",
            "Metal-response pathways",
            "Placental molecular response"
        ],

        "Pb": [
            "Oxidative stress",
            "Inflammatory signaling",
            "Metal-response signaling",
            "Cellular stress response"
        ],

        "Cd": [
            "Oxidative stress",
            "Detoxification response",
            "Metal-response signaling",
            "Cellular stress response"
        ],

        "NO2": [
            "Oxidative stress",
            "Inflammatory signaling",
            "Xenobiotic response",
            "Cellular stress response"
        ],

        "SO2": [
            "Oxidative stress",
            "Inflammatory signaling",
            "Detoxification response",
            "Cellular stress response"
        ]
    }


    for outcome in outcomes.get(
        selected_pollutant,
        ["Placental molecular response"]
    ):

        st.write(
            f"• {outcome}"
        )


    st.caption(
        "Prototype biological associations shown for dashboard "
        "demonstration; they should not be interpreted as clinical diagnoses."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "OMIKA | Placental Health Analyzer"
)