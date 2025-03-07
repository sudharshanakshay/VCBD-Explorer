import os
import json

def find_attribute_in_json(directory, key, limit=None):
    def find_key(data, key):
        if isinstance(data, dict):
            if key in data:
                return data[key]
            for k, v in data.items():
                result = find_key(v, key)
                if result is not None:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = find_key(item, key)
                if result is not None:
                    return result
        return None

    json_files = [f for f in os.listdir(directory) if f.lower().endswith('.json')]
    print(f'Total JSON files loaded: {len(json_files)}')
    count = 0

    for json_file in json_files:
        if limit is not None and count >= limit:
            break
        file_path = os.path.join(directory, json_file)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                data = data['victim']
                value = find_key(data, key)
                if value is not None:
                    print(f"File: {json_file}, {key}: {value}")
                count += 1
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {json_file}: {e}")

    print(f'Count: {count}')

# Example usage
directory = 'C:/Users/sudharshan.acharya/Downloads/VCDB-master/VCDB-master/data/json/validated'
key = 'your_key_here'
find_attribute_in_json(directory, key)