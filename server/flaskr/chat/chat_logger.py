from datasets import load_dataset
from datetime import datetime
import os
import json

directory = "./user_data"
prompt = ""
chosen = ""
rejected = ""

UPDATE_NUM = 5
UPDATE_QUEUE_DATE = None
MAX_ENTRIES = 5

iteration_counter = 0
latest_date = None
update_list = []

previous_prompt = ""


from datetime import datetime, timedelta

def load_variables(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    else:
        return {} 

def update_variable(filepath, key, value):
    data = load_variables(filepath)
    data[key] = value
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_state():

  global latest_date, iteration_counter, update_list

  config = load_variables("./user_data/config.json")
  
  latest_date = config["latest_date"]
  iteration_counter = config["iteration_counter"]
  update_list = config["update_list"]

  print("VARIABLES",  latest_date, iteration_counter, update_list)
     
  return [latest_date, iteration_counter, update_list]

def save_state():
     
  file_path = "./user_data/config.json"

  update_variable(file_path, "iteration_counter", iteration_counter)
  update_variable(file_path, "latest_date", latest_date)
  update_variable(file_path, "update_list", update_list)

def load_ds(path : str = "", unloaded = True, date_range : list[str] = [], size = -1):
  if len(path) > 0:
    # print("does this work?")
    dataset = load_dataset('json', data_files=path, split='train')
    return dataset

  # print("are we here?")
  if unloaded:
    # we lookup in the db to find all unloaded datasets
    # select name logs where unloaded = True
    files = ["./human_like_data.json"]
    dataset = load_dataset('json', data_files=files)

    return dataset

# def set_update_time(hours):
#   global UPDATE_QUEUE_DATE
#   UPDATE_QUEUE_DATE = datetime.now() + timedelta(hours=hours) 

# def check_if_time_exceeded():

#   global UPDATE_QUEUE_DATE

#   if (abs((datetime.now() - UPDATE_QUEUE_DATE).total_seconds()) < 10):
#     return True
#   else: return False

def check_for_update():
  load_state()
  if len(update_list) > 0:
    return True
  else: return False

def register_chosen(current_chosen):
  global chosen
  chosen = current_chosen

def register_rejected(current_rejected):
  global rejected
  rejected = current_rejected

def register_prompt(current_prompt):
  global prompt
  prompt = current_prompt

def apply_chosen(current_prompt, chosen_candidate):
  global chosen, rejected, prompt
  if current_prompt == prompt and len(rejected) > 0:
    register_chosen(chosen_candidate)
    return True
  return False

def reset(current_prompt, current_chosen, current_rejected):
  register_prompt(current_prompt)
  register_chosen(current_chosen)
  register_rejected(current_rejected)

  
def log_sequence(current_prompt):
  global prompt, chosen, rejected, iteration_counter, latest_date, update_list, previous_prompt


  new_entry = {
      "prompt": prompt,
      "chosen": chosen,
      "rejected": rejected
  }

  current_date = datetime.today().strftime('%Y-%m-%d')

  if latest_date != current_date:
    latest_date = current_date
    iteration_counter = 0

  file_name = current_date + "-" + str(iteration_counter) + ".json"
  full_path = os.path.join(directory, file_name)

  # Load existing dataset or create a new one
  if os.path.exists(full_path):
      with open(full_path, "r", encoding="utf-8") as f:
          data = json.load(f)
  else:
      data = []

  # print("HELLLLLOOOOO, I SHOULD BE LOGGING")
  print("Prompts in chat logger", current_prompt, previous_prompt)
  if len(data) > 0 and len(data) < MAX_ENTRIES:
    if data[-1]["prompt"] == current_prompt:
      data[-1]["chosen"] = chosen
      data[-1]["rejected"] = rejected
    else:
      data.append(new_entry)
  elif len(data) == 0:
    data.append(new_entry)
  else:
    data = []
    iteration_counter += 1
    update_list.append(full_path)
    file_name = current_date + "-" + str(iteration_counter) + ".json"
    full_path = os.path.join(directory, file_name)

    data.append(new_entry)

  # Save updated dataset
  with open(full_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)

  # update state after each iteration
  save_state()

  return True

