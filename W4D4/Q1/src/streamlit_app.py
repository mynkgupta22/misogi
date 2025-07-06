import streamlit as st
import requests
import json

# Configure page
st.set_page_config(
    page_title="HR Knowledge Assistant",
    page_icon="👩‍💼",
    layout="wide"
)

# Constants
API_URL = "http://localhost:8000"

def main():
    st.title("HR Knowledge Assistant 👩‍💼")
    st.write("Upload HR documents and ask questions about company policies!")

    # File upload section
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader(
            "Upload HR Document",
            type=['pdf', 'docx'],
            help="Upload PDF or Word documents containing HR policies"
        )
        
        if uploaded_file:
            with st.spinner("Processing document..."):
                files = {"file": uploaded_file}
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.success("Document processed successfully!")
                else:
                    st.error(f"Error: {response.text}")

    # Query section
    st.header("Ask Questions")
    query = st.text_input(
        "What would you like to know about company policies?",
        placeholder="E.g., What's the process for requesting parental leave?"
    )

    if query:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"text": query}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display answer
                    st.markdown("### Answer")
                    st.write(result["answer"])
                    
                    # Display sources if available
                    if result.get("sources"):
                        st.markdown("### Sources")
                        for source in result["sources"]:
                            st.info(f"Source: {source}")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to the server: {str(e)}")

    # Instructions
    with st.sidebar:
        st.markdown("### How to use")
        st.markdown("""
        1. Upload HR documents using the file uploader above
        2. Ask questions about company policies in the main panel
        3. Get instant answers with source citations
        """)
        
        st.markdown("### Sample Questions")
        st.markdown("""
        - How many vacation days do I get?
        - What's the work from home policy?
        - How do I request sick leave?
        - What are the benefits offered?
        """)

if __name__ == "__main__":
    main() 