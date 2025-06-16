chat_log = []

"""
Format for chat logs

  {
    role: "ruffle|riley|user"
    context : ""
    content : ""
  }
"""

def add_message(role : str, content : str):
  global chat_log 

  if role == "user":
    content = f"{content}"
  else:
    content = f"{content}"

  chat_log.append( {
      "role" : role,
      "content" : content
    }
  )


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

def add_messages(message_list = []) :
  for message in message_list:
    add_message(message["role"], message["content"])

def get_latest_messages(message_count = 3):
  return chat_log[len(chat_log) - (message_count + 1) : len(chat_log)]


def print_history():
  print(chat_log)
  
def get_last_user_message():
  for chat in reversed(chat_log):
    if chat["role"] == "user":
      return chat

def get_last_ruffle_message():
  for chat in reversed(chat_log):
    if chat["role"] == "ruffle":
      return chat

def get_last_riley_message():
  for chat in reversed(chat_log):
    if chat["role"] == "riley":
      return chat
