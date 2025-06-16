from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Define chat history
chat_history = []

def format_chat(history):
    """
    Formats chat history for LLaMA 2 chat models.
    """
    formatted = "<s>"  # Start of conversation token
    for msg in history:
        if msg["role"] == "user":
            formatted += f"[INST] {msg['content']} [/INST] "
        else:
            formatted += f"{msg['content']} </s> "  # End assistant message
    return formatted

def chat(user_input):
    """
    Generates a response from the model, keeping track of chat history.
    """
    global chat_history  # Maintain history across calls

    chat_history.append({"role": "user", "content": user_input})

    chat_history.append({"role": "assistant", "content": ""})

    return ""

