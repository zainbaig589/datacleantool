import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Data Clean Tool Pro",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with blue and gold accents
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #f0e6d2;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: #f0e6d2;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    .stFileUploader>div>div>input {
        background-color: #1f1f1f;
        color: #f0e6d2;
    }
    .stDataFrame div {
        background-color: #0d1117 !important;
        color: #f0e6d2 !important;
    }
    h1, h2, h3, h4 {
        color: #ffbf00;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🧹 Data Clean Tool Pro")
st.subheader("Upload your CSV and clean your data effortlessly!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Load CSV
    df = pd.read_csv(uploaded_file)
    st.success("File loaded successfully!")
    
    st.markdown("### Raw Data Preview")
    st.dataframe(df.head())

    st.markdown("### Cleaning Options")
    
    # Remove duplicates
    remove_dup = st.checkbox("Remove duplicate rows")
    
    # Handle missing values
    missing_option = st.selectbox("Handle missing values", ["None", "Drop rows", "Fill with 0", "Fill with mean"])
    
    # Normalize column names
    normalize_cols = st.checkbox("Normalize column names (lowercase, remove spaces)")

    if st.button("Clean Data"):
        df_clean = df.copy()
        
        if remove_dup:
            df_clean = df_clean.drop_duplicates()
        
        if missing_option == "Drop rows":
            df_clean = df_clean.dropna()
        elif missing_option == "Fill with 0":
            df_clean = df_clean.fillna(0)
        elif missing_option == "Fill with mean":
            for col in df_clean.select_dtypes(include=np.number).columns:
                df_clean[col].fillna(df_clean[col].mean(), inplace=True)
        
        if normalize_cols:
            df_clean.columns = [c.strip().lower().replace(" ", "_") for c in df_clean.columns]
        
        st.success("Data cleaned successfully!")
        st.markdown("### Cleaned Data Preview")
        st.dataframe(df_clean.head())
        
        # Download button
        buffer = BytesIO()
        df_clean.to_csv(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="Download Cleaned CSV",
            data=buffer,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    st.markdown("### Quick Stats")
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        st.bar_chart(df[numeric_cols].describe().T['mean'])

