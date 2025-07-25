import streamlit as st


st.set_page_config(page_title="Human Resource knowledge base", page_icon="🚞", layout="wide")
st.title("Human Resource Q&A Bot")

tab1, tab2 = st.tabs(["Upload Document", "Chat with your virtual AI assistant"])

with tab1:
    st.header("Upload your Document")

    uploaded_file = st.file_uploader(type=["pdf", "docx", "txt"], accept_multiple_files=True)

    if uploaded_file and st.button("Upload"):
        with st.spinner("Uploading..."):
            for file in uploaded_file:
                chunks = st.session


with tab2:
    st.header("Ask your questions here")