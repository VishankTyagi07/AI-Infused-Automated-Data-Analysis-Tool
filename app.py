import streamlit as st
import pandas as pd

from profiling.profiler import (profile_dataset, generate_profile_report)
from cleaner.cleaner import clean_dataset
from sql.sql_generator import generate_sql_queries
from visualization.visual_assets import generate_visualizations
from visualization.exporter import export_dashboard_html
from ai.rule_based_summary import (
    generate_dataset_summary,
    cleaning_process_summary,
    generate_cleaning_result_summary,
    generate_profile_summary,
    generate_sql_summary,
    generate_viz_summary,   
)

st.set_page_config(
    page_title="Automated Data Analysis Tool",
    layout="wide"
)
# Session state initialization
defaults = {
    "active_action": None,
    "show_cleaning_summary": False,
    "cleaning_completed": False,
    "cleaned_df": None,
    "cleaning_result_summary": None,
    "current_file_name": None,
    "profile_report_html": None,
    "show_profile_summary": False,
    "profile_completed": False,
    "sql_queries": None,
    "show_sql_summary": False,
    "sql_completed": False,
    "show_viz_summary": False,
    "viz_completed": False,
    "viz_figures": None,
    "viz_dashboard_html": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: black;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    /* File uploader */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #4a90e2;
        padding: 1.25rem;
        border-radius: 12px;
        background-color: black;
    }

    /* Summary card */
    .summary-card {
        background-color: black;
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 1.05rem;
        line-height: 1.65;
        border: 1px solid #e0e0e0;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        padding: 0.65rem 1rem;
        font-size: 1rem;
        font-weight: 500;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #357abd;
        color: white;
    }
    .app-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9rem;
        border-top: 1px solid #e0e0e0;
        z-index: 9999;
        background-color: #1e1e1e;
        color: #e0e0e0;
    }

    .app-footer a {
        color: #1f4fd8;
        text-decoration: none;
        margin: 0 8px;
        font-weight: 500;
    }

    .app-footer a:hover {
        text-decoration: underline;
    }

    section.main > div {
        padding-bottom: 70px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div class='main-title'>Automated Data Analysis Tool</div>",
    unsafe_allow_html=True
)


left, center, right = st.columns([1, 2, 1])

with center:
    st.markdown(
        "<div class='section-title'>Upload Dataset</div>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        label_visibility="collapsed"
    )


