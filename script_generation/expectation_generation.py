from script_generation import helpers
from script_generation import formatters 
from script_generation import consts
from script_generation import solution_generation

def generate_expectations():
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

    expectations = []
    for pair in solution_generation.question_solution_pairs:
        prompt = formatters.expecation_single_shot(subject=consts.SUBJECT, question=pair, example=consts.EXAMPLE, content=consts.CONTENT)
        res = helpers.chat(prompt)
        # print(res)
        expectation = res.split("<<SYS>>")[-1]
        # print(expectation)
        expectations.append(expectation)

    helpers.write_content("expectations", expectations)

def generate_per_pair(pair):
    global generated_expectation
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

    prompt = formatters.expecation_single_shot(subject=consts.SUBJECT, question=pair, example=consts.EXAMPLE, content=consts.CONTENT)
    res = helpers.chat(prompt)

    generated_expectation = (res.split("<<SYS>>")[-1]).split(":")[-1]

    # helpers.write_content("expectations", generated_expectation)