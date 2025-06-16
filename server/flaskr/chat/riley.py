# prepare revision
# revises accuracy to content
from transformers import LlamaTokenizer

DELIMITER = "####"

# this will actually provide a response based on that misconception
def prepare_revision_message(material: str, teacher_response: str):
    return f"""[INST] <<SYS>>
        You are a **supportive and encouraging computer science professor**, supervising a new teacher's interaction with a student.
        Your goal is to provide **brief, constructive feedback** on the teacher’s response **without introducing new information**.

        - **Only refer to the provided material**.
        - **Keep feedback polite, positive, and concise**.
        - **If you detect incorrect information or a typo, ask the teacher to revise their response**.

        <teacher-response> {teacher_response} </teacher-response>
        <material> {material} </material>

        Use this format:
        **Comment for teacher: <Your polite revision comment>**

    <</SYS>> [/INST]"""

expected_answer = """
  The operating system is a software that manages a computer’s hardware and provides a basis for application programs.
  Its primary goals are to execute user programs and make solving user problems easier, make the computer system convenient
  to use, and use the computer hardware in an efficient manner. Operating systems are found almost everywhere today, from cars
  and home appliances (IoT), to smartphones and cloud computing environments.
"""
# this simply detects a misconception on the teachers behalf
def prepare_misconception_message(student_question : str, teacher_answer : str):
  return f"""<s> [INST] <<SYS>>

    <s> [INST] <<SYS>>  
     You are a professor evaluating a teacher's answer to a student's question.   

     ### **Evaluation Rules:**  
     1. **Ignore typos, grammar, or formatting issues** — these do not count as inaccuracies.    
     2. **Partially correct responses are acceptable** — an answer does not need to be complete. The student will ask follow up questions if the answer is not complete.  
     3. **Fully irrelevant or nonsensical answers are inaccurate**.  

    **Student Question:**  
    {student_question}

    **Teacher Answer:**  
    {teacher_answer}

    Respond using the format:
    **Classify the answer as one of the following: PERFECT, GOOD, POOR, FALSE*

    <</SYS>> [/INST]"""


# def prepare_misconception_message(student_question: str, teacher_answer: str) -> str:
#   return f"""
#     <s> [INST] <<SYS>>  
#     You are a professor evaluating the accuracy of a teacher’s  

#     ### **Evaluation Rules:**  
#     1. **Ignore typos, grammar, or formatting issues**—these do not count as inaccuracies.    
#     2. **Partially correct responses are acceptable**—an answer does not need to be 100% complete.  
#     3. **Fully irrelevant or nonsensical answers are inaccurate**.  
#     4. **Answers that do not answer the question are inaccurate
#     5. **Answers that contradict known knowledge is very inaccurate

#     ### **Task:**  
#     Assess whether the teacher’s response contains factual inaccuracies **based on the provided material**.  

#     **Student Question:**  
#     {student_question}

#     **Teacher Answer:**  
#     {teacher_answer}

#     Rate the accuracy of the teacher’s response on a scale of **1 to 10**, where **10 is fully accurate** and **1 is entirely incorrect**.  

#     Respond in the following format:  

#     Rating=
#     <</SYS>> [/INST] </s>  
#   """

def prepare_misconception_message_orignal(student_question : str, teacher_answer : str):
  return f"""You are a professor evaluating whether a teacher's answer to a student's question contains factually incorrect information. Ignore typos, but count fully irrelevant responses as incorrect.

  Student Question: #### ${student_question} ####
  Teacher Answer: #### ${teacher_answer} ####

  Teacher answer contains factually incorrect information: <YES or NO>
"""

def prepare_help_message(relevant_content : str, teacher_response : str, question : str = ""):
  return f"""
    You are a friendly and encouraging computer science professor who supervises interactions between a new teacher and a student. Provide brief and positive advice to help the teacher respond to the student’s question. Only use the material provided below, and avoid referring to any outside information. Do not answer the question but only hint towards how the teacher could answer the question

    Material: {relevant_content}
    Current Question: {teacher_response}

    Comment for Teacher: <brief hint or advice based on the material>
    """

  # <expected-answer> {expected_answer} </expected-answer>
def detect_misconception(tokenizer, model, prev_student_message, current_user_message, context) -> bool:
  full_prompt = prepare_misconception_message(prev_student_message, current_user_message)
  # print(full_prompt)
  inputs = tokenizer(full_prompt, return_tensors='pt').to(model.device)

  outputs = model.generate(
        inputs.input_ids,
        do_sample=False
  )

  response = tokenizer.decode(outputs[0], skip_special_tokens=True)
  filtered_response = response.split("[/INST]")[-1].strip()
  print(filtered_response)
  if "FALSE" in filtered_response or "POOR" in filtered_response:
    return True
 
  return False

def evaluate_understanding(answer : str, solution : str):
  pass

