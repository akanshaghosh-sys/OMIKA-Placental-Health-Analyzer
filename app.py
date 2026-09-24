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

    /* ========================================================
       MAIN BACKGROUND
       ======================================================== */

    .stApp {{
        background:
            radial-gradient(
                circle at 90% 5%,
                rgba(57,121,124,0.13),
                transparent 25%
            ),
            radial-gradient(
                circle at 5% 90%,
                rgba(97,158,160,0.10),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #F5FBFA 0%,
                {BG} 55%,
                #D7ECEB 100%
            );
    }}


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                #619EA0 0%,
                #528F92 55%,
                #477F82 100%
            );

        border-right: 1px solid rgba(255,255,255,0.18);
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: white !important;
    }}


    /* ========================================================
       SIDEBAR SELECTBOX
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] {{
        background-color: white;
        border-radius: 10px;
    }}

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {{
        background-color: white;
        border-radius: 10px;
        color: {TEXT};
    }}

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {{
        color: {TEXT} !important;
    }}


    /* ========================================================
       HEADINGS
       ======================================================== */

    .main h1 {{
        color: #17383D !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em;
    }}

    .main h2 {{
        color: #17383D !important;
        font-weight: 750 !important;
        letter-spacing: -0.025em;
    }}

    .main h3 {{
        color: #285F63 !important;
        font-weight: 700 !important;
    }}


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {{
        background:
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F3FAF9 100%
            );

        border: 1px solid {BORDER};
        border-radius: 18px;

        padding: 18px;

        min-height: 125px;

        box-shadow:
            0 8px 22px rgba(40,95,99,0.09);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-3px);

        box-shadow:
            0 13px 28px rgba(40,95,99,0.14);
    }}


    /* Metric labels */

    div[data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-weight: 600 !important;
    }}


    /* Metric values */

    div[data-testid="stMetricValue"] {{
        color: {TEAL_DARK} !important;

        font-size: 28px !important;

        font-weight: 700 !important;

        white-space: nowrap !important;

        overflow: visible !important;

        text-overflow: clip !important;

        letter-spacing: -0.02em;
    }}


    /* Specifically give text such as Moderate enough room */

    div[data-testid="stMetricValue"] > div {{
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }}


    /* ========================================================
       ALERT / INFO BOXES
       ======================================================== */

    div[data-testid="stAlert"] {{
        border-radius: 16px !important;

        box-shadow:
            0 6px 18px rgba(40,95,99,0.07);
    }}


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {{
        width: 100%;

        background:
            linear-gradient(
                135deg,
                #FFFFFF 0%,
                #F0F9F8 100%
            );

        color: {TEAL_DARK} !important;

        border: 1px solid {BORDER};

        border-radius: 12px;

        font-weight: 650;

        padding: 0.68rem;

        box-shadow:
            0 4px 12px rgba(40,95,99,0.06);

        transition:
            all 0.2s ease;
    }}

    .stButton > button:hover {{
        background:
            linear-gradient(
                135deg,
                #EDF8F7 0%,
                #DCEFED 100%
            );

        border-color: {TEAL};

        color: {TEAL_DARK} !important;

        transform: translateY(-2px);

        box-shadow:
            0 8px 18px rgba(40,95,99,0.11);
    }}


    /* ========================================================
       DOWNLOAD BUTTON
       ======================================================== */

    .stDownloadButton > button {{
        width: 100%;

        background:
            linear-gradient(
                135deg,
                #285F63 0%,
                #39797C 100%
            );

        color: white !important;

        border: none;

        border-radius: 12px;

        font-weight: 700;

        padding: 0.75rem 1rem;

        box-shadow:
            0 8px 20px rgba(40,95,99,0.17);

        transition:
            all 0.2s ease;
    }}

    .stDownloadButton > button:hover {{
        background:
            linear-gradient(
                135deg,
                #214F53 0%,
                #326C70 100%
            );

        color: white !important;

        transform: translateY(-2px);

        box-shadow:
            0 11px 25px rgba(40,95,99,0.22);
    }}


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;

        box-shadow:
            0 6px 18px rgba(40,95,99,0.06);
    }}


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {{
        border-color: rgba(57,121,124,0.20) !important;
    }}


    /* ========================================================
       CAPTIONS
       ======================================================== */

    .main .stCaption {{
        color: {MUTED};
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

        if x in [
            "gene",
            "genes",
            "gene_symbol"
        ]:

            rename[col] = "gene_symbol"

        elif x in [
            "logfc",
            "log_2_fc",
            "log2fc"
        ]:

            rename[col] = "log2FC"

        elif x in [
            "pvalue",
            "p_value",
            "p-val",
            "pval"
        ]:

            rename[col] = "p_value"

        elif x in [
            "pathway",
            "pathway_name"
        ]:

            rename[col] = "Pathway"

        elif x in [
            "biomarker",
            "biomarkers"
        ]:

            rename[col] = "Biomarker"

        elif x in [
            "evidence",
            "evidence_level"
        ]:

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

    [
        "Arsenic",
        "AQP9",
        1.42,
        0.003,
        "Upregulated",
        "Literature-grounded demo",
        "Transport and metabolism",
        "AQP9",
        "Moderate evidence"
    ],

    [
        "Arsenic",
        "ENPP2",
        1.18,
        0.008,
        "Upregulated",
        "Literature-grounded demo",
        "Lipid signaling",
        "ENPP2",
        "Moderate evidence"
    ],

    [
        "Arsenic",
        "AS3MT",
        1.65,
        0.002,
        "Upregulated",
        "Literature-grounded demo",
        "Arsenic metabolism",
        "AS3MT",
        "Strong evidence"
    ],

    [
        "Arsenic",
        "SLC39A2",
        0.96,
        0.021,
        "Upregulated",
        "Literature-grounded demo",
        "Metal ion transport",
        "SLC39A2",
        "Limited evidence"
    ],

    [
        "Arsenic",
        "GSTM1",
        -1.11,
        0.015,
        "Downregulated",
        "Literature-grounded demo",
        "Oxidative stress",
        "GSTM1",
        "Limited evidence"
    ],


    # ---------------- LEAD ----------------

    [
        "Pb",
        "MT1A",
        1.31,
        0.012,
        "Upregulated",
        "Synthetic demo data",
        "Metal response",
        "MT1A",
        "Moderate evidence"
    ],

    [
        "Pb",
        "MT2A",
        1.17,
        0.018,
        "Upregulated",
        "Synthetic demo data",
        "Metal response",
        "MT2A",
        "Moderate evidence"
    ],

    [
        "Pb",
        "HMOX1",
        1.44,
        0.009,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "HMOX1",
        "Moderate evidence"
    ],

    [
        "Pb",
        "SOD1",
        0.82,
        0.031,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "SOD1",
        "Limited evidence"
    ],

    [
        "Pb",
        "IL6",
        1.08,
        0.022,
        "Upregulated",
        "Synthetic demo data",
        "Inflammatory signaling",
        "IL6",
        "Limited evidence"
    ],


    # ---------------- CADMIUM ----------------

    [
        "Cd",
        "MT1A",
        1.52,
        0.004,
        "Upregulated",
        "Synthetic demo data",
        "Metal response",
        "MT1A",
        "Moderate evidence"
    ],

    [
        "Cd",
        "MT2A",
        1.38,
        0.006,
        "Upregulated",
        "Synthetic demo data",
        "Metal response",
        "MT2A",
        "Moderate evidence"
    ],

    [
        "Cd",
        "HMOX1",
        1.21,
        0.013,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "HMOX1",
        "Moderate evidence"
    ],

    [
        "Cd",
        "GSTM1",
        -0.94,
        0.026,
        "Downregulated",
        "Synthetic demo data",
        "Detoxification",
        "GSTM1",
        "Limited evidence"
    ],


    # ---------------- NO2 ----------------

    [
        "NO2",
        "CYP1A1",
        1.26,
        0.011,
        "Upregulated",
        "Synthetic demo data",
        "Xenobiotic metabolism",
        "CYP1A1",
        "Moderate evidence"
    ],

    [
        "NO2",
        "HMOX1",
        1.13,
        0.019,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "HMOX1",
        "Moderate evidence"
    ],

    [
        "NO2",
        "IL6",
        0.91,
        0.029,
        "Upregulated",
        "Synthetic demo data",
        "Inflammatory signaling",
        "IL6",
        "Limited evidence"
    ],

    [
        "NO2",
        "NQO1",
        1.34,
        0.007,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "NQO1",
        "Moderate evidence"
    ],


    # ---------------- SO2 ----------------

    [
        "SO2",
        "HMOX1",
        1.08,
        0.016,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "HMOX1",
        "Moderate evidence"
    ],

    [
        "SO2",
        "IL6",
        1.22,
        0.014,
        "Upregulated",
        "Synthetic demo data",
        "Inflammatory signaling",
        "IL6",
        "Moderate evidence"
    ],

    [
        "SO2",
        "SOD1",
        0.77,
        0.035,
        "Upregulated",
        "Synthetic demo data",
        "Oxidative stress",
        "SOD1",
        "Limited evidence"
    ],

    [
        "SO2",
        "GSTM1",
        -0.88,
        0.027,
        "Downregulated",
        "Synthetic demo data",
        "Detoxification",
        "GSTM1",
        "Limited evidence"
    ],
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
# PLACENTAL OUTCOMES
#
# Defined here globally so the report section can also
# access the same information.
# ============================================================

OUTCOMES = {

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

if (
    not selected_genes.empty
    and "gene_symbol" in selected_genes.columns
):

    selected_genes = selected_genes.drop_duplicates(
        subset=["gene_symbol"]
    )


if (
    not selected_pathways.empty
    and "Pathway" in selected_pathways.columns
):

    selected_pathways = selected_pathways.drop_duplicates(
        subset=["Pathway"]
    )


if (
    not selected_biomarkers.empty
    and "Biomarker" in selected_biomarkers.columns
):

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

if (
    not selected_evidence.empty
    and "Evidence" in selected_evidence.columns
):

    evidence_text = (
        selected_evidence["Evidence"]
        .astype(str)
        .str.lower()
    )

    if evidence_text.str.contains(
        "strong"
    ).any():

        evidence_level = "Strong"

    elif evidence_text.str.contains(
        "moderate"
    ).any():

        evidence_level = "Moderate"

    else:

        evidence_level = "Limited"

else:

    evidence_level = "Moderate"


# ============================================================
# IMPACT SCORE
# ============================================================

# Impact Score based on actual gene-level log2FC values.
# A mean absolute log2FC of 2.0 corresponds to 100/100.

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

st.caption(
    "CURRENTLY VIEWING"
)

st.title(
    selected_pollutant
)

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

    st.metric(
        "Selected Pollutant",
        selected_pollutant
    )


with c2:

    st.metric(
        "Genes Associated",
        gene_count
    )


with c3:

    st.metric(
        "Candidate Biomarkers",
        biomarker_count
    )


with c4:

    st.metric(
        "Evidence Level",
        evidence_level
    )


with c5:

    st.metric(
        "Impact Score",
        f"{impact_score}/100"
    )


# ============================================================
# EXPLORE EVIDENCE
# ============================================================

st.markdown(
    "## Explore Evidence"
)

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
            c
            for c in [
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
                [
                    "gene_symbol",
                    "log2FC"
                ]
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
            c
            for c in [
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
            c
            for c in [
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

            plt.xticks(
                rotation=0
            )

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


    for outcome in OUTCOMES.get(
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
# DOWNLOAD REPORT
# ============================================================

st.markdown("---")

st.markdown(
    "## Download Report"
)

st.caption(
    "Save a snapshot of the currently selected pollutant "
    "and its dashboard summary."
)


# ============================================================
# CREATE REPORT CONTENT
# ============================================================

report_lines = [

    "OMIKA | Placental Health Analyzer",

    "=" * 42,

    "",

    f"Selected pollutant: {selected_pollutant}",

    f"Genes associated: {gene_count}",

    f"Candidate biomarkers: {biomarker_count}",

    f"Pathways: {pathway_count}",

    f"Evidence level: {evidence_level}",

    f"Impact score: {impact_score}/100",

    "Impact score method:",

    "min((mean(abs(log2FC)) / 2.0) * 100, 100)",

    "",

    "Placental outcomes:"
]


for outcome in OUTCOMES.get(
    selected_pollutant,
    ["Placental molecular response"]
):

    report_lines.append(
        f"- {outcome}"
    )


report_lines.extend(
    [
        "",
        (
            "Note: Prototype/demo associations shown "
            "by the dashboard are for demonstration "
            "and are not clinical findings."
        )
    ]
)


report_text = "\n".join(
    report_lines
)


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

st.download_button(
    label="Download Current Report",

    data=report_text,

    file_name=(
        f"OMIKA_{selected_pollutant}_report.txt"
    ),

    mime="text/plain",

    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "OMIKA | Placental Health Analyzer"
)