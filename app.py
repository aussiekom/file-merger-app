# pip install openpyxl
import pandas as pd
import streamlit as st
from PIL import Image
import zipfile
import base64
import os

# **Excel File Merger**

# Load and display the image
image = Image.open('excel.png')
st.image(image, use_column_width = True)


# Excel file merge function
def excel_file_merge(zip_file_name):
    df = pd.DataFrame()
    archive = zipfile.ZipFile(zip_file_name, 'r')
    with zipfile.ZipFile(zip_file_name, "r") as f:
        for file in f.namelist():
          xlfile = archive.open(file)
          if file.endswith('.xlsx'):
            # Add a note indicating the file name that this dataframe originates from
            df_xl = pd.read_excel(xlfile, engine='openpyxl')
            df_xl['Note'] = file
            # Appends content of each Excel file iteratively
            df = df.append(df_xl, ignore_index=True)
    return df

# Upload CSV data
with st.sidebar.header('1. Upload your ZIP file'):
    uploaded_file = st.sidebar.file_uploader("Excel-containing ZIP file", type=["zip"])
    st.sidebar.markdown("""
[Example ZIP input file](https://github.com/dataprofessor/excel-file-merge-app/raw/main/nba_data.zip)
""")

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged File as CSV</a>'
    return href

def xldownload(df):
    df.to_excel('data.xlsx', index=False)
    data = open('data.xlsx', 'rb').read()
    b64 = base64.b64encode(data).decode('UTF-8')
    #b64 = base64.b64encode(xl.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/xls;base64,{b64}" download="merged_file.xlsx">Download Merged File as XLSX</a>'
    return href

# Main panel
if st.sidebar.button('Submit'):
    #@st.cache
    df = excel_file_merge(uploaded_file)
    st.header('**Merged data**')
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)
    st.markdown(xldownload(df), unsafe_allow_html=True)
else:
    st.info('Awaiting for ZIP file to be uploaded.')


# author note
st.markdown('''
by Evgeniia Komarova [LinkedIn](https://www.linkedin.com/in/evgeniia-komarova/) [GitHub](https://github.com/aussiekom)
---
''')
