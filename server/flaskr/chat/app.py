import asyncio
import json
from torch.cuda import temperature
import websockets
import socket
from websockets.asyncio.server import serve
from websockets.asyncio.client import connect
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, TextIteratorStreamer, TextStreamer
import torch
from threading import Thread
import os
import model_util
import answer_util as answer
import rag_util as rag
import ruffle
import riley
import history
import chat_logger
import dpo
from datetime import datetime, timedelta
import gc
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5005

load_model = True

# these are temporary, the chat history should hold these
previous_response = ""
previous_prompt = ""

role = ""
context = ""
content = ""
message_list = []
agent = "ruffle"

chosen = ""
rejected = ""

misconception_detected : bool = False

training = False

async def async_streamer_wrapper(streamer):
    for token in streamer:
        yield token
        await asyncio.sleep(0)  # Let the event loop run


async def send_stream(websocket, config = None):
  global load_model, previous_response, previous_prompt, agent, misconception_detected, training

  async for message in websocket:
    message = json.loads(message)

    print("INIT MESSAGE",message)
    config = model_util.load_config(message)

    streamer = None

    inputs =  None

    
    if len(previous_response) > 0 and agent == "ruffle":
      # add user message to the history
      history.add_message(
        role="user",
        content=previous_prompt
      )

      # add agent message to the history
      history.add_message(
        role=agent,
        content=previous_response
      )

    # notifies front end that updates are available
    if chat_logger.check_for_update():
      await websocket.send(json.dumps({"message" : []}))
      await websocket.send(json.dumps({"message" : "Do you want to update now?", "agent" : "status"}))
    
    if not misconception_detected and len(previous_response) > 0 and agent == "riley":
      current_prompt = history.get_last_ruffle_message()["content"]
      # print(current_prompt, history.print_history())
      if (chat_logger.apply_chosen(current_prompt, previous_response)):
          chat_logger.log_sequence(current_prompt)
          
      else: 
       chat_logger.register_prompt(history.get_last_ruffle_message()["content"])
       chat_logger.register_rejected(previous_response)

    # print("MESSAGE PROMPT", message["prompt"])
    # print("MESSAGE", message)
    previous_prompt = message["prompt"]

    # history.print_history()

    # print("MESSAGE", message)

    # an error is encountered here
    if message["agent"] == "dpo":

      model_util.update_model()
 
      agent = "dpo" 
      training = True

      await websocket.send(json.dumps({"message" : []}))
      await websocket.send(json.dumps({"message" : "System is updating", "agent" : "status"}))
    
    if training: return

    # if the agent being requested is ruffle, that is the student
    elif message["agent"] == "ruffle": #message["agent"] == "ruffle" or :
      # print("RUFFLE IS BEING CALLED")
      misconception_detected = False
      context = ""

      # check if there's a misconception
      if len(previous_response) > 0:
        # This is for detecting misconceptions using riley
        print("Detecting misconceptions")

        if rag.vectorstore == None:
          documents = rag.load_document_chunks("../storage/pdfs/")
          rag.embeddings = rag.load_embeddings()
          rag.vectorstore = rag.create_vectorstore(documents, rag.embeddings)

        relevant_documents = rag.retrieve_documents(message["prompt"], rag.vectorstore)
        context = answer.create_full_context(relevant_documents)

        misconception_detected = riley.detect_misconception(model_util.tokenizer,
                                                                  model_util.model,
                                                                 previous_response,
                                                                 message["prompt"],
                                                                 context)
      if misconception_detected:
        print("A misconception has been detected")
        full_prompt = riley.prepare_revision_message(context, message["prompt"])
        inputs = model_util.tokenizer(full_prompt, return_tensors='pt').to(model_util.model.device)
        agent = "riley"
      else:
        print("A misconception has not been detected")
        # print("latest messages", history.format_chat(history.get_latest_messages()))
        full_prompt = ruffle.construct_prompt(message["prompt"], history.format_chat(history.get_latest_messages()))
        # print("Full prompt is here", full_prompt, len(full_prompt))
        inputs = model_util.tokenizer(full_prompt, return_tensors='pt')
        agent = "ruffle"

        # print("did this work?")
      # to appease the front end
      await websocket.send(json.dumps({"message" : []}))

    # if the agent being requested is riley, that is the helper
    elif message["agent"] == "riley":
      
      documents = rag.load_document_chunks("../storage/pdfs/")
      vector_store = rag.create_vectorstore(documents, rag.load_embeddings())
      relevant_documents = rag.retrieve_documents("What is a operating system?", vector_store)
      context = answer.create_full_context(relevant_documents)

      full_prompt = riley.prepare_help_message(context, history.get_last_ruffle_message()["content"])

      inputs = model_util.tokenizer(full_prompt, return_tensors='pt').to(model_util.model.device)

      arr = []

      for doc in relevant_documents:
          doc_obj = {
              "pageContent" : doc.page_content,
              "metaData" : doc.metadata,
          }

          arr.append(doc_obj)
      # print("ARR", arr)
      agent = "riley"

      # this sends the context, specifically the RAG documents so we can get the page and whatnot
      await websocket.send(json.dumps({"message" : arr}))
    # if user is requesting RAG
    else:

        if rag.vectorstore == None:
          documents = rag.load_document_chunks("../storage/pdfs/")
          rag.embeddings = rag.load_embeddings()
          rag.vectorstore = rag.create_vectorstore(documents, rag.embeddings)

        print("RAG PROMPT", message["prompt"])
        relevant_documents = rag.retrieve_documents(message["prompt"], rag.vectorstore)

        arr = []

        for doc in relevant_documents:
            doc_obj = {
                "pageContent" : doc.page_content,
                "metaData" : doc.metadata,
            }

            arr.append(doc_obj)
        # print("ARR", arr)
        agent = "rag"

        # this sends the context, specifically the RAG documents so we can get the page and whatnot
        await websocket.send(json.dumps({"message" : arr}))

    if message["agent"] == "ruffle" or message["agent"] == "riley":

      print("Streaming should be happening1")
      # this should never happen in the app but just a safety check
      if inputs is None: print("Something went wrong")

      if model_util.model.device.type == "cuda":
          inputs.to(model_util.model.device)

      streamer = TextIteratorStreamer(model_util.tokenizer, skip_special_tokens=True, skip_prompt=True)

      attention_mask = inputs["attention_mask"]

      thread = Thread(
          target=model_util.model.generate,
          kwargs={
              "input_ids": inputs.input_ids,
              "streamer": streamer,
              "max_new_tokens": config["max_new_tokens"],
              "top_k" : config["top_k"],
              "top_p" : config["top_p"],
              "temperature" : config["temperature"],
              "attention_mask" : attention_mask
          }
      )

      thread.start() # now start the thread
      previous_response = ""

      async for token in async_streamer_wrapper(streamer):
        message = {"message" : token, "agent" : agent}
        previous_response += token
        await websocket.send(json.dumps(message))

    # free unused memory
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    time.sleep(1)



async def main():
    
    chat_logger.load_state()

    # need to test this
    if os.path.exists("./adapters/user"):
      model_util.load_model(load_adapter=True, adapter_path="./adapters/user")
      # model_util.update_model()
    else:
      model_util.load_model()
      # model_util.update_model()

    documents = rag.load_document_chunks("../storage/pdfs/")
    rag.embeddings = rag.load_embeddings()
    rag.vectorstore = rag.create_vectorstore(documents, rag.embeddings)

 
    async with websockets.serve(send_stream, "localhost", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())
