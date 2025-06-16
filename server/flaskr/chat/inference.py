
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, TextIteratorStreamer, TextStreamer
import torch

model = None
tokenizer = None

eval_prompt = """
    <s> [INST] <<SYS>>

    You are a professor assessing whether a teacher's answer contains factually incorrect information. 
    
    Follow the rules below to guide your evaluation:

    1. Typos, grammatical errors or poor formatting does not count as incorrect information 
  \n2. Fully irrelevant responses are incorrect
  \n3. Do not ask the user to provide more context or examples. Lack of context or examples does not count as inaccurate / incorrect information
    4. Base your evaluation solely on the provided material
    5. Partially correct statements are acceptable. The answer does not need to be 100 correct 

    Factually incorrect ONLY refers to an instance where the teacher's response contradicts something that is in the material.
    A response is not inaccurate if it does lacks examples, details or does not explain in the clearest manner possibe.
    A response is only inaccurate if it has a infactual piece of information that constradicts something that is in the provided material 
    
    <student-question> Great, let's get started! Here's my first question: Question 1: What is an operating system, and what are its primary goals? </student-question>
    <teacher-answer> The operating system is a software that manages a computer’s hardware and provides a basis for application programs. Its primary goals are to execute user programs and make solving user problems easier, make the computer system convenient to use, and use the computer hardware in an efficient manner. Operating systems are found almost everywhere today, from cars and home appliances (IoT), to smartphones and cloud computing environments. </teacher-answer>
    <material>  
      ⬡ Operating System is a resource allocator
       Manages all resources
       Decides between conflicting requests for efficient and fair resource use
      ⬡ Operating System is a control program
       Controls execution of programs to prevent errors and improper use of the computer
      What Operating Systems Do?
      System View
      24
      University of Guyana
      Jerome Allicock
      ⬡ Computer system can be divided into four components:
       Hardware – provides basic computing resources
       CPU, memory, I/O devices
       Operating System
       Controls and coordinates use of hardware among various applications and users
       Application programs – define the ways in which the system resources are used to solve 
      the computing problems of the users
       Word processors, compilers, web browsers, database systems, video games
       Users
       People, machines, other computers
      What Operating Systems Do?
      Computer System Structure
      21
      University of Guyana
      Jerome Allicock
      ⬡ A software that manages a computer’s hardware. 
       Also provides a basis for application programs and acts as an intermediary between 
      the computer user and the computer hardware. 
      ⬡ Operating system goals:
       Execute user programs and make solving user problems easier
       Make the computer system convenient to use
       Use the computer hardware in an efficient manner
      ⬡ Operating systems are found almost everywhere today, from cars and home appliances 
      (IoT), to smart phones and cloud computing environments. 
      What is an Operating System?
      20
      University of Guyana
      Jerome Allicock 
    </material>

    Rate the accuracy of the response from 1 to 100 and respond using the following format:
    **Accuracy Rating: **

    <</SYS>> [/INST] </s>
"""

