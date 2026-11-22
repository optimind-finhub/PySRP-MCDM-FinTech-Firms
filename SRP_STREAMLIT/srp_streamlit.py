import streamlit as st
import pandas as pd
import numpy as np
from srp import SRP
from mpsi import compute_mpsi
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SRP-MCDM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# WHITE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL WHITE BACKGROUND
       ======================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .stApp,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    section.main,
    .main,
    .block-container {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    .block-container {
        max-width: 1500px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }

    p,
    label,
    span,
    div {
        color: #1f2937;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input,
    textarea,
    [data-baseweb="select"] > div,
    [data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-color: #cbd5e1 !important;
    }

    input::placeholder {
        color: #64748b !important;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    [data-baseweb="select"] {
        background-color: #ffffff !important;
    }

    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        border: 2px dashed #94a3b8 !important;
        border-radius: 10px !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
    }

    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }


    /* ========================================================
       DOWNLOAD BUTTONS
       ======================================================== */

    .stDownloadButton > button {
        background-color: #ffffff !important;
        color: #1e3a8a !important;
        border: 1px solid #93c5fd !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stDownloadButton > button:hover {
        background-color: #eff6ff !important;
        border-color: #2563eb !important;
        color: #1d4ed8 !important;
    }


    /* ========================================================
       DATAFRAMES / TABLE CONTAINERS
       ======================================================== */

    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    [data-testid="stDataFrame"] > div {
        background-color: #ffffff !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb !important;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .info-card {
        background-color: #eff6ff !important;
        border-left: 5px solid #2563eb !important;
        border-radius: 8px;
        padding: 15px 18px;
        margin: 10px 0 25px 0;
    }

    .success-card {
        background-color: #f0fdf4 !important;
        border-left: 5px solid #16a34a !important;
        border-radius: 8px;
        padding: 15px 18px;
        margin: 15px 0;
    }

    .warning-card {
        background-color: #fffbeb !important;
        border-left: 5px solid #f59e0b !important;
        border-radius: 8px;
        padding: 15px 18px;
        margin: 15px 0;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-top: 1px solid #e2e8f0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def plot_layout(fig, title=None):
    """
    Plotly layout.
    Visualization only.
    Does NOT modify calculation values.
    """

    fig.update_layout(
        title=title,
        template="plotly_white",

        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            size=14,
            color="#111827"
        ),

        title_font=dict(
            size=20,
            color="#111827"
        ),

        xaxis=dict(
            color="#111827",

            title_font=dict(
                size=15,
                color="#111827"
            ),

            tickfont=dict(
                size=12,
                color="#111827"
            ),

            showline=True,
            linecolor="#374151",
            linewidth=1,

            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            color="#111827",

            title_font=dict(
                size=15,
                color="#111827"
            ),

            tickfont=dict(
                size=12,
                color="#111827"
            ),

            showline=True,
            linecolor="#374151",
            linewidth=1,

            showgrid=True,
            gridcolor="#e5e7eb",

            zeroline=False
        ),

        legend=dict(
            font=dict(
                color="#111827"
            ),
            bgcolor="#ffffff"
        ),

        hoverlabel=dict(
            bgcolor="#ffffff",
            font_color="#111827"
        ),

        margin=dict(
            l=90,
            r=50,
            t=80,
            b=100
        )
    )

    return fig


def format_numeric_dataframe(dataframe, decimals=6):
    """
    DISPLAY ONLY.

    This function creates a copy.
    It NEVER changes calculation values.
    """

    df_out = dataframe.copy()

    for column in df_out.columns:

        if pd.api.types.is_numeric_dtype(df_out[column]):

            if str(column).lower() == "rank":

                df_out[column] = (
                    df_out[column]
                    .astype(int)
                )

            else:

                df_out[column] = (
                    df_out[column]
                    .round(decimals)
                )

    return df_out


