
import json
import re
from pathlib import Path

def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def find_matching_brace(content, start_index):
    stack = []
    for i in range(start_index, len(content)):
        if content[i] == '{':
            stack.append('{')
        elif content[i] == '}':
            if len(stack) == 1:  # Closing the block of the method we're interested in
                return i
            stack.pop()
    return -1  # No matching closing brace found

def extract_method_details(block):
    calls = re.findall(r'\b(\w+)\.\w+\(', block)
    classes_used = re.findall(r'\bnew\s+(\w+)\(', block)
    attributes = re.findall(r'\b(private|public|protected)\s+(\w+)\s+(\w+);', block)
    return list(set(calls)), list(set(classes_used)), attributes

def parse_java_file(file_path, method_names):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    method_details = {method: {'calls': [], 'classes_used': [], 'attributes': []} for method in method_names}
    method_signature_pattern = r'(public|protected|private)\s+\w+\s+(\w+)\s*\(([^)]*)\)\s*{'

    for match in re.finditer(method_signature_pattern, content, re.DOTALL):
        access_modifier, method_name, params = match.groups()
        if method_name in method_names:
            start_index = match.start()
            end_index = find_matching_brace(content, match.end() - 1)
            if end_index != -1:
                method_block = content[start_index:end_index + 1]
                calls, classes_used, attributes = extract_method_details(method_block)
                method_details[method_name] = {
                    'calls': calls,
                    'classes_used': classes_used,
                    'attributes': attributes
                }

    return method_details

def update_json_data(json_data):
    for item in json_data:
        file_path =  item['file_path']
        methods = item['methods']
        method_details = parse_java_file(file_path, methods)
        
        for method in methods:
            if method in method_details:
                item[method] = method_details[method]

def save_json_data(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Usage
json_filepath = 'java_class_methods.json'
project_directory = 'springboot-projects/projet_SI_gestion_ECM'
json_data = load_json_data(json_filepath)
update_json_data(json_data)
save_json_data(json_data, 'updated_java_class_methods.json')
