
def question_format(subject, content):
    return  f""" <<SYS>> You are a {subject} professor that prepares review/guiding \
                questions to help your students learn a lesson. Write at least 5 free-response questions \
                designed to help your students understand the lesson material. Do not answer the questions and do not assign points to the questions. The questions you write \
                should promote comprehensive learning and cover all the lesson material. Please try \
                to avoid writing questions that overlap in content. The lesson material is provided \
                below delimited by triple backticks.\n Write the questions in the following format:\n\
                Question 1: <Question 1 text> \n\
                ... \n\
                Question N: <Question N text> \n\n\
                Lesson Material:```{content}``` <<SYS>>"""

def solution_format(subject, question, content):
    return f"""  <<SYS>>You are a {subject} professor that prepares solutions \
                for a range of review/guiding questions designed to help your students learn a lesson. \
                The questions and lesson text are provided below delimited by triple backticks. \
                The solutions should be focused and explain only the most important information from 
                the lesson material. Do not just copy sentences from the lesson text. Write the 
                solutions in the following format:\n\
                Solution 1: <Question 1 solution text> \n\
                ... \n\
                Solution N: <Question N solution text> \n\

                Question List: ```{question}```\n\n\
                Lesson Material: ```{content}```<<SYS>>
            """

# this with max tokens 4096 worked in like one attempt
def expectation_format(subject, questions, example):
    return f"""  <<SYS>>You are a {subject} professor that creates lists summarizing \
                the key facts contained in the solutions to review/guiding questions \
                designed to help your students learn a lesson. \
                The questions and solutions are provided below delimited by triple backticks. \
                You want to keep the lists brief and focused. \
                Write the lists in the following format:\n\
                List 1: <Question 1 fact 1; ...; Question 1 fact m1>\n\
                ...\n\
                List N: <Question N fact 1; ...; Question N fact mN>\n\
                \n\
                Questions and Solutions: ```{questions}```
                An example of the expected format is as follows:
                ```{example}```
                <<SYS>>
                """

def expectation_format_example(subject, questions, example):
    return f"""  <<SYS>>You are a {subject} professor that creates lists summarizing \
                the key facts contained in the solutions to review/guiding questions \
                designed to help your students learn a lesson. \
                The questions and solutions are provided below delimited by triple backticks. \
                Questions and Solutions: ```{questions}```
                You want to keep the lists brief and focused. \
                List 1: <Question 1 fact 1; ...; Question 1 fact m1>\n\
                ...\n\
                List N: <Question N fact 1; ...; Question N fact mN>\n\
                \n\
                Write the lists as shown in the following example\
                ```{example}```
         
                <<SYS>>
                """

def expecation_single_shot(subject, question, example, content, num=3):
    return f"""  <<SYS>>You are a {subject} professor that creates lists summarizing \
                the key facts contained in the solutions to review/guiding questions \
                designed to help your students learn a lesson. \
                For the following question <question>```{question}```</question>, generate {num} 
                facts from the given context <context>```{content}```</context> \
                
                Please follow the format of below example when listing the facts:
                <example>{example}</example> 

                Facts: 
                
                """