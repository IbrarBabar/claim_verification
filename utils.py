import os
import glob
import logging
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import AzureChatOpenAI
from tqdm import tqdm
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
import os
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import yaml

# Load configuration files
def load_config(config_path):
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)
    
    
def initialize_embeddings(model_name):
    """Initialize the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=model_name)


def create_embeddings(embeddings_dir, model_name):
    """Create a FAISS database from PDF files, with citation metadata."""
    hf_embed = initialize_embeddings(model_name)
    file_list = glob.glob("medical_artical/*.pdf")
#     file_list = glob.glob("vector_store_articles_currupt/*.pdf")
    documents = []

    # Load each PDF file and extract text with metadata
    for idx, file in enumerate(tqdm(file_list, desc="Reading PDFs", ncols=100)):
        # print(f"Processing file {idx+1}/{len(file_list)}: {os.path.basename(file)}...")
        loader = PyPDFLoader(file)
        pages = loader.load_and_split()

        # Add each page as a separate document with metadata for citation
        for page in pages:
            # print(f"  Processing page from {os.path.basename(file)}...")
            # Add the source filename and page number as metadata
            metadata = {
                "source": os.path.basename(file),
                "page": page.metadata.get("page", 0)
            }
            documents.append(Document(page_content=page.page_content, metadata=metadata))

    # Create the FAISS database from the documents and embeddings
    print("Creating FAISS database from documents...")
    db = FAISS.from_documents(documents, embedding=hf_embed)

    # Save the FAISS database locally
    db.save_local(embeddings_dir)
    print("Creating embeddings with metadata completed.")
    return db


def load_embeddings(embeddings_dir, model_name):
    """Load the existing FAISS database, allowing dangerous deserialization."""
    hf_embed = initialize_embeddings(model_name)
    try:
        db = FAISS.load_local(embeddings_dir, hf_embed, allow_dangerous_deserialization=True)
        print("Loaded the embeddings with metadata.")
        return db
    except Exception as e:
        print(f"Failed to load embeddings: {e}")
        raise

        
def initialize_vector_store(embeddings_dir, model_name):
    """Initialize or load the FAISS database."""
    if not os.path.exists(embeddings_dir):
        print("Creating new embeddings from PDF files...")
        return create_embeddings(embeddings_dir, model_name)
    else:
        print("Loading existing embeddings...")
        return load_embeddings(embeddings_dir, model_name)

    
def initialize_qa_chain(llm, prompt_template):
    """Initialize the QA chain with the provided language model and prompt template."""
    return load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt_template)


def create_embeddings(model_name = "sentence-transformers/all-mpnet-base-v2"):
    embeddings_dir = os.path.join(os.getcwd(), "medical_local_vector_store_embeddings_faiss")
    model_name = "sentence-transformers/all-mpnet-base-v2"
    # Initialize vector store (create or load)
    print("Initializing vector store...")
    db = initialize_vector_store(embeddings_dir, model_name)
    print("================================================================")
    return db
    
    
    
def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


def create_qa_prompt_template(instruction_text):
    return PromptTemplate(
        input_variables=["context", "question"],
        template=instruction_text + "\n\nContext: {context}\n\nQuestion: {question}"
    )



def instantiate_openai_model(api_key, model_name="gpt-4o-mini", temperature=0.7, max_tokens=None, timeout=None):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        api_key=api_key
    )


# def initialize_qa_chain(llm, qa_prompt_template):
#     return load_qa_chain(llm, qa_prompt_template)




def ask_question(db, chain, question, num_references=1):
    """Ask a question and get a response using the FAISS vector store and OpenAI, with citations."""
    # Retrieve a specified number of similar documents from the FAISS database
    docs_db = db.similarity_search(question, k=num_references)

    if not docs_db:
        return "No similar documents found."

    # Prepare the context by joining document contents with metadata for citation
    context = "\n\n".join(
        f"Source: {doc.metadata['source']}, Page: {doc.metadata.get('page', 'N/A')}\n{doc.page_content}"
        for doc in docs_db
    )

    # Call the QA chain with the retrieved documents
    response = chain({
        "input_documents": docs_db,
        "question": question,
        "context": context,
        "existing_answer": ""
    }, return_only_outputs=True)
    
    if response['output_text'] == "The answer is not in the knowledge base.":
        return response['output_text']
    # Format the response to include citations for each source document
    response_text = response['output_text'] + "\n\nCitations:\n"
    citations = "\n".join(
        f"- Source: {doc.metadata['source']}, Page: {doc.metadata.get('page', 'N/A')}"
        for doc in docs_db
    )
    response_text += citations

    return response_text

