import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from trl import DPOConfig, DPOTrainer
import torch
import time
import os
import gc
import chat_logger
import model_util

def update_model():

    latest_date, iteration_counter, update_list = chat_logger.load_state()

    if len(update_list) == 0:
        print("Nothing to update")
        return

    # load model in 4 bit
    # bnb_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_compute_dtype=torch.bfloat16,
    #     bnb_4bit_quant_type="nf4",
    # )

    # model = AutoModelForCausalLM.from_pretrained(
    #   "meta-llama/Llama-2-7b-chat-hf",
    #   quantization_config=bnb_config,
    #   device_map={"": 0},
    #   torch_dtype=torch.float16,
    #   attn_implementation="flash_attention_2",
    # )

    # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    # tokenizer.pad_token = tokenizer.eos_token


    # load your dataset of choice
    # dataset = load_dataset('json', data_files=update_list, split='train')
    dataset = load_dataset("HumanLLMs/Human-Like-DPO-Dataset", split="train")
    dataset = dataset.select(range(10))

    print(latest_date, iteration_counter, update_list)
  
    peft_config = None
    if model_util.has_adapter:
        peft_config = None
    else:
        print("THIS SHOULD RUN")
        peft_config = LoraConfig(
            lora_alpha=256,
            lora_dropout=0.1,
            r=8, # default set to 8
            bias="none",
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

    training_args = DPOConfig(
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        save_steps=100,
        optim="paged_adamw_8bit",
        logging_steps=1,
        learning_rate=5e-7,
        max_grad_norm=1.0,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        do_eval=False,
        adam_epsilon=1e-08,
        save_strategy="no",
        output_dir=f"./test",
        gradient_checkpointing=True,
        fp16=True,
        bf16=False,
        remove_unused_columns=False,
        beta = 2,
        push_to_hub=False, # if you want to push to hugging face,
        label_names=["prompt", "chosen", "rejected"]
    )

    # tr_dataset = dataset.select(range(i))

    dpo_trainer = DPOTrainer(
        model=model_util.model,
        args=training_args,
        train_dataset=dataset,
        processing_class=model_util.tokenizer,
        peft_config=peft_config,
    )

    dpo_trainer.train()
    dpo_trainer.save_model("./adapters/user")

    del dpo_trainer
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    time.sleep(1)

    chat_logger.update_list = []

    # save state
    chat_logger.save_state()



def test_upate():
    
    # load your dataset of choice
    # dataset = load_dataset('json', data_files=update_list, split='train')
    dataset = load_dataset("HumanLLMs/Human-Like-DPO-Dataset", split="train")
    dataset = dataset.select(range(2))


    peft_config = None

    print("THIS SHOULD RUN")
    peft_config = LoraConfig(
        lora_alpha=256,
        lora_dropout=0.1,
        r=8, # default set to 8
        bias="none",
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

    training_args = DPOConfig(
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        save_steps=100,
        optim="paged_adamw_8bit",
        logging_steps=1,
        learning_rate=5e-7,
        max_grad_norm=1.0,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        do_eval=False,
        adam_epsilon=1e-08,
        save_strategy="no",
        output_dir=f"./test",
        gradient_checkpointing=True,
        fp16=True,
        bf16=False,
        remove_unused_columns=False,
        beta = 2,
        push_to_hub=False, # if you want to push to hugging face,
        label_names=["prompt", "chosen", "rejected"]
    )

    # tr_dataset = dataset.select(range(i))

    dpo_trainer = DPOTrainer(
        model=model_util.model,
        args=training_args,
        train_dataset=dataset,
        processing_class=model_util.tokenizer,
        peft_config=peft_config,
    )

    dpo_trainer.train()
    dpo_trainer.save_model("./adapters/user")

