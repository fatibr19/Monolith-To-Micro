import re
from pathlib import Path
import json
from typing import Dict, List, Set, Optional, Any, Tuple
import numpy as np

from MethodParser import extract_all_info, extract_method_calls, perform_substitution
from StreamAndCoParser import extract_method_calls_from_stream

def load_json_data(file_path: str) -> Optional[dict]:
    """
    Loads JSON data from a file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"No file found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def extract_attributes(file_path: Path) -> Dict[str, str]:
    """
    Extract attributes and their types from a Java file.
    """
    attribute_pattern = re.compile(r"\b(private|protected|public)\s+(\w+[\w<>,\s]*)\s+(\w+);")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            java_code = file.read()
        return {
            match.group(3).strip(): match.group(2).strip()
            for match in attribute_pattern.finditer(java_code)
        }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}

def create_inheritance_map(inheritance_file: str, node_mapping_file: str) -> Dict[str, str]:
    """
    Creates a mapping from interface to implementation classes.
    """
    inheritance_data = load_json_data(inheritance_file)
    node_mapping = load_json_data(node_mapping_file)
    
    if not inheritance_data or not node_mapping:
        return {}
        
    # Create interface to implementation mapping
    interface_impl_map = {}
    for relation in inheritance_data['inheritance_relations']:
        parent_name = relation['parent']
        child_name = relation['child']
        
        if 'Service' in parent_name and 'Impl' in child_name:
            interface_impl_map[parent_name] = child_name
            
    print(f"Interface to Implementation mapping: {interface_impl_map}")
    return interface_impl_map

def extract_method_name_simple(declaration: str) -> str:
    """
    Extract method name from its declaration.
    """
    words = declaration.split()
    access_modifiers = {'public', 'protected', 'private', 'static'}
    
    if not words:
        return ""
        
    for i, word in enumerate(words):
        if '(' in word:
            return word.split('(')[0]
            
    return ""

def extract_stream_blocks(method_body: str) -> List[str]:
    """
    Extracts sections of code that involve stream operations.
    """
    lines = method_body.split('\n') if isinstance(method_body, str) else method_body
    
    stream_patterns = {
        '.stream()', 
        '.parallelStream()',
        'Stream.of(',
        'Stream.iterate(',
        'Stream.generate(',
        '.toStream()',
        'Arrays.stream(',
        'Collection.stream('
    }
    
    blocks = []
    current_block = []
    brace_count = 0
    in_stream = False
    
    for line in lines:
        stripped_line = line.strip()
        
        if any(pattern in line for pattern in stream_patterns) and not in_stream:
            in_stream = True
            current_block = [line]
            brace_count += line.count('{') - line.count('}')
            continue
            
        if in_stream:
            current_block.append(line)
            brace_count += line.count('{') - line.count('}')
            
            if ';' in line and brace_count <= 0:
                blocks.append('\n'.join(current_block))
                current_block = []
                in_stream = False
                brace_count = 0
            elif line.strip().endswith('.') or '->' in line or '::' in line:
                continue
    
    if current_block:
        blocks.append('\n'.join(current_block))
    
    return blocks

def transform_method_call(method_call: str, interface_impl_map: Dict[str, str]) -> str:
    """
    Transforms a method call to use implementation class if available.
    """
    if '.' not in method_call:
        return method_call
        
    obj, method = method_call.split('.', 1)
    for interface, impl in interface_impl_map.items():
        if interface == obj:
            return f"{impl}.{method}"
    return method_call

def parse_java_methods(file_path: Path, method_names: List[str], attribute_map: Dict[str, str], interface_impl_map: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Parse specified methods from a Java file and extract their method calls.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            java_code = file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return {name: [] for name in method_names}

    methods = {name: [] for name in method_names}
    in_method = False
    current_method = None
    method_body = []
    stack: List[Tuple[str, str]] = []

    for line in java_code.splitlines():
        stripped_line = line.strip()

        if any(name in stripped_line for name in method_names) and '{' in stripped_line:
            if not in_method:
                current_method = next((name for name in method_names if name in stripped_line), None)
                in_method = True
                method_body = [stripped_line]
                stack.append(('{', "start method"))
            else:
                method_body.append(stripped_line)
        
        elif in_method:
            method_body.append(stripped_line)
            if '{' in stripped_line:
                stack.append(('{', "other"))
            if '}' in stripped_line and stack:
                context = stack.pop()
                if context[1] == "start method":
                    full_method_body = "\n".join(method_body)
                    all_info = extract_all_info(full_method_body)
                    full_method_body = perform_substitution(full_method_body, all_info, attribute_map)
                    
                    current_method = extract_method_name_simple(full_method_body)
                    method_calls = set()

                    # Process stream operations
                    stream_blocks = extract_stream_blocks(full_method_body)
                    if stream_blocks:
                        stream_blocks_str = "\n".join(stream_blocks)
                        stream_calls = extract_method_calls_from_stream(stream_blocks_str)
                        method_calls.update(stream_calls)
                        
                        # Process non-stream code
                        remaining_code = full_method_body
                        for block in stream_blocks:
                            remaining_code = remaining_code.replace(block, '')
                            
                        standard_calls = set(f"{m[0]}.{m[1]}" for m in extract_method_calls(remaining_code))
                        
                        # Filter stream-related calls
                        standard_calls = {call for call in standard_calls 
                                        if not call.lower().endswith('.stream') 
                                        and 'collectors.' not in call.lower()
                                        and '.collect(' not in call.lower()
                                        and '.filter(' not in call.lower()}
                                        
                        # Transform interface calls to implementation calls
                        transformed_calls = {transform_method_call(call, interface_impl_map) 
                                          for call in standard_calls}
                        method_calls.update(transformed_calls)
                    else:
                        standard_calls = set(f"{m[0]}.{m[1]}" for m in extract_method_calls(full_method_body))
                        transformed_calls = {transform_method_call(call, interface_impl_map) 
                                          for call in standard_calls}
                        method_calls.update(transformed_calls)
                    
                    if current_method in methods:
                        methods[current_method] = list(method_calls)
                    
                    in_method = False
                    current_method = None
                    method_body = []
    return methods

def analyze_project(json_data: List[dict], inheritance_file: str, node_mapping_file: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Analyzes Java files with inheritance relationships considered.
    """
    interface_impl_map = create_inheritance_map(inheritance_file, node_mapping_file)
    project_report = {}
    
    for item in json_data:
        file_path = Path(item['file_path'].replace('\\', '/'))
        if file_path.exists():
            attribute_map = extract_attributes(file_path)
            methods = item['methods']
            project_report[str(file_path)] = parse_java_methods(
                file_path,
                methods,
                attribute_map,
                interface_impl_map
            )
        else:
            print(f"File not found: {file_path}")
    
    return project_report

def save_analysis_to_json(data: dict, file_name: str) -> None:
    """
    Saves analysis data to a JSON file.
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {file_name}")
    except Exception as e:
        print(f"Failed to save data: {e}")

def main():
    # Configuration files
    json_file_path = 'java_class_methods.json'
    inheritance_file = 'inheritance_relations.json'
    node_mapping_file = 'node_mapping.json'
    
    # Load input data
    json_data = load_json_data(json_file_path)

    if json_data:
        # Perform analysis with inheritance
        project_analysis = analyze_project(json_data, inheritance_file, node_mapping_file)
        
        # Save results
        output_file = 'project_analysis_results_with_inheritance.json'
        save_analysis_to_json(project_analysis, output_file)
        print(f"Analysis completed and saved to {output_file}")
    else:
        print("Failed to load or invalid JSON data.")

if __name__ == "__main__":
    main()