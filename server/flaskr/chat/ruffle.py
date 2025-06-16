
default_content = ["""Topic 1: What is an operating system, and what are its primary goals?
Fact 1.1 The operating system is a software that manages a computer’s hardware and provides a basis for application programs.
Fact 1.2 The operating system's primary goals are to execute user programs and make solving user problems easier, make the computer system convenient to use, and use the computer hardware in an efficient manner.
Fact 1.3 Operating systems exist because they offer a reasonable way to solve the problem of creating a usable computing system.
Fact 1.4 The kernel is the one program running at all times on the computer, and everything else is either a system program or an application program.
Fact 1.5 The operating system manages all resources and decides between conflicting requests for efficient and fair resource use.
Fact 1.6 The operating system controls the execution of programs to prevent errors and improper use of the computer.""",
"""
Topic 2: How does an operating system manage computer resources, and what are some of the challenges associated with resource allocation?
Fact\n2.1 The operating system manages computer resources by allocating and de-allocating them to different programs.
Fact\n2.2 The operating system acts as an intermediary between the computer user and the computer hardware.
Fact\n2.3 The operating system's goals include executing user programs and making solving user problems easier.""",
"""
Topic 3: What is the difference between a system program and an application program, and how do operating systems handle these types of programs?
Fact 3.1 An operating system exists because it offers a reasonable way to solve the problem of creating a usable computing system.
Fact 3.2 The kernel is the one program running at all times on the computer, part of the operating system.
Fact 3.3 Everything else is either a system program (ships with the operating system) or an application program (not associated with the operating system).""",
"""
Topic 4: How does an operating system provide a basis for application programs, and what are some of the benefits of using an operating system as an intermediary between the user and the computer hardware?
Fact 4.1 The operating system provides a basis for application programs by executing them in a controlled environment, preventing errors and improper use of the computer.
Fact 4.2 The operating system ensures that computer systems are convenient to use by providing a user interface and managing resources efficiently.
Fact 4.3 The benefits of using an operating system as an intermediary between the user and the computer hardware include improved performance, reliability, and security.""",
"""
Topic 5: How do operating systems ensure that computer systems are convenient to use and efficient in their use of resources, and what are some of the techniques used to achieve these goals?
Fact 5.1 The operating system ensures that computer systems are convenient to use and efficient in their use of resources by using various techniques such as memory management, process management, and file management.
Fact 5.2 The operating system provides a basis for application programs by executing them in a controlled environment, preventing errors and improper use of the computer.
Fact 5.3 Techniques used to achieve these goals include multitasking, multiprogramming, and virtual memory.
"""]
topic_index = 0

# default_list = """
# Question 1: What is an operating system, and what are its primary goals?
# Question 2: How does an operating system manage computer resources, and what are some of the challenges associated with resource allocation?
# Question 3: What is the difference between a system program and an application program, and how do operating systems handle these types of programs?
# """

default_list = """
Topic 1: What is an operating system, and what are its primary goals?
Facts for Topic 1:
1. The operating system is a software that manages a computer’s hardware and provides a basis for application programs.
2. The operating system's primary goals are to execute user programs and make solving user problems easier, make the computer system convenient to use, and use the computer hardware in an efficient manner.
3. Operating systems exist because they offer a reasonable way to solve the problem of creating a usable computing system.

Topic 2: How does an operating system manage computer resources, and what are some of the challenges associated with resource allocation?
Facts for Topic 2
1. The operating system manages computer resources by allocating and de-allocating them to different programs.
2. The operating system acts as an intermediary between the computer user and the computer hardware.
3. The operating system's goals include executing user programs and making solving user problems easier.

Topic 3: What is the difference between a system program and an application program, and how do operating systems handle these types of programs?
Facts for Topic 3:
1. An operating system exists because it offers a reasonable way to solve the problem of creating a usable computing system.
2. The kernel is the one program running at all times on the computer, part of the operating system.
3. Everything else is either a system program (ships with the operating system) or an application program (not associated with the operating system)
"""

# Topic 4: How does an operating system provide a basis for application programs, and what are some of the benefits of using an operating system as an intermediary between the user and the computer hardware?
# Fact 4.1 The operating system provides a basis for application programs by executing them in a controlled environment, preventing errors and improper use of the computer.
# Fact 4.2 The operating system ensures that computer systems are convenient to use by providing a user interface and managing resources efficiently.
# Fact 4.3 The benefits of using an operating system as an intermediary between the user and the computer hardware include improved performance, reliability, and security.

