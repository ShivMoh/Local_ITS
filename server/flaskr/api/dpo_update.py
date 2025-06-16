from typing import Dict
import os
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig
import numpy as np
from datasets import load_dataset
from typing import Dict, List
import torch
from huggingface_hub import login, logout, get_token, snapshot_download
from dotenv import load_dotenv
import gc
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, stream_with_context
)
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from trl import DPOConfig, DPOTrainer

# from flaskr.db import get_db

bp = Blueprint('update', __name__, url_prefix='/update')

@bp.route("/reload_model", methods=["GET", "POST"])
def reload_model():
  global model, tokenizer

  model_name = "meta-llama/Llama-2-7b-chat-hf"

  tokenizer = AutoTokenizer.from_pretrained(model_name)
  tokenizer.pad_token = tokenizer.eos_token

  bnb_config = BitsAndBytesConfig( load_in_4bit=True,
      bnb_4bit_compute_dtype=torch.bfloat16,
      bnb_4bit_quant_type="nf4",
  )

  model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map={"": 0}
  )

  return {
      "success" : True,
      "message" : "Session Initiated"
  }


@bp.route("/get_update_data", methods=["GET", "POST"]):
def get_update_data():
  global update_dataset
  dataset = load_dataset("HumanLLMs/Human-Like-DPO-Dataset", split="train")
  update_dataset = dataset.select(range(32))

  return {
      "success" : True,
      "message" : "Session Initiated"
  }


@bp.route("/update", methods=["GET", "POST"])
def update_model():
  global model, update_dataset, tokenizer
  peft_config = LoraConfig(
    lora_alpha=128, # higher means stronger adaption but increases instability
    lora_dropout=0.05, # prevents overfitting, useful for small datasets
    r=8, # rank of the LoRA adaption matrices, lower rank means fewer trainable params
    bias="none", # no bias
    task_type="CAUSAL_LM",
    target_modules=[
      "q_proj",
      "o_proj",
      "k_proj",
      "v_proj",
      "gate_proj",
      "up_proj",
      "down_proj"
    ],
  )

  model = get_peft_model(model, peft_config)

  training_args = DPOConfig(
      num_train_epochs=10,  # More epochs for memorization
      per_device_train_batch_size=2,  # Smaller batch for better updates
      gradient_accumulation_steps=1,  # No accumulation, update frequently
      save_steps=100,
      optim="paged_adamw_8bit",
      logging_steps=10,
      learning_rate=1e-5,  # Higher LR for stronger updates
      max_grad_norm=1.0,  # Allow bigger updates
      warmup_ratio=0.1,
      lr_scheduler_type="cosine",  # Better for adaptation
      do_eval=False,
      adam_epsilon=1e-08,
      seed=42,
      save_strategy="steps",
      output_dir="./output-dir-2",
      gradient_checkpointing=True,
      fp16=True,
      bf16=False,
      remove_unused_columns=False,
  )


  dpo_trainer = DPOTrainer(
    model=model,
    args=training_args,
    train_dataset=update_dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
  )

  dpo_trainer.train()
  dpo_trainer.save_model()

  import gc
  import time
  del model, tokenizer, update_dataset
  gc.collect()
  torch.cuda.empty_cache()
  time.sleep(1)

