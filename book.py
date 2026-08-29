import streamlit as st
import pandas as pd
from groq import Groq
st.title("Hello,Welcome to Smart Library")
name=st.text_input("Enter your name")
st.title(f"Hello {name}")
category_choice=st.radio("Choose a Library Section: ",options=["Course/Academic Textbooks","Leisure reading"],horizontal=True)
@st.cache_data
def load_data():
    df=pd.read_csv("book.csv")
    df.columns=df.columns.str.strip()
    return df
df=load_data()
if category_choice=="Course/Academic Textbooks":
    dataset = df[df["category"].astype(str).str.strip().str.lower() == "academic"]
else:
    dataset = df[df["category"].astype(str).str.strip().str.lower() == "leisure"]
search= st.text_input("Search for a book:", placeholder="Type any title...")
if search:
    # Fixed: added .str.contains(search.strip().lower(), regex=False)
    matches = dataset[
        dataset["title"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.contains(search.strip().lower(), regex=False)
    ]
    if not matches.empty:
        quantity = matches["quantity"].values[0]
        title = matches["title"].values[0]

        if quantity > 0:
            st.success(f"{title} is available! ({quantity} copies left)")
        else:
            st.warning(f"{title} is out of stock.")
    else:
        st.error(f"'{search}' is not in the library database.")