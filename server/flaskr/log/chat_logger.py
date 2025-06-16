from datasets import load_dataset
from datetime import datetime
import os

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

def log_sequence(prompt, chosen, rejected):
  current_date = datetime.today().strftime('%Y-%m-%d')

  # select counter from chat_logger
  iteration_counter = 2
  global current_row
  directory = "./"

  file_name = current_date + "-" + str(iteration_counter) + ".json"
  full_path = os.path.join(directory, file_name)
  # adds the opening [ if its a new batch
  if not os.path.exists(full_path):
    with open(full_path, "w") as fs:
      fs.write("[{" + f'"prompt" : "{prompt}",  "chosen" : "{chosen}", "rejected" : "{rejected}"' + "},")
  # adds a closing ] if its the final row of batch
  elif current_row == 15:
    with open(full_path, "a") as fs:
      fs.write("{" + f'"prompt" : "{prompt}",  "chosen" : "{chosen}", "rejected" : "{rejected}"' + "}]")
  # writes a row
  else:
    with open(full_path, "a") as fs:
      fs.write("{" + f'"prompt" : "{prompt}",  "chosen" : "{chosen}", "rejected" : "{rejected}"' + "},")


  fs.close()

  return True

"""
for i in range(16):

  current_row = i
  log_sequence("what is a operating system", "A operating system is x y z", "An operating system is something something else")

"""
import time

start = time.time()
dataset = load_ds(path="/home/shivesh/Documents/python/its_solution/data/json_output_1.json")

print(dataset[0]["chosen"])
print(dataset)

end = time.time()

print(end - start)