eval_prompt_optimized = """
  <s> [INST] <<SYS>>  
  You are a professor evaluating the accuracy of a teacher’s  

  ### **Evaluation Rules:**  
  1. **Ignore typos, grammar, or formatting issues**—these do not count as inaccuracies.    
\n2. **Partially correct responses are acceptable**—an answer does not need to be 100% complete.  
\n3. **Fully irrelevant or nonsensical answers are inaccurate**.  
  4. **Answers that do not answer the question are inaccurate
  5. **Answers that contradict known knowledge is very inaccurate

  ### **Task:**  
  Assess whether the teacher’s response contains factual inaccuracies **based on the provided material**.  

  **Student Question:**  
  How does an operating system manage computer resources, and what are some of the challenges associated with resource allocation?

  **Teacher Answer:**  
  The operating system is a frog

  Rate the accuracy of the teacher’s response on a scale of **1 to 10**, where **10 is fully accurate** and **1 is entirely incorrect**.  

  Respond in the following format:  

  Rating=
  <</SYS>> [/INST] </s>  
"""
def run(query):

  system_prompt =  """
  [INST] <<SYS>>
  You are an eager student learning step by step. You are provided with a topic with a list of facts that the teacher needs to teach you about. Keep your questions brief. Avoid making lengthy remarks or followups.

  Follow these guidelines when the teacher responds:

  1. Only ask a single question at a tim
\n2. Never answer your own question or the teacher’s questions.
\n3. You may ask a follow up question if the previous question is not full answered
  4. Move on to the next topic if the previous question has been answered adequately

  <topics>
    <topic-1>
    Topic 1: What is an operating system, and what are its primary goals?
    Fact 1.1 The operating system is a software that manages a computer’s hardware and provides a basis for application programs.
    Fact 1.2 The operating system's primary goals are to execute user programs and make solving user problems easier, make the computer system convenient to use, and use the computer hardware in an efficient manner.
    Fact 1.3 Operating systems exist because they offer a reasonable way to solve the problem of creating a usable computing system.
    </topic-1>

    <topic-2>
    Topic 2: How does an operating system manage computer resources, and what are some of the challenges associated with resource allocation?
    Fact\n2.1 The operating system manages computer resources by allocating and de-allocating them to different programs.
    Fact\n2.2 The operating system acts as an intermediary between the computer user and the computer hardware.
    Fact\n2.3 The operating system's goals include executing user programs and making solving user problems easier.
    </topic-2>

    <topic-3>
    Topic 3: What is the difference between a system program and an application program, and how do operating systems handle these types of programs?
    Fact 3.1 An operating system exists because it offers a reasonable way to solve the problem of creating a usable computing system.
    Fact 3.2 The kernel is the one program running at all times on the computer, part of the operating system.
    Fact 3.3 Everything else is either a system program (ships with the operating system) or an application program (not associated with the operating system)
    </topic-3>
  </topics>
  """
   

  conversation = [
    {"role": "user", "content": query},
    {"role" : "assistant", "content" : system_prompt}
  ]
  # tools = [get_current_weather]

  global model, tokenizer
  if model is None and tokenizer is None:

    model_name = "mistralai/Mistral-7B-Instruct-v0.3"

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4"
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config = bnb_config,
        device_map={"":0},
            # attn_implementation="flash_attention_2"
    )

        # model = torch.compile(model)

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '<PAD>'})

  # inputs = tokenizer(query, return_tensors='pt').to(model.device)
    # format and tokenize the tool use prompt 
  inputs = tokenizer.apply_chat_template(
              conversation,
              add_generation_prompt=True,
              return_dict=True,
              return_tensors="pt",
  )

  inputs.to(model.device)
  outputs = model.generate(**inputs, max_new_tokens=250)

  return tokenizer.decode(outputs[0], skip_special_tokens=True)

def evaluate():
  # tools = [get_current_weather]

  global model, tokenizer, eval_prompt_optimized

  if model is None and tokenizer is None:

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
        attn_implementation="flash_attention_2"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '<PAD>'})

  inputs = tokenizer(eval_prompt_optimized, return_tensors='pt').to(model.device)

  inputs.to(model.device)
  
  outputs = model.generate(
    **inputs, 
    max_new_tokens=50,
    temperature=0.1, # keep responses deterministic
    top_k=20, # restricts token selection to high confidence choices
    top_p=0.9, # balances diversity and precision,
    repetition_penalty=1.1
  )

  return tokenizer.decode(outputs[0], skip_special_tokens=True)

inaccurate_count = 0
import time

for i in range(5):
  # prompt = input("Enter your prompt: ")

  start = time.time()

  response = evaluate()
  res = response.split("Rating = ")
  print("RES", res[-1][0])
  if int(res[-1][0]) < 6:
    # print("Response is inaccurate")
    inaccurate_count += 1
  
  #print("Res", res)

  print(f"Time taken: {time.time() - start}")

print(inaccurate_count)