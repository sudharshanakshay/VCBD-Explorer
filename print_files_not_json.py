import os

def print_non_json_files(directory):
    non_json_files = [f for f in os.listdir(directory) if not f.endswith('.json')]
    print(f"Total non-JSON files: {len(non_json_files)}")
    for file in non_json_files:
        print(file)

directory = 'C:/Users/sudharshan.acharya/Downloads/VCDB-master/VCDB-master/data/json/validated'
print_non_json_files(directory)