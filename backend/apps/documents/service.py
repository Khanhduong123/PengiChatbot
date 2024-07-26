import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader

from apps.documents.config import document_config
from apps.documents.exceptions import ErrorDelete, ErrorFormat, ErrorUpload
from apps.documents.schemas import DocumentsQdrant

from utils.logging import LOGGER

from cryptography.hazmat.primitives.ciphers.algorithms import ARC4

async def save_document(file):
    # Construct the full file path based on the settings
    file_path = document_config.UPLOAD_DIR + file.filename

    LOGGER.info(file_path)
    # Read the contents of the uploaded file asynchronously
    contents = await file.read()
    LOGGER.info(contents)
    # Write the uploaded contents to the specified file path
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path


def read_split_document(file_path, document_id):
    # Extract the document name from the file path
    document_name = os.path.basename(file_path)
    LOGGER.info(f"document_name: {document_name}")
    # Choose the appropriate loader
    loader = (
        PyPDFLoader(file_path)
        if file_path.lower().endswith(".pdf")
        else Docx2txtLoader(file_path)
    )

    # Load and split the document using the selected loader
    documents = loader.load_and_split()

    # Set up tokenizer and text splitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=document_config.CHUNK_SIZE,
        chunk_overlap=document_config.CHUNK_OVERLAP,
    )

    # Split the documents into chunks and create a list of dictionaries
    list_chunks = [
        {
            "document_id": document_id,
            "content": doc.page_content,
            "document_name": document_name,
            "page": doc.metadata["page"] + 1 if "page" in doc.metadata else 0,
        }
        for doc in text_splitter.split_documents(documents)
    ]

    return list_chunks


class DocumentService:
    def __init__(self, document_search):
        self.document_search = document_search

    async def upload_document(self, document_id, file):
        # Determine the file type and choose the appropriate loader
        if not file.filename.lower().endswith((".pdf", ".docx")):
            raise ErrorFormat

        try:
            file_path = await save_document(file=file)

            list_chunks = read_split_document(
                file_path=file_path, document_id=document_id
            )
            LOGGER.info(f"list_chunks: {list_chunks}")
            self.document_search.add_patching_points(list_chunks=list_chunks)

        except Exception as e:
            LOGGER.info(f"document_id: {document_id}")
            DocumentsQdrant.delete_doc_by_id(document_id)
            LOGGER.info(f"Import Document failed! {file_path}")
            LOGGER.error(f"Error: {e}")

            raise ErrorUpload

    async def delete_document(self, document_id):
        try:
            await self.document_search.delete_document(document_id=document_id)

        except Exception as e:
            LOGGER.info(f"Delete Document failed! {document_id}")
            LOGGER.error(f"Error: {e}")

            raise ErrorDelete