import json
import os
from pathlib import Path

def extract_method_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = content.splitlines()

    methods = []
    is_repository = '@Repository' in content or 'extends JpaRepository' in content

    if is_repository:
        methods.extend(['save', 'saveAll', 'findById', 'existsById', 'findAll', 
                       'deleteById', 'delete', 'deleteAll', 'count', 'findAllById'])
        
        for line in lines:
            cleaned_line = ' '.join(line.split()).split('//')[0]
            if ('Optional<' in cleaned_line or 'List<' in cleaned_line or 
                'void' in cleaned_line or 'boolean' in cleaned_line or 
                'int' in cleaned_line or 'long' in cleaned_line):
                if '(' in cleaned_line:
                    method_parts = cleaned_line.split('(')[0].split()
                    if len(method_parts) > 0:
                        method_name = method_parts[-1]
                        methods.append(method_name)
    else:
        for line in lines:
            cleaned_line = ' '.join(line.split()).split('//')[0]
            
            if 'public' in cleaned_line or 'private' in cleaned_line or 'protected' in cleaned_line:
                parts = cleaned_line.split()
                try:
                    is_static = 'static' in parts
                    index = next(i for i, part in enumerate(parts) 
                               if part in ['public', 'private', 'protected'])
                    
                    method_candidate = parts[index + (3 if is_static else 2)]
                    if '(' in method_candidate:
                        method_name = method_candidate.split('(')[0]
                        methods.append(method_name)
                except (IndexError, StopIteration):
                    continue

    return list(set(methods))

def analyze_java_directory(directory):
    path = Path(directory)
    all_results = []

    for file_path in path.rglob('*.java'):
        method_names = extract_method_names(file_path)
        if method_names:
            all_results.append({
                'file_path': str(file_path),
                'methods': method_names
            })

    return all_results

def save_results_to_json(results, filename='java_class_methods.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        print(f"Results saved to {filename}")
        
# Utilisation du script
directory = 'projet_SI_gestion_ECM'
results = analyze_java_directory(directory)
save_results_to_json(results)