def clean_result(result):
    """
    Preserve the original SRP result.

    Only sorting is performed for display.
    No numerical values are recalculated.
    """

    result = pd.DataFrame(result).copy()

    if "Rank" in result.columns:

        result = (
            result
            .sort_values(
                "Rank",
                kind="stable"
            )
            .reset_index(drop=True)
        )

    return result


# ============================================================
# SESSION STATE
# ============================================================

if "srp_result" not in st.session_state:
    st.session_state.srp_result = None

if "srp_R" not in st.session_state:
    st.session_state.srp_R = None

if "srp_Theta" not in st.session_state:
    st.session_state.srp_Theta = None

if "srp_weights" not in st.session_state:
    st.session_state.srp_weights = None

if "srp_alternatives" not in st.session_state:
    st.session_state.srp_alternatives = None

if "srp_criteria" not in st.session_state:
    st.session_state.srp_criteria = None

if "srp_n_benefit" not in st.session_state:
    st.session_state.srp_n_benefit = None

if "uploaded_file_signature" not in st.session_state:
    st.session_state.uploaded_file_signature = None


# ============================================================
# TITLE
# ============================================================

st.title("📊 SRP-MCDM")

st.markdown(
    """
    <div class="info-card">
        <strong>SRP-MCDM Analysis</strong><br>
        Upload your decision matrix, select benefit criteria,
        choose manual or MPSI weights, and run the SRP
        calculation.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 1. FILE UPLOAD
# ============================================================

st.subheader("1. Upload Decision Matrix")

uploaded_file = st.file_uploader(
    "Upload Decision Matrix (CSV or Excel)",
    type=["csv", "xlsx"],
    help=(
        "First column = alternatives. "
        "Remaining columns = numerical criteria."
    )
)

if uploaded_file is None:

    st.info(
        "📁 Please upload a CSV or Excel file to continue."
    )

    st.stop()


# ============================================================
# DETECT NEW FILE
# ============================================================

file_signature = (
    uploaded_file.name,
    uploaded_file.size
)

if (
    st.session_state.uploaded_file_signature is not None
    and
    st.session_state.uploaded_file_signature != file_signature
):

    # New file = previous SRP result is no longer valid.
    st.session_state.srp_result = None
    st.session_state.srp_R = None
    st.session_state.srp_Theta = None
    st.session_state.srp_weights = None
    st.session_state.srp_alternatives = None
    st.session_state.srp_criteria = None
    st.session_state.srp_n_benefit = None

st.session_state.uploaded_file_signature = file_signature


# ============================================================
# READ FILE
# ============================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(
        f"Error reading file: {e}"
    )

    st.stop()


# ============================================================
# VALIDATE FILE
# ============================================================

if df.empty:

    st.error(
        "The uploaded file is empty."
    )

    st.stop()


if df.shape[1] < 2:

    st.error(
        "The file must contain at least two columns: "
        "Alternative + one criterion."
    )

    st.stop()


# ============================================================
# PREPARE DATA
# ============================================================

alternatives = (
    df.iloc[:, 0]
    .astype(str)
    .tolist()
)

criteria = (
    df.columns[1:]
    .tolist()
)

num_crit = len(criteria)


try:

    # IMPORTANT:
    # Exactly the same matrix conversion as original code.

    matrix = (
        df.iloc[:, 1:]
        .astype(float)
        .values
    )

except Exception as e:

    st.error(
        "All criterion columns must contain numerical values."
    )

    st.stop()


# ============================================================
# 2. DECISION MATRIX
# ============================================================

st.subheader("2. Decision Matrix")

decision_display = df.copy()

for criterion in criteria:

    decision_display[criterion] = (
        pd.to_numeric(
            decision_display[criterion],
            errors="coerce"
        )
        .round(4)
    )

st.dataframe(
    decision_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATA SUMMARY
# ============================================================

summary = st.columns(3)

with summary[0]:

    st.metric(
        "Alternatives",
        len(alternatives)
    )

with summary[1]:

    st.metric(
        "Criteria",
        num_crit
    )

with summary[2]:

    st.metric(
        "Data Points",
        len(alternatives) * num_crit
    )


# ============================================================
# 3. CRITERIA SETTINGS
# ============================================================

st.subheader("3. Criteria Settings")

n_benefit = st.number_input(
    "Number of Benefit Criteria (first n columns)",
    min_value=0,
    max_value=num_crit,
    value=num_crit,
    step=1
)

# Make absolutely sure SRP receives an integer.
n_benefit = int(n_benefit)

benefit_criteria = criteria[:n_benefit]

cost_criteria = criteria[n_benefit:]


col_a, col_b = st.columns(2)

with col_a:

    st.markdown(
        """
        <div class="success-card">
            <strong>Benefit Criteria</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    if benefit_criteria:

        st.write(
            ", ".join(
                map(str, benefit_criteria)
            )
        )

    else:

        st.write("None")


with col_b:

    st.markdown(
        """
        <div class="warning-card">
            <strong>Cost Criteria</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    if cost_criteria:

        st.write(
            ", ".join(
                map(str, cost_criteria)
            )
        )

    else:

        st.write("None")


# ============================================================
# DIRECTIONS FOR MPSI
# ============================================================

directions = [
    1 if i < n_benefit else 0
    for i in range(num_crit)
]


# ============================================================
# 4. MPSI
# ============================================================

st.subheader("4. MPSI Weight Calculation")

try:

    mpsi_df = compute_mpsi(
        df.iloc[:, 1:].copy(),
        directions
    )

    mpsi_weights = np.asarray(
        mpsi_df["Weight"],
        dtype=float
    )

except Exception as e:

    st.error(
        f"MPSI calculation failed: {e}"
    )

    st.stop()


with st.expander(
    "View MPSI Computed Weights",
    expanded=False
):

    mpsi_display = mpsi_df.copy()

    if "Weight" in mpsi_display.columns:

        mpsi_display["Weight"] = (
            mpsi_display["Weight"]
            .astype(float)
            .round(4)
        )

    st.dataframe(
        mpsi_display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 5. WEIGHT SELECTION
# ============================================================

st.subheader("5. Weight Selection")

use_mpsi_weights = st.checkbox(
    "Use MPSI Computed Weights",
    value=False
)


# ============================================================
# WEIGHTS
# ============================================================

weights = []

weight_cols = st.columns(num_crit)

for i, criterion in enumerate(criteria):

    with weight_cols[i]:

        if use_mpsi_weights:

            # MPSI weights are shown AND used at 4 decimals,
            # exactly as reported in the paper (e.g. RVS = 0.1557).

            default_weight = (
                f"{mpsi_weights[i]:.4f}"
            )

        else:

            default_weight = "1.0000"


        weight_value_text = st.text_input(
            label=criterion,
            value=default_weight,
            key=f"weight_input_{i}_{use_mpsi_weights}"
        )


        try:

            weight_value = float(
                weight_value_text
            )

        except ValueError:

            st.error(
                f"Invalid weight for {criterion}"
            )

            st.stop()


        if weight_value < 0:

            st.error(
                f"Weight for {criterion} cannot be negative."
            )

            st.stop()


        # ====================================================
        # The SRP model receives exactly the value in the input
        # box (4-decimal MPSI weights when the MPSI box is ticked).
        # ====================================================

        weights.append(
            weight_value
        )


weights = np.asarray(
    weights,
    dtype=float
)


# ============================================================
# WEIGHT TABLE
# ============================================================

weight_table = pd.DataFrame(
    {
        "Criterion": criteria,

        "Weight": weights,

        "Type": [
            "Benefit"
            if i < n_benefit
            else "Cost"
            for i in range(num_crit)
        ]
    }
)

weight_table_display = (
    weight_table.copy()
)

weight_table_display["Weight"] = (
    weight_table_display["Weight"]
    .round(4)
)

st.dataframe(
    weight_table_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CALCULATION NOTE
# ============================================================

st.markdown(
    """
    <div class="info-card">
        <strong>Calculation precision:</strong>
        The decision matrix is passed to the original SRP model at full
        precision. MPSI weights are used at 4 decimals, as in the paper;
        manual weights are used exactly as typed.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 6. RUN SRP
# ============================================================

st.subheader("6. SRP Calculation")

run_srp = st.button(
    "▶ Run SRP Analysis",
    use_container_width=True
)


# ============================================================
# SRP CALCULATION
# ============================================================

if run_srp:

    try:

        # ====================================================
        # THIS IS THE ORIGINAL SRP CALCULATION
        # ====================================================

        model = SRP(
            matrix=matrix,
            weights=weights,
            alternatives=alternatives,
            n_benefit=n_benefit
        )

        result = model.rank()


    except Exception as e:

        st.error(
            f"SRP calculation failed: {e}"
        )

        st.stop()


    # ========================================================
    # STORE EXACT ORIGINAL OUTPUTS
    # ========================================================

    st.session_state.srp_result = (
        pd.DataFrame(result).copy()
    )

    st.session_state.srp_R = (
        np.asarray(model.R).copy()
    )

    st.session_state.srp_Theta = (
        np.asarray(model.Theta).copy()
    )

    st.session_state.srp_weights = (
        weights.copy()
    )

    st.session_state.srp_alternatives = (
        alternatives.copy()
    )

    st.session_state.srp_criteria = (
        criteria.copy()
    )

    st.session_state.srp_n_benefit = (
        int(n_benefit)
    )


# ============================================================
# CHECK RESULT
# ============================================================

if st.session_state.srp_result is None:

    st.info(
        "Enter your settings and click **Run SRP Analysis**."
    )

    st.stop()


# ============================================================
# LOAD STORED RESULTS
# ============================================================

result = (
    st.session_state.srp_result.copy()
)

R_matrix = (
    st.session_state.srp_R.copy()
)

Theta_matrix = (
    st.session_state.srp_Theta.copy()
)

calculated_weights = (
    st.session_state.srp_weights.copy()
)

calculated_alternatives = (
    st.session_state.srp_alternatives.copy()
)

calculated_criteria = (
    st.session_state.srp_criteria.copy()
)

calculated_n_benefit = (
    st.session_state.srp_n_benefit
)


# ============================================================
# SORT RESULT FOR DISPLAY ONLY
# ============================================================

result_sorted = clean_result(
    result
)


# ============================================================
# 7. R MATRIX
# ============================================================

st.subheader("7. Ranking Matrix (R)")

R_df = pd.DataFrame(
    R_matrix,
    columns=calculated_criteria,
    index=calculated_alternatives
)

R_df.index.name = "Alternative"

R_display = (
    R_df
    .reset_index()
)

R_display_formatted = (
    format_numeric_dataframe(
        R_display,
        decimals=6
    )
)

st.dataframe(
    R_display_formatted,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 8. THETA MATRIX
# ============================================================

st.subheader("8. Weighted Ranking Matrix (θ)")

Theta_df = pd.DataFrame(
    Theta_matrix,
    columns=calculated_criteria,
    index=calculated_alternatives
)

Theta_df.index.name = "Alternative"

Theta_display = (
    Theta_df
    .reset_index()
)

Theta_display_formatted = (
    format_numeric_dataframe(
        Theta_display,
        decimals=6
    )
)

st.dataframe(
    Theta_display_formatted,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 9. FINAL RESULT
# ============================================================

st.subheader("9. Final SRP Ranking")

result_display = (
    format_numeric_dataframe(
        result_sorted,
        decimals=6
    )
)

st.dataframe(
    result_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# BEST ALTERNATIVE
# ============================================================

if not result_sorted.empty:

    best = (
        result_sorted.iloc[0]
    )

    best_name = best.get(
        "Alternative",
        "N/A"
    )

    best_rank = best.get(
        "Rank",
        "N/A"
    )

    st.markdown(
        f"""
        <div class="success-card">
            <strong>🏆 Best Alternative</strong><br><br>
            <strong>{best_name}</strong>
            &nbsp;&nbsp; | &nbsp;&nbsp;
            Rank: <strong>{best_rank}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 10. CALCULATION AUDIT
# ============================================================

st.subheader("10. Calculation Audit")

st.caption(
    "This section shows the numerical values retained by the "
    "SRP calculation. Display rounding does not modify these values."
)


with st.expander(
    "Show calculation inputs and full-precision outputs"
):

    # ========================================================
    # ORIGINAL MATRIX
    # ========================================================

    st.markdown(
        "### Decision Matrix — Values Passed to SRP"
    )

    input_matrix_df = pd.DataFrame(
        matrix,
        columns=calculated_criteria,
        index=calculated_alternatives
    )

    input_matrix_df.index.name = "Alternative"

    input_matrix_full = (
        input_matrix_df
        .reset_index()
        .copy()
    )

    for c in calculated_criteria:

        input_matrix_full[c] = (
            input_matrix_full[c]
            .map(
                lambda x: repr(float(x))
            )
        )

    st.dataframe(
        input_matrix_full,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # BENEFIT / COST
    # ========================================================

    st.markdown(
        "### SRP Benefit/Cost Configuration"
    )

    direction_audit = pd.DataFrame(
        {
            "Criterion": calculated_criteria,

            "Direction": [
                1
                if i < calculated_n_benefit
                else 0
                for i in range(
                    len(calculated_criteria)
                )
            ],

            "Type": [
                "Benefit"
                if i < calculated_n_benefit
                else "Cost"
                for i in range(
                    len(calculated_criteria)
                )
            ]
        }
    )

    st.dataframe(
        direction_audit,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # WEIGHTS
    # ========================================================

    st.markdown(
        "### Weights Actually Passed to SRP"
    )

    audit_weights = pd.DataFrame(
        {
            "Criterion": calculated_criteria,

            "Weight Used by SRP": [
                repr(float(x))
                for x in calculated_weights
            ],

            "Type": [
                "Benefit"
                if i < calculated_n_benefit
                else "Cost"
                for i in range(
                    len(calculated_criteria)
                )
            ]
        }
    )

    st.dataframe(
        audit_weights,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # R FULL PRECISION
    # ========================================================

    st.markdown(
        "### R Matrix — Full Precision"
    )

    R_full = (
        R_df
        .copy()
    )

    for c in R_full.columns:

        R_full[c] = (
            R_full[c]
            .map(
                lambda x: repr(float(x))
            )
        )

    R_full = (
        R_full
        .reset_index()
    )

    st.dataframe(
        R_full,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # THETA FULL PRECISION
    # ========================================================

    st.markdown(
        "### θ Matrix — Full Precision"
    )

    Theta_full = (
        Theta_df
        .copy()
    )

    for c in Theta_full.columns:

        Theta_full[c] = (
            Theta_full[c]
            .map(
                lambda x: repr(float(x))
            )
        )

    Theta_full = (
        Theta_full
        .reset_index()
    )

    st.dataframe(
        Theta_full,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # FINAL RESULT FULL PRECISION
    # ========================================================

    st.markdown(
        "### Final SRP Result — Full Precision"
    )

    result_full = (
        result
        .copy()
    )

    for c in result_full.columns:

        if pd.api.types.is_numeric_dtype(
            result_full[c]
        ):

            if c != "Rank":

                result_full[c] = (
                    result_full[c]
                    .map(
                        lambda x: repr(float(x))
                    )
                )

    st.dataframe(
        result_full,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 11. DOWNLOAD RESULTS
# ============================================================

st.subheader("11. Download Results")

result_csv = (
    result_sorted
    .to_csv(index=False)
    .encode("utf-8")
)

R_csv = (
    R_display
    .to_csv(index=False)
    .encode("utf-8")
)

Theta_csv = (
    Theta_display
    .to_csv(index=False)
    .encode("utf-8")
)

weights_csv = (
    weight_table
    .to_csv(index=False)
    .encode("utf-8")
)


download_cols = st.columns(4)


with download_cols[0]:

    st.download_button(
        "⬇ Final Result",
        result_csv,
        "srp_result.csv",
        "text/csv",
        use_container_width=True
    )


with download_cols[1]:

    st.download_button(
        "⬇ Ranking Matrix (R)",
        R_csv,
        "srp_ranking_matrix.csv",
        "text/csv",
        use_container_width=True
    )


with download_cols[2]:

    st.download_button(
        "⬇ Weighted Matrix (θ)",
        Theta_csv,
        "srp_weighted_matrix.csv",
        "text/csv",
        use_container_width=True
    )


with download_cols[3]:

    st.download_button(
        "⬇ Weights",
        weights_csv,
        "srp_weights.csv",
        "text/csv",
        use_container_width=True
    )


# ============================================================
# 12. INTERACTIVE VISUALIZATIONS
# ============================================================

st.subheader("12. Interactive SRP Visualizations")

st.caption(
    "The controls below change only the visualization. "
    "They do not rerun or change the SRP calculation."
)


# ============================================================
# PREPARE PLOT DATA
# ============================================================

plot_df = (
    result_sorted
    .copy()
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏆 Ranking",
        "📊 SRP Scores",
        "🔥 Heatmaps",
        "🎯 Alternative Analysis",
        "⚖ Criterion Comparison"
    ]
)


# ============================================================
# TAB 1 — RANKING
# ============================================================

with tab1:

    st.markdown("### Final Ranking")

    if {
        "Alternative",
        "Rank"
    }.issubset(plot_df.columns):

        fig_rank = px.bar(
            plot_df,
            x="Alternative",
            y="Rank",
            text="Rank",
            color="Rank",

            color_continuous_scale=[
                "#16a34a",
                "#60a5fa",
                "#f59e0b",
                "#ef4444"
            ],

            hover_data=[
                "Alternative",
                "Rank"
            ]
        )

        fig_rank.update_yaxes(
            autorange="reversed",
            dtick=1,
            title="Rank"
        )

        fig_rank.update_xaxes(
            title="Alternative"
        )

        fig_rank.update_traces(
            textposition="outside"
        )

        fig_rank = plot_layout(
            fig_rank,
            "Final Ranking of Alternatives"
        )

        fig_rank.update_layout(
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_rank,
            use_container_width=True
        )


# ============================================================
# TAB 2 — SRP SCORES
# ============================================================

with tab2:

    # --------------------------------------------------------
    # TRS
    # --------------------------------------------------------

    if {
        "Alternative",
        "TRS"
    }.issubset(plot_df.columns):

        st.markdown(
            "### Total Rank Score (TRS)"
        )

        fig_trs = px.bar(
            plot_df,
            x="Alternative",
            y="TRS",
            text="TRS",
            color="TRS",
            color_continuous_scale="Blues",
            hover_data={
                "TRS": ":.8f"
            }
        )

        fig_trs.update_xaxes(
            title="Alternative"
        )

        fig_trs.update_yaxes(
            title="Total Rank Score (TRS)"
        )

        fig_trs.update_traces(
            texttemplate="%{y:.4f}",
            textposition="outside"
        )

        fig_trs = plot_layout(
            fig_trs,
            "Total Rank Score (TRS)"
        )

        fig_trs.update_layout(
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_trs,
            use_container_width=True
        )


    # --------------------------------------------------------
    # S
    # --------------------------------------------------------

    if {
        "Alternative",
        "S"
    }.issubset(plot_df.columns):

        st.markdown(
            "### S Score"
        )

        fig_s = px.line(
            plot_df,
            x="Alternative",
            y="S",
            markers=True,
            text="S",
            hover_data={
                "S": ":.8f"
            }
        )

        fig_s.update_xaxes(
            title="Alternative"
        )

        fig_s.update_yaxes(
            title="S Score"
        )

        fig_s.update_traces(
            line=dict(
                color="#2563eb",
                width=3
            ),

            marker=dict(
                color="#1d4ed8",
                size=10
            ),

            texttemplate="%{y:.4f}",
            textposition="top center"
        )

        fig_s = plot_layout(
            fig_s,
            "S Score Comparison"
        )

        st.plotly_chart(
            fig_s,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TRS VS S
    # --------------------------------------------------------

    if {
        "Alternative",
        "TRS",
        "S"
    }.issubset(plot_df.columns):

        st.markdown(
            "### TRS vs S"
        )

        fig_scatter = px.scatter(
            plot_df,
            x="S",
            y="TRS",
            text="Alternative",
            color="Rank",
            size="TRS",

            color_continuous_scale="RdYlGn_r",

            hover_data=[
                "Alternative",
                "Rank",
                "S",
                "TRS"
            ]
        )

        fig_scatter.update_xaxes(
            title="S Score"
        )

        fig_scatter.update_yaxes(
            title="Total Rank Score (TRS)"
        )

        fig_scatter.update_traces(
            textposition="top center"
        )

        fig_scatter = plot_layout(
            fig_scatter,
            "TRS vs S Score"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )


# ============================================================
# TAB 3 — HEATMAPS
# ============================================================

with tab3:

    st.markdown(
        "### Ranking Matrix Heatmap"
    )

    fig_R = px.imshow(
        R_df,
        text_auto=".4f",
        aspect="auto",
        color_continuous_scale="Blues",

        labels={
            "x": "Criterion",
            "y": "Alternative",
            "color": "R"
        }
    )

    fig_R.update_xaxes(
        title="Criterion"
    )

    fig_R.update_yaxes(
        title="Alternative"
    )

    fig_R = plot_layout(
        fig_R,
        "Ranking Matrix (R)"
    )

    st.plotly_chart(
        fig_R,
        use_container_width=True
    )


    st.markdown(
        "### Weighted Ranking Matrix Heatmap"
    )

    fig_theta = px.imshow(
        Theta_df,
        text_auto=".4f",
        aspect="auto",
        color_continuous_scale="Greens",

        labels={
            "x": "Criterion",
            "y": "Alternative",
            "color": "θ"
        }
    )

    fig_theta.update_xaxes(
        title="Criterion"
    )

    fig_theta.update_yaxes(
        title="Alternative"
    )

    fig_theta = plot_layout(
        fig_theta,
        "Weighted Ranking Matrix (θ)"
    )

    st.plotly_chart(
        fig_theta,
        use_container_width=True
    )


# ============================================================
# TAB 4 — ALTERNATIVE ANALYSIS
# ============================================================

with tab4:

    st.markdown(
        "### Individual Alternative Analysis"
    )

    selected_alt = st.selectbox(
        "Select Alternative",
        calculated_alternatives,
        key="selected_alt_visualization"
    )

    alt_index = (
        calculated_alternatives.index(
            selected_alt
        )
    )

    alt_R = (
        R_df.iloc[alt_index]
    )

    alt_theta = (
        Theta_df.iloc[alt_index]
    )


    # --------------------------------------------------------
    # FIND RESULT ROW
    # --------------------------------------------------------

    selected_result = result[
        result["Alternative"].astype(str)
        ==
        str(selected_alt)
    ]


    if not selected_result.empty:

        selected_row = (
            selected_result.iloc[0]
        )

        metric_cols = st.columns(3)


        with metric_cols[0]:

            if "Rank" in selected_row:

                st.metric(
                    "Rank",
                    int(
                        selected_row["Rank"]
                    )
                )


        with metric_cols[1]:

            if "TRS" in selected_row:

                st.metric(
                    "TRS",
                    f"{float(selected_row['TRS']):.6f}"
                )


        with metric_cols[2]:

            if "S" in selected_row:

                st.metric(
                    "S Score",
                    f"{float(selected_row['S']):.6f}"
                )


    # --------------------------------------------------------
    # CRITERION TABLE
    # --------------------------------------------------------

    alt_df = pd.DataFrame(
        {
            "Criterion": calculated_criteria,

            "Weight": calculated_weights,

            "Type": [
                "Benefit"
                if i < calculated_n_benefit
                else "Cost"
                for i in range(
                    len(calculated_criteria)
                )
            ],

            "R": alt_R.values,

            "Theta": alt_theta.values
        }
    )


    alt_display = (
        alt_df.copy()
    )


    for c in [
        "Weight",
        "R",
        "Theta"
    ]:

        alt_display[c] = (
            alt_display[c]
            .round(6)
        )


    st.markdown(
        "### Criterion Performance"
    )

    st.dataframe(
        alt_display,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # THETA BAR
    # --------------------------------------------------------

    fig_alt = px.bar(
        alt_df,
        x="Criterion",
        y="Theta",
        color="Theta",
        text="Theta",
        color_continuous_scale="Viridis",

        hover_data={
            "Weight": ":.8f",
            "R": ":.8f",
            "Theta": ":.8f"
        }
    )

    fig_alt.update_xaxes(
        title="Criterion"
    )

    fig_alt.update_yaxes(
        title="Weighted Score (θ)"
    )

    fig_alt.update_traces(
        texttemplate="%{y:.4f}",
        textposition="outside"
    )

    fig_alt = plot_layout(
        fig_alt,
        f"Criterion Performance — {selected_alt}"
    )

    fig_alt.update_layout(
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_alt,
        use_container_width=True
    )


    # --------------------------------------------------------
    # RADAR
    # --------------------------------------------------------

    radar = go.Figure()

    radar.add_trace(
        go.Scatterpolar(
            r=alt_theta.values.tolist(),

            theta=calculated_criteria,

            fill="toself",

            name=str(selected_alt),

            line=dict(
                color="#2563eb",
                width=3
            ),

            fillcolor="rgba(37,99,235,0.20)"
        )
    )


    radar.update_layout(
        template="plotly_white",

        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        font=dict(
            color="#111827"
        ),

        polar=dict(

            bgcolor="#ffffff",

            radialaxis=dict(
                title="θ",
                color="#111827",
                gridcolor="#d1d5db",
                linecolor="#64748b",
                showline=True
            ),

            angularaxis=dict(
                color="#111827",
                gridcolor="#e5e7eb"
            )
        ),

        title=dict(
            text=f"Alternative Profile — {selected_alt}",

            font=dict(
                color="#111827",
                size=20
            )
        ),

        margin=dict(
            l=70,
            r=70,
            t=80,
            b=70
        )
    )


    st.plotly_chart(
        radar,
        use_container_width=True
    )


# ============================================================
# TAB 5 — CRITERION COMPARISON
# ============================================================

with tab5:

    st.markdown(
        "### Compare Alternatives by Criterion"
    )

    selected_criteria = st.multiselect(
        "Select Criteria",
        calculated_criteria,

        default=calculated_criteria[
            :min(
                3,
                len(calculated_criteria)
            )
        ],

        key="selected_comparison_criteria"
    )


    if selected_criteria:

        comparison_df = (
            Theta_df[
                selected_criteria
            ]
            .copy()
        )

        comparison_df["Alternative"] = (
            comparison_df.index
        )

        comparison_long = (
            comparison_df
            .melt(
                id_vars="Alternative",
                var_name="Criterion",
                value_name="Theta"
            )
        )


        fig_comparison = px.bar(
            comparison_long,

            x="Alternative",
            y="Theta",

            color="Criterion",

            barmode="group",

            hover_data={
                "Theta": ":.8f"
            }
        )


        fig_comparison.update_xaxes(
            title="Alternative"
        )

        fig_comparison.update_yaxes(
            title="Weighted Score (θ)"
        )


        fig_comparison = plot_layout(
            fig_comparison,
            "Criterion-wise Alternative Comparison"
        )


        st.plotly_chart(
            fig_comparison,
            use_container_width=True
        )


    else:

        st.info(
            "Select at least one criterion to display the comparison."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SRP-MCDM • Original SRP calculation preserved • "
    "Display rounding does not alter calculation precision"
)