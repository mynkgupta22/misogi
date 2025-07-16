import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import plotly.express as px

# Load environment variables
load_dotenv()

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

def init_session_state():
    """Initialize session state variables"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "current_doc_id" not in st.session_state:
        st.session_state.current_doc_id = None

def signup(email: str, password: str) -> bool:
    """Handle user signup"""
    try:
        response = requests.post(
            f"{API_URL}/api/v1/auth/register",
            json={"email": email, "password": password}
        )
        if response.status_code == 201:
            st.success("Signup successful! Please login.")
            return True
        st.error(f"Signup failed: {response.json().get('detail', 'Unknown error')}")
        return False
    except Exception as e:
        st.error(f"Signup failed: {str(e)}")
        return False

def login(email: str, password: str) -> bool:
    """Handle user login"""
    try:
        response = requests.post(
            f"{API_URL}/api/v1/auth/jwt/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.current_page = "documents"
            return True
        return False
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return False

def render_signup_page():
    """Render the signup page"""
    st.title("Research Assistant Signup")
    
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long!")
            else:
                if signup(email, password):
                    st.session_state.current_page = "login"
                    st.rerun()

    if st.button("Already have an account? Login"):
        st.session_state.current_page = "login"
        st.rerun()

def render_login_page():
    """Render the login page"""
    st.title("Research Assistant Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if login(email, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.current_page = "signup"
        st.rerun()

def fetch_documents():
    """Fetch user's documents"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/api/v1/my-documents", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Failed to fetch documents: {str(e)}")
        return []

def upload_document(title: str, file):
    """Upload a new document"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        files = {"file": file}
        data = {"title": title}
        response = requests.post(
            f"{API_URL}/api/v1/documents",
            headers=headers,
            data=data,
            files=files
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return False

def export_document(doc_id: int, format: str):
    """Export document in various formats"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(
            f"{API_URL}/api/v1/documents/{doc_id}/export?format={format}",
            headers=headers
        )
        return response.content if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Export failed: {str(e)}")
        return None

def share_document(doc_id: int, platform: str):
    """Share document to various platforms"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            f"{API_URL}/api/v1/documents/{doc_id}/share",
            headers=headers,
            json={"platform": platform}
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Sharing failed: {str(e)}")
        return False

def fetch_document(doc_id: int):
    """Fetch a specific document"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/api/v1/documents/{doc_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Failed to fetch document: {str(e)}")
        return None

def render_document_viewer():
    """Render the document viewer page"""
    if not st.session_state.current_doc_id:
        st.error("No document selected")
        return

    document = fetch_document(st.session_state.current_doc_id)
    if not document:
        st.error("Failed to load document")
        return

    # Document header
    st.title(document["title"])
    
    # Action buttons in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        export_format = st.selectbox("Export As:", ["pdf", "docx", "md"])
        if st.button("Export"):
            content = export_document(st.session_state.current_doc_id, export_format)
            if content:
                st.download_button(
                    f"Download {export_format.upper()}",
                    content,
                    file_name=f"{document['title']}.{export_format}"
                )
    
    with col2:
        platform = st.selectbox("Share To:", ["notion", "slack", "teams"])
        if st.button("Share"):
            if share_document(st.session_state.current_doc_id, platform):
                st.success(f"Shared to {platform} successfully!")
    
    with col3:
        if st.button("Back to Documents"):
            st.session_state.current_page = "documents"
            st.session_state.current_doc_id = None
            st.rerun()

    # Document content
    st.markdown("---")
    if "content" in document and document["content"]:
        st.markdown(document["content"])
    else:
        st.info("No content available for this document")

def render_documents_page():
    """Render the documents page"""
    st.title("My Documents")
    
    # Upload new document
    with st.expander("Upload New Document"):
        with st.form("upload_form"):
            title = st.text_input("Document Title")
            file = st.file_uploader("Choose a file")
            submit = st.form_submit_button("Upload")
            
            if submit and file and title:
                if upload_document(title, file):
                    st.success("Document uploaded successfully!")
                    st.rerun()
    
    # List documents
    documents = fetch_documents()
    if documents:
        df = pd.DataFrame(documents)
        
        # Make the title column clickable
        def make_clickable(title, doc_id):
            return f'<a href="#" onclick="handle_doc_click({doc_id})">{title}</a>'
        
        df["title"] = df.apply(lambda x: make_clickable(x["title"], x["id"]), axis=1)
        
        st.dataframe(
            df[["title", "file_type", "created_at"]],
            column_config={
                "created_at": st.column_config.DatetimeColumn("Created At"),
                "title": st.column_config.Column("Title", help="Click to view document")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Document selection for viewing
        selected_doc = st.selectbox("Select document to view:", df["title"].tolist())
        if selected_doc and st.button("View Document"):
            doc_id = df[df["title"] == selected_doc]["id"].iloc[0]
            st.session_state.current_doc_id = doc_id
            st.session_state.current_page = "viewer"
            st.rerun()
    else:
        st.info("No documents found. Upload your first document!")

def main():
    """Main application"""
    init_session_state()
    
    # Sidebar navigation
    if st.session_state.token:
        if st.sidebar.button("Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.current_page = "login"
            st.rerun()
    
    # Page routing
    if st.session_state.current_page == "signup":
        render_signup_page()
    elif st.session_state.current_page == "login" and not st.session_state.token:
        render_login_page()
    elif st.session_state.current_page == "viewer" and st.session_state.token:
        render_document_viewer()
    elif st.session_state.token:
        render_documents_page()

if __name__ == "__main__":
    main() 