if uploaded_file is not None:
    if uploaded_file.name != st.session_state["current_file_name"]:
        st.session_state["current_file_name"] = uploaded_file.name
        st.session_state["active_action"] = None
        st.session_state["current_file_name"] = uploaded_file.name
        st.session_state["show_cleaning_summary"] = False
        st.session_state["cleaning_completed"] = False
        st.session_state["cleaned_df"] = None
        st.session_state["cleaning_result_summary"] = None
        st.session_state["show_profile_summary"] = False
        st.session_state["profile_completed"] = False
        st.session_state["profile_report_html"] = None
        st.session_state["show_viz_summary"] = False
        st.session_state["viz_completed"] = False
        st.session_state["viz_figures"] = None

    df = pd.read_csv(uploaded_file)

    # Profile dataset
    metadata = profile_dataset(df)

    # Generate rule-based summary
    summary = generate_dataset_summary(metadata)

    st.divider()

    left, center, right = st.columns([1, 3, 1])

    with center:
        st.markdown(
            "<div class='section-title'>Dataset Summary</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='summary-card'>{summary.replace(chr(10), '<br>')}</div>",
            unsafe_allow_html=True
        )

    st.divider()


    st.markdown(
        "<div class='section-title'>Actions</div>",
        unsafe_allow_html=True
    )

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        if st.button("Profile Data", width="stretch"):
            st.session_state["active_action"] = "profile"
            st.session_state["show_profile_summary"] = True
            st.session_state["profile_completed"] = False

    with b2:
        if st.button("Clean Dataset", width="stretch"):
            st.session_state["active_action"] = "clean"
            st.session_state["show_cleaning_summary"] = True
            st.session_state["cleaning_completed"] = False

    with b3:
        if st.button("Generate SQL Queries", width="stretch"):
            st.session_state["active_action"] = "sql"
            st.session_state["show_sql_summary"] = True
            st.session_state["sql_completed"] = False

    with b4:
        if st.button("Visualize Data", width="stretch"):
            st.session_state["active_action"] = "visualize"
            st.session_state["show_viz_summary"] = True
            st.session_state["viz_completed"] = False

    if st.session_state["active_action"] == "clean":

        # ---- Pre-clean AI explanation
        if st.session_state["show_cleaning_summary"] and not st.session_state["cleaning_completed"]:
            st.markdown("### AI Explanation (Before Cleaning)")
            st.info(cleaning_process_summary(metadata))

            if st.button("Proceed with Cleaning", width="stretch"):
                with st.spinner("Cleaning dataset..."):
                    cleaned_df = clean_dataset(df)

                st.session_state["cleaned_df"] = cleaned_df
                st.session_state["cleaning_completed"] = True
                st.session_state["show_cleaning_summary"] = False

                st.session_state["cleaning_result_summary"] = (
                    generate_cleaning_result_summary(df, cleaned_df)
                )

                st.success("Dataset cleaned successfully.")

        # ---- Post-clean AI log
        if st.session_state["cleaning_completed"]:
            st.markdown("### AI Cleaning Log (What Changed)")
            st.info(st.session_state["cleaning_result_summary"])

            st.markdown("### Preview of Cleaned Dataset")

            st.dataframe(
                st.session_state["cleaned_df"],
                width="stretch",
                height=400
            )
            csv = st.session_state["cleaned_df"].to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Cleaned Dataset",
                data=csv,
                file_name="cleaned_dataset.csv",
                mime="text/csv",
                width="stretch",
            )
    
    if st.session_state["active_action"] == "profile":

        # ---- Pre-profile explanation
        if st.session_state["show_profile_summary"] and not st.session_state["profile_completed"]:
            st.markdown("### AI Explanation (Before Profiling)")
            st.info(generate_profile_summary(metadata))

            if st.button("Proceed with Profiling", width="stretch"):
                with st.spinner("Generating profiling report..."):
                    html_report = generate_profile_report(df)

                st.session_state["profile_report_html"] = html_report
                st.session_state["profile_completed"] = True
                st.session_state["show_profile_summary"] = False

                st.success("Profiling report generated successfully.")

        # ---- Post-profile AI log + download
        if st.session_state["profile_completed"]:
            st.markdown("### AI Profiling Log")
            st.info(
                "The profiling report summarizes dataset structure, distributions, "
                "missing values, and potential data quality issues. "
                "Use it to visually inspect patterns and anomalies."
            )

            st.download_button(
                label="Download Profiling Report (HTML)",
                data=st.session_state["profile_report_html"],
                file_name="profiling_report.html",
                mime="text/html",
                width="stretch"
            )
    
    if st.session_state["active_action"] == "sql":

        table_name = st.text_input("Table name", value="dataset")
        sql_dialect = st.selectbox("SQL Engine", ["ANSI", "PostgreSQL", "MySQL"])

        if st.session_state["show_sql_summary"] and not st.session_state["sql_completed"]:
            st.markdown("### AI Explanation (Before SQL Generation)")
            st.info(generate_sql_summary(metadata))

            if st.button("Proceed with SQL Generation", width="stretch"):
                sql_text = generate_sql_queries(
                    metadata,
                    table_name=table_name,
                    dialect=sql_dialect
                )
                st.session_state["sql_queries"] = sql_text
                st.session_state["sql_completed"] = True
                st.session_state["show_sql_summary"] = False

                st.success("SQL queries generated successfully.")

        if st.session_state["sql_completed"]:
            st.markdown("### AI SQL Log")
            st.info(
                f"Generated SQL for **{sql_dialect}** using table name **{table_name}**. "
                "Includes schema, missing value checks, and EDA queries."
            )

            st.code(st.session_state["sql_queries"], language="sql")

            st.download_button(
                "Download SQL File",
                data=st.session_state["sql_queries"],
                file_name="eda_queries.sql",
                mime="text/plain",
                width="stretch"
            )

    if st.session_state["active_action"] == "visualize":

        if st.session_state["show_viz_summary"] and not st.session_state["viz_completed"]:
            st.markdown("### AI Explanation (Before Visualization)")
            st.info(generate_viz_summary(st.session_state["cleaned_df"] or df))

            if st.button("Generate Visualizations", width="stretch"):
                with st.spinner("Generating visualizations..."):
                    figs = generate_visualizations(
                        st.session_state["cleaned_df"] or df
                    )
                st.session_state["viz_figures"] = figs
                st.session_state["viz_dashboard_html"] = export_dashboard_html(figs)
                st.session_state["viz_completed"] = True
                st.session_state["show_viz_summary"] = False

                st.success("Visual dashboard generated successfully.")

        if st.session_state["viz_completed"]:
            st.markdown("### Visual Insights")

            for fig in st.session_state["viz_figures"].values():
                st.plotly_chart(fig, width="stretch")
            st.download_button(
                label="Download Visualization Dashboard (HTML)",
                data=st.session_state["viz_dashboard_html"],
                file_name="visualization_dashboard.html",
                mime="text/html",
                width="stretch"
            )
st.markdown(
    """
    <div class="app-footer">
        © 2026 <strong>Vishank Tyagi</strong> ·
        <a href="https://github.com/VishankTyagi07" target="_blank">GitHub</a> ·
        <a href="https://www.linkedin.com/in/vishank-t/" target="_blank">LinkedIn</a> ·
        <a href="https://mail.google.com/mail/?view=cm&to=tyagivishank1234@gmail.com" target="_blank">Email</a>
    </div>
    """,
    unsafe_allow_html=True
)