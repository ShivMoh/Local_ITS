default_prompt = """
  Use the following pieces of context to answer the question at the end. Please follow the following rules:
  1. If you don't know the answer, say you don't the answer.
\n2. Only respond in short answer format. Try to keep answers to a maximum of 2 lines.
"""

def construct_prompt(context : str, question : str, sys_prompt = "") -> str:

  if len(sys_prompt) == 0:
    sys_prompt = default_prompt

  return f"""[INST] <<SYS>>
    You are a student seeking to learn. Your task is to ask the teacher relevant questions to gain a deeper understanding of the topic.
    Do not answer your own questions—focus on prompting the teacher to explain. Only ask a single question at a time

    <topic>
      Topic: What is an operating system, and what are its primary goals?
      - The operating system manages hardware and provides a foundation for applications.
      - Its goals include program execution, user convenience, and efficient hardware utilization.
      - It solves the challenge of creating a usable computing system.
      - The kernel is always running, while other programs are system or application programs.
      - The OS manages resources and resolves conflicts fairly.
      - It controls program execution to prevent errors and misuse.
    </topic>

    <teacher>
      {question}
    </teacher>
    <<SYS>>

    Answer: [/INST] """

  return f"""

    <system_prompt>
      {sys_prompt}
    </system_prompt>

    <context>
    {context}
    </context>

    <user>
    {question}
    </user>

    Answer:
    """


def calculate_number_of_characters(documents : list) -> int:
  return sum([len(doc.page_content) for doc in documents])

def create_full_context(documents : list) -> str:
  return "\n".join([doc.page_content for doc in documents])

def get_answer(response : str) -> str:
  answer : str = ""
  for x in range(1, len(response)):
    if response[len(response) - x] == ">": break
    answer = response[len(response) - x] + answer

  return answer
def write_output_to_file(output : str, filename : str) -> None:
  with open(filename, "a") as f:

    f.write(output)
    f.close()

