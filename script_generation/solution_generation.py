from script_generation import helpers
from script_generation import formatters 
from script_generation import consts 
from script_generation import question_generation
import torch

filtered_solutions = None
def generate_solutions():
    global filtered_solutions

    if len(consts.CONTENT) == 0:
        if helpers.huggingface_embeddings == None:
            helpers.embeddings = helpers.load_embeddings()

        if helpers.docs == None:
            helpers.docs = helpers.load_files()
        
        helpers.init_vectorstore(helpers.docs)

        results = helpers.find_content()

        consts.CONTENT = helpers.create_full_context(results)

    prompt = formatters.solution_format(consts.SUBJECT, question_generation.formatted_questions_string, consts.CONTENT)

    response = helpers.chat(prompt)

    split = response.split("<<SYS>>")

    rev_sol = split[-1]

    # print(rev_sol)

    ques = rev_sol.split("\n")

    # print(ques[2:len(ques) - 2])
    filtered_solutions = [x.split(":")[-1] for x in ques[2:len(ques) - 2] if len(x) > 0]

    print("Questions are as follows", len(filtered_solutions))

    if len(filtered_solutions) < len(question_generation.filtered_questions):
        print("Please regenerate responses. Insufficient number of solutions")
        helpers.write_content("solutions_failed", filtered_solutions)
        filtered_solutions = None
        return filtered_solutions
    
    # for i, solution in enumerate(filtered_solutions[0:len(question_generation.filtered_questions)]):
    #     print(f"Question {i} : {question_generation.filtered_questions[i]}")
    #     print(f"Solution {i} : {solution}")
    helpers.write_content("solutions_success", filtered_solutions)
    return filtered_solutions[0:len(question_generation.filtered_questions)]

def format_question_solution_string():
    global question_solution_string, filtered_solutions
    # process information for next prompt
    question_solution_string = ""
    for i, q in enumerate(filtered_solutions):
        question_solution_string += "Question " + str(i + 1) + ": " + question_generation.filtered_questions[i] + "\n"
        question_solution_string += "Solution " + str(i + 1) + ": " + filtered_solutions[i] + "\n"

    return question_solution_string

def format_question_solution_pairs():
    global filtered_solutions, question_solution_pairs
    # process information for next prompt
    question_solution_pairs = []
    for i, q in enumerate(question_generation.filtered_questions):
        pair = ""
        pair += "Question " + str(i + 1) + ": " + question_generation.filtered_questions[i] + "\n"
        pair += "Solution " + str(i + 1) + ": " + filtered_solutions[i] + "\n"

        question_solution_pairs.append(pair)

    return question_solution_pairs