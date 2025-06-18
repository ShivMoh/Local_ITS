from script_generation import question_generation, solution_generation, expectation_generation
from script_generation import helpers
import time

# question_generation.filtered_questions = helpers.load_file("questions_success_1")
# print(question_generation.filtered_questions)

# question_generation.format_questions()

# solution_generation.filtered_solutions = helpers.load_file("solutions_success_2")
# solution_generation.format_question_solution_pairs()

# print(solution_generation.question_solution_pairs)

# exit()



questions = None
solutions = None

start_time_question_gen = time.time()
while True:
    if questions == None:
        questions = question_generation.generate_questions()
        
    else:
        check = input("Please review the generated questions. Questions are okay? y/n")
        if check == "y":
            question_generation.filtered_questions = helpers.load_file("questions_success_0")
            break

question_generation.format_questions()

print(f"Question generation took {time.time() - start_time_question_gen}")

start_time_solution_gen = time.time()

while True:
    if solutions == None: 
        solutions = solution_generation.generate_solutions()
    else: 
        check = input("Please review the generated questions. Questions are okay? y/n")
        if check == "y":
            solution_generation.filtered_solutions = helpers.load_file("solutions_success_1")
            break


solution_generation.format_question_solution_pairs()

print(f"Solution Generation took {time.time() - start_time_solution_gen}")

start_time_expectation_generation = time.time()

x = 0
exclude = []
while x < 5:

    if x not in exclude:
        expectation_generation.generate_per_pair(pair=solution_generation.question_solution_pairs[x])
        helpers.write_content("correct_expectations", [solution_generation.question_solution_pairs[x]], number=False)
        helpers.write_content("correct_expectations", [expectation_generation.generated_expectation], number=False)
        helpers.write_content("correct_expectations", [" "], number=False)

    x+=1
    print(f"At iteration {x}")

print(f"Expectation generation took {time.time() - start_time_expectation_generation} seconds\nTotal Generation time took: {time.time() - start_time_question_gen} seconds")