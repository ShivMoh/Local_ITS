from typing import Dict, List
import torch
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, TrainingArguments, TextIteratorStreamer
from peft import LoraConfig
from trl import SFTTrainer
import os
from urllib.request import urlretrieve
import numpy as np
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model = None
tokenizer = None
huggingface_embeddings = None
vectorstore = None
docs = None

def load_model(model_id = "meta-llama/Llama-2-7b-chat-hf"):
    global model, tokenizer

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map={"": 0},
        attn_implementation="flash_attention_2",
    )

    print(model.device)

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '<PAD>'})

    return [tokenizer, model]


def chat(prompt):

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    # repetition_penalty=1.2, top_k = 10, top_p = 0.9, temperature=0.6, do_sample=True, max_new_tokens=1024
    outputs = model.generate(input_ids, max_new_tokens=1024)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def create_full_context(documents : list) -> str:
  return "\n".join([doc.page_content for doc in documents])

def load_embeddings():
    global huggingface_embeddings
    huggingface_embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",  # alternatively use "sentence-transformers/all-MiniLM-l6-v2" for a light and faster experience.
        model_kwargs={'device':'cuda'},
        encode_kwargs={'normalize_embeddings': True}
    )

    return huggingface_embeddings

def load_files():
    loader = PyPDFDirectoryLoader("/home/shivesh/Documents/python/its_solution/local_its/server/flaskr/storage/pdfs")

    docs_before_split = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 700,
        chunk_overlap  = 50,
    )

    docs_after_split = text_splitter.split_documents(docs_before_split)

    return docs_after_split

def init_vectorstore(docs):
    global vectorstore
    vectorstore = FAISS.from_documents(docs, huggingface_embeddings)
    return vectorstore

def find_content():
    global vectorstore
    results = vectorstore.similarity_search("What is a operating system", k=3)
    return results

COUNTER = 0
import os
def write_content(content_type, arr, number=True):
    global COUNTER
    os.makedirs("./generated", exist_ok=True)
    if number:
        file_name = f"./generated/{content_type}_{COUNTER}.txt"  # Ensure it has an extension
    else:
        file_name = f"./generated/{content_type}.txt"  # Ensure it has an extension

    with open(file_name, "a") as f:
        for content in arr:
            f.write(content + "\n")
        
        f.close()
    
    COUNTER+=1

def load_file(file_name):  
    file_name = f"./generated/{file_name}.txt"  # Ensure it has an extension
    with open(file_name, "r") as f:
        content = f.readlines()
        f.close()
    return content
    