from script_generation import helpers
from script_generation import formatters 
from script_generation import consts

formatted_questions_string = ""
filtered_questions = []

def generate_questions():
    global filtered_questions
    if len(consts.CONTENT) == 0:
        if helpers.huggingface_embeddings == None:
            helpers.embeddings = helpers.load_embeddings()

        if helpers.docs == None:
            helpers.docs = helpers.load_files()
        
        helpers.init_vectorstore(helpers.docs)

        results = helpers.find_content()

        consts.CONTENT = helpers.create_full_context(results)


    if helpers.model == None:
        helpers.load_model()

    response = helpers.chat(formatters.question_format(consts.SUBJECT, consts.CONTENT))

    split = response.split("<<SYS>>")

    rev_quest = split[-1]

    ques = rev_quest.split("\n")
    filtered_questions = [x.split(":")[-1] for x in ques[2:len(ques) - 2] if len(x) > 0]

    if len(filtered_questions) < 5:
        assert("Please regenerate responses. Insufficient number of questions")
        helpers.write_content("questions_failed", filtered_questions)
        filtered_questions = None
        return filtered_questions
    
    helpers.write_content("questions_success", filtered_questions)
    return filtered_questions

    # for question in filtered_questions:
    #     print(question)

def format_questions():
    global filtered_questions, formatted_questions_string

    formatted_questions_string = ""
    for i, q in enumerate(filtered_questions):
        if i == 5: break
        formatted_questions_string += "Question " + str(i + 1) + ": " + q + "\n"   

    return formatted_questions_string