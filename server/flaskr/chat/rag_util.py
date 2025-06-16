from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from typing import Dict, List

from langchain_core.vectorstores import VectorStore

path_to_file = ""
vectorstore = None
embeddings = None
def load_document_chunks(path_to_file) -> List[Document]:
  loader = PyPDFDirectoryLoader(path_to_file)
  docs_before_split : List[Document] = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 700,
      chunk_overlap  = 50,
  )

  docs_after_split  : List[Document] = text_splitter.split_documents(docs_before_split)

  return docs_after_split

def load_embeddings(model_name = "BAAI/bge-small-en-v1.5", model_args = {"device" : "cuda"}, encode_args = {"normalize_embeddings" : True}) -> HuggingFaceBgeEmbeddings:
   return HuggingFaceBgeEmbeddings(
    model_name=model_name,  # alternatively use "sentence-transformers/all-MiniLM-l6-v2" for a light and faster experience.
    model_kwargs={'device':'cuda'},
    encode_kwargs={'normalize_embeddings': True}
  )

def create_vectorstore(docs : List[Document], embeddings : HuggingFaceBgeEmbeddings) -> VectorStore:
  global vectorstore
  vectorstore = FAISS.from_documents(docs, embeddings)
  return vectorstore

def retrieve_documents(prompt : str, vectorstore : VectorStore, validate=True, number_of_docs: int=3) -> List[Document]:
  # this will rank the list of relevant docs from most relevant to least relevant
  if validate:
    results = vectorstore.similarity_search_with_score(prompt, k=number_of_docs)
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    filtered_docs = [doc for doc, score in sorted_results if score >= 0.0]
    return filtered_docs
  # this will just return the docs
  else:
    return vectorstore.similarity_search(prompt, k=number_of_docs)


# load_document_chunks("../storage/pdfs/")