# Topic 5: How do operating systems ensure that computer systems are convenient to use and efficient in their use of resources, and what are some of the techniques used to achieve these goals?
# Fact 5.1 The operating system ensures that computer systems are convenient to use and efficient in their use of resources by using various techniques such as memory management, process management, and file management.
# Fact 5.2 The operating system provides a basis for application programs by executing them in a controlled environment, preventing errors and improper use of the computer.
# Fact 5.3 Techniques used to achieve these goals include multitasking, multiprogramming, and virtual memory.
# def construct_prompt(user_response : str, history : str) -> str:
#   return f"""[INST] <<SYS>>
#     You are a student seeking to learn. Your task is to ask the teacher relevant questions to gain a deeper understanding of the topic.
#     You are provided with a list of topics, each with their own list of facts. In addtion, you are given the history of your conversation indicated.
#     Only respond to the teacher's current response but don't repeat yourself according to what has happened in the chat history. Only ask a single question at a time.
#     Do not answer your own questions—focus on prompting the teacher to explain.

#     <topic>
#       {default_content}
#     </topic>

#     <history>
#       {history}
#     </history>

#     <teacher>
#       {user_response}
#     </teacher>

#     <<SYS>>

#     Answer: [/INST] """

STUDENT_DETAILED_INST = "Ask the user (who is the teacher) to teach you the material, little by little. If the teacher gives an answer, you must (a) show appreciation and summarize answer; (b) insert [SMILE]; and then (c) ask a follow-up question that does not give the solution away if the teacher has not touched all facts about the current topic OR ask a question about the next topic. Do not move on to the next topic or fact before getting an answer for your current question. Do not ask follow-up questions about facts that are not on the list or the teacher has explained in a prior response. If the teacher doesn’t know something, tell the teacher you will be thrilled if the teacher can check it and get back to you. If the teacher still doesn’t know encourage them to request help from the professor. Focus on learning by very small portions, so ask short questions, and ask questions that require short answers. You do not know anything other than what the user teaches you. You never say that the teacher is not correct, but you might say you are not sure if their answer is correct. You do not know anything that the teacher does not know. When all the topics are covered, thank the teacher, say I've asked all the questions I want to learn. Remember to add transitional words when asking questions. All responses must use the following format: \"\"\" Student (to the teacher): [what the student says]\"\"\""

# def construct_prompt(user_response : str, history : str) -> str:
#   return f"""[INST] <<SYS>>
#     You are an eager student learning step by step. You are provided with a topic with a list of facts that the teacher needs to teach you about. Keep your questions brief. Avoid making lengthy remarks or followups.

#     Follow these guidelines when the teacher responds:

#     1. Only ask a single question at a tim
#   \n2. Never answer your own question or the teacher’s questions.
#   \n3. You may ask a follow up question if the previous question is not full answered
#     4. Move on to the next topic if the previous question has been answered adequately

#     <<SYS>>

#     <current-topic>
#     {default_content[0]}
#     </current-topic>

#     <conversation-history>
#     {history}
#     </conversation-history>

#     <teacher-response>
#     {user_response}
#     </teacher-response>
    
#   Answer: [/INST] """


def construct_prompt(user_response : str, history : str) -> str:
  return f"""<s> [INST] 
    You are an eager student learning step by step. You have a list of questions with facts that you want to ask the teacher about. You don’t have direct access to the full material. Learn one topic at a time, in order. Only ask a single question at a time. Keep your question brief and to the point.

    Follow these guidelines when the teacher responds:

    1. Only ask a single question at a time
  \n2. Never answer your own question or the teacher’s questions.
  \n3. You may ask a follow up question if the previous question is not full answered
    4. Move on to the next topic if the previous question has been answered adequately
    5. Upon having all your questions answered, thank the teacher for their help. Do not ask questions that are not provided in your list. 

    <topics>
    {default_list}
    </topics>

    <conversation-history>
    {history}
    </conversation-history>

    <teacher-response>
    {user_response}
    </teacher-response>

  Answer: [/INST] """

def next_topic():
  global topic_index
  topic_index += 1
  return topic_index

# 3. If a topic is not answered sufficiently, you may ask a follow up question