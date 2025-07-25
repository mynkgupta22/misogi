from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader

class DocumentProcessor:
    def __init__(self):
        self.text_splitter =RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200, separator = ["\n","\n\n", " ","."])

    def process_uploaded_files(self,uploaded_file):
        with open(f"temp_{uploaded_file.name}","wb") as f:
            f.write(uploaded_file.getvalue())

        file_path = f"temp_{uploaded_file.name}"
        if(uploaded_file.name.endswith("pdf")):
            loader = PyPDFLoader(file_path)
        elif(uploaded_file.name.endswith("docx")):
            loader = Docx2txtLoader(file_path)
        else:
            st.error("Unsupported file")
            return []

        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)

        return [chunk.page_content for chunk in chunks]