import json
from datasets import load_dataset

# path = "/content/drive/MyDrive/shivesh_mohamed_1039116_final_year_research/data/dpo_datasets"
path = "/home/shivesh/Documents/python/its_solution/data/json_output_1.json"
# file_name = f"{path}/json_output_0.json"
# print(file_name)
output = load_dataset('json', data_files=path, split='train')
print(output)

# for i in range(6):
#   file_name = f"{path}/json_output_{i}.json"
#   output = load_dataset('json', data_files=file_name, split='train')
#   print(output)