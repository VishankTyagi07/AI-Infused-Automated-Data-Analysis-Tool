import streamlit as st
import pandas as pd

from profiling.profiler import profile_dataset
from ai.rule_based_summary import generate_dataset_summary


st.set_page_config(
    page_title="Automated Data Analysis Tool",
    layout="wide"
)

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
        st.button("Profile Data", use_container_width=True)

    with b2:
        st.button("Clean Dataset", use_container_width=True)

    with b3:
        st.button("Generate SQL Queries", use_container_width=True)

    with b4:
        st.button("Visualize Data", use_container_width=True)
