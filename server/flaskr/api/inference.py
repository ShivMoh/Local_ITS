import socket
import json
from typing import Dict
import os
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig
import numpy as np
from datasets import load_dataset
from typing import Dict, List
import torch
from dotenv import load_dotenv
from huggingface_hub import login, logout, get_token, snapshot_download
from dotenv import load_dotenv
import gc
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, stream_with_context
)
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

# from flaskr.db import get_db

bp = Blueprint('inference', __name__, url_prefix='/inference')

@bp.route("/initiate", methods=["GET", "POST"])
def initiate_udp_session() -> Dict:
    os.environ["session_id"] = "1"
    os.environ["active"] = "True"

    return {
        "success" : True,
        "message" : "Session Initiated"
    }

@bp.route("/load", methods=["GET", "POST"])
def load_model() -> Dict:
    global model, tokenizer

    model_name = "meta-llama/Llama-2-7b-chat-hf"

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4"
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config = bnb_config,
        device_map={"":0},
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '<PAD>'})

    return {
        "success" : True,
        "message" : "Model Loaded Successfully",
        "status" : 200
    }

@bp.route("/query", methods=['POST'])
def query() -> Dict:
    global model, tokenizer

    if "model" not in globals() or "tokenizer" not in globals():
        return {
            "success" : False,
            "message" : "Please load the model first",
            "status" : 200
        }

    prompt = request.json["prompt"]

    print(request.json)
    inputs = tokenizer(prompt, return_tensors='pt')

    if model.device.type == "cuda":
        inputs.to(model.device)

    if request.json["new"] == True:
        outputs = model.generate(
            inputs.input_ids,
            temperature=0.7,  # Adjust for more/less randomness
            top_k=30,         # Adjust for more/less diversity
            top_p=0.9,        # Nucleus sampling
            repetition_penalty=1.2,  # Penalize repetition
            do_sample=True,    # Enable sampling (not just greedy decoding)
            max_new_tokens=250
        )
    else: outputs = model.generate(
      inputs.input_ids,
      do_sample=True,
      max_new_tokens=250
    )

    text_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # free unused memory
    torch.cuda.empty_cache()

    return {
        "success" : True,
        "message" : text_output,
        "status" : 200
    }

@bp.route("/free", methods = ["GET", "POST"])
def free_memory() -> Dict:
    if "model" not in globals() and not "tokenizer" in globals():
        return {
            "success" : True,
            "message" : "No memory to free",
            "status" : 200
        }

    try:
        global model, tokenizer
        del model, tokenizer
        gc.collect()
        torch.cuda.empty_cache()

        return {
            "success" : True,
            "message" : "Memory successfully freed",
            "status" : 200
        }
    except:
        return {
            "success" : False,
            "message" : "Unknown error occurred when freeing memory",
            "status" : 500
        }

@bp.route("/some", methods= ["GET", "POST"])
def streamed_response():
    import time
    def generate():
        for x in range(1, 10):
            yield "hello"
    return generate()

