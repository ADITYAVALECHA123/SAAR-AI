from langchain_community.document_loaders import PyPDFLoader
def load_pdf(file_path):
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        if not docs:
            raise ValueError("PDF is empty or unreadable")
        return docs
    except Exception as e:
        raise Exception(
            f"Failed to process PDF: {str(e)}"
        )