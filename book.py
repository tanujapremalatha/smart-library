import streamlit as st
import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
api = os.getenv("GROQ_API_KEY")
client=Groq(api_key=api)
st.title("Welcome to Smart Library")
name=st.text_input("Enter your name")
st.title(f"Hello {name}")
category_choice=st.radio("Choose a Library Section: ",options=["Course/Academic Textbooks","Leisure reading"],horizontal=True)
@st.cache_data
def load_data():
    df=pd.read_csv("book.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df
df=load_data()
if category_choice=="Course/Academic Textbooks":
    dataset = df[df["category"].astype(str).str.strip().str.lower() == "academic"]
else:
    dataset = df[df["category"].astype(str).str.strip().str.lower() == "leisure"]
search = st.text_input("Search for a book:", placeholder="Type any title...")
def recommendations(search,dataset):
    available_list = dataset["title"].dropna().tolist()[:30]
    if len(available_list) > 30:
        available_list = available_list[:30]
    prompt = f"""
    A user searched for the book "{search}", but it is currently out of stock.
    Here is a list of available books in our library:
    {", ".join(available_list)}

    Please recommend 1 to 3 books from the provided available list that are most similar or relevant to "{search}".
    Only recommend books that are present in the provided list. Keep the response friendly and concise.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="openai/gpt-oss-20b",)
    return response.choices[0].message.content
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
            with st.spinner("Finding similar available books for you..."):
                recommendations_1 = recommendations(search, dataset)
                st.info(f"**AI Recommendations:**\n\n{recommendations_1}")
    else:
        st.error(f"'{search}' is not in the library database.")
        with st.spinner("Finding similar available books for you..."):
            recommendations_1 = recommendations(search, dataset)
            st.info(f"**AI Recommendations:**\n\n{recommendations_1}")

    