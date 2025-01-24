# import re

# from MethodParser import delete_annotations, extract_all_info, perform_substitution, remove_comments

# def extract_stream_related_lines(java_code):
#     # Capturer les motifs de stream dans une instruction complète
#     pattern = re.compile(
#         r'(\.stream\(\)|\.parallelStream\(\)|\b(Stream|IntStream|LongStream|DoubleStream)\b|\.builder\(\)|\.parser\(\))',
#         re.DOTALL
#     )

#     # Initialisation
#     lines = java_code.split('\n')  # Diviser le code en lignes
#     accumulated_line = ''  # Accumuler les lignes pour former des instructions complètes
#     results = []  # Stocker les résultats

#     # Accumuler les lignes jusqu'à trouver un ';'
#     for line in lines:
#         stripped_line = line.strip()
#         accumulated_line += stripped_line  # Ajouter un espace pour éviter la fusion des mots
#         if ';' in stripped_line:  # Fin de l'instruction
#             if pattern.search(accumulated_line):  # Rechercher le motif dans l'instruction accumulée
#                 results.append(accumulated_line.strip())
#             accumulated_line = ''  # Réinitialiser pour la prochaine instruction

#     print("\nresult of extraction: ", results)
#     return results

# def transform_stream_methods(java_code):
#     i = 0
#     n = len(java_code)
#     in_stream = False
#     generic_type = None
#     result = ''
#     temp_var = ''
#     lambda_depth = 0  # Depth of lambda expressions to manage nested lambdas
    
#     while i < n:
#         if java_code[i] == '<':
#             # Extract generic type
#             j = i + 1
#             generic_type = ''
#             while java_code[j] != '>':
#                 generic_type += java_code[j]
#                 j += 1
#             i = j
#             result += '<' + generic_type + '>'
#             i += 1  # Skip the '>'
#             continue

#         if java_code[i:].startswith('.stream()') or java_code[i:].startswith('.parallelStream()'):
#             in_stream = True
#             stream_method = '.stream()' if java_code[i:].startswith('.stream()') else '.parallelStream()'
#             result += stream_method
#             i += len(stream_method)
#             continue

#         if java_code[i] == '(':
#             if in_stream and '->' in java_code[i:]:
#                 lambda_depth += 1
#                 arrow_index = java_code[i:].index('->') + i
#                 temp_var = java_code[i+1:arrow_index].strip().split()[-1]
#             result += '('
#             i += 1
#             continue

#         if java_code[i] == ')':
#             if lambda_depth > 0:
#                 lambda_depth -= 1
#                 if lambda_depth == 0:
#                     temp_var = ''  # Reset temporary variable after ending lambda
#             result += ')'
#             i += 1
#             continue

#         if java_code[i] == ';':
#             if in_stream:
#                 in_stream = False
#                 lambda_depth = 0  # Reset lambda depth at the end of the stream
#             result += ';'
#             i += 1
#             continue

#         if in_stream and temp_var and generic_type and lambda_depth > 0:
#             # Replace the temporary variable inside the lambda with the generic type
#             if java_code[i:i+len(temp_var)] == temp_var:
#                 result += generic_type
#                 i += len(temp_var)
#             else:
#                 result += java_code[i]
#         else:
#             result += java_code[i]
        
#         i += 1
#     print("test")

#     return result



# def main():
#     java_code = """
#     List<Candidat> filteredCandidats = candidats.stream()
#     .filter(candidat -> "Active".equals(candidat.getStatut()))
#     .map(candidat -> new ProcessedCandidat(candidat.getName()))
#     .collect(Collectors.toList())"""

#     # Clean up the code
#     clean_code = remove_comments(java_code)
#     print("\ncleaned code 1: ", clean_code)
#     clean_code = delete_annotations(clean_code)
#     print("\ncleaned code 2: ", clean_code)

#     # Extract method bodies
#     method_info = extract_all_info(clean_code)
#     print("\methods extraction : ", clean_code)

#     # We assume `attribute_dict` is known or extracted earlier from the class attributes
#     attribute_dict = {'candidatService': 'CandidatService', 'storageService': 'StorageService'}
#     # for var_name, var_type in attribute_dict.items():
#     #     attribute_dict[var_name] = 'List<Candidat>'  # Assume all are lists of Candidat for this example

#     # Substitute variables in the method body based on the stream operations
#     substituted_body = perform_substitution(clean_code, method_info, attribute_dict)
    
#     # Extract stream-related lines
#     stream_lines = extract_stream_related_lines(substituted_body)
#     print("\nStream-related Lines:")
#     for line in stream_lines:
#         print(transform_stream_methods(line))


# if __name__ == "__main__":
#     main()


import re

def extract_method_calls_from_stream(java_code):
    """
    Extrait les appels de méthodes pertinents des opérations stream, 
    en ignorant les méthodes utilitaires.
    """
    # Méthodes à ignorer car elles sont des utilitaires
    ignored_methods = {
        'stream', 'parallelStream', 'filter', 'map', 'collect', 'toList',
        'forEach', 'findFirst', 'findAny', 'count', 'distinct', 'sorted',
        'limit', 'skip', 'builder', 'parser'
    }
    
    # Classes utilitaires à ignorer
    ignored_classes = {
        'List', 'Set', 'Collection', 'Collections', 'Arrays', 'Stream',
        'Collectors', 'Optional', 'Objects', 'String', 'Integer', 'Long',
        'Double', 'Boolean', 'ResponseEntity', 'HttpStatus'
    }

    def extract_stream_block(code):
        """Extrait un bloc complet de stream jusqu'au point-virgule."""
        lines = []
        depth = 0
        in_stream = False
        
        for line in code.split('\n'):
            line = line.strip()
            if '.stream()' in line:
                in_stream = True
            
            if in_stream:
                lines.append(line)
                depth += line.count('(') - line.count(')')
                
                if ';' in line and depth <= 0:
                    return ' '.join(lines)
        return None

    def analyze_lambda_methods(lambda_expr):
        """Analyse les méthodes appelées dans une expression lambda."""
        method_calls = set()
        
        # Pattern pour capturer les appels de méthodes dans les lambdas
        method_pattern = re.compile(r'(\w+)\.(\w+)\(\)')
        matches = method_pattern.finditer(lambda_expr)
        
        for match in matches:
            var_name = match.group(1)
            method_name = match.group(2)
            
            # On ajoute l'appel si ce n'est pas une méthode utilitaire
            if method_name not in ignored_methods:
                # Pour les lambdas dans un stream, la variable fait référence au type générique
                generic_match = re.search(r'List<(\w+)>', java_code)
                if generic_match:
                    class_name = generic_match.group(1)
                    if class_name not in ignored_classes:
                        method_calls.add(f"{class_name}.{method_name}")
        
        return method_calls

    # Extraire les blocs de stream
    method_calls = set()
    stream_block = extract_stream_block(java_code)
    
    if stream_block:
        # Analyser les expressions lambda dans le stream
        lambda_matches = re.finditer(r'->([^,;]+)', stream_block)
        for match in lambda_matches:
            lambda_expr = match.group(1)
            method_calls.update(analyze_lambda_methods(lambda_expr))

    return list(method_calls)

# Exemple d'utilisation avec le code de getAllCandidats
def analyze_method(java_code):
    """Analyse une méthode Java complète."""
    return extract_method_calls_from_stream(java_code)

if __name__ == "__main__":
    # Test avec le code de getAllCandidats
    java_code = """
    @GetMapping("/getAll")
    public ResponseEntity<List<Candidat>> getAllCandidats(){
        List<Candidat> candidats = candidatService.getAllCandidats();
        List<Candidat> filteredCandidats = candidats.stream()
                .filter(candidat -> !("Refused".equals(candidat.getStatut()) || "Accepted".equals(candidat.getStatut())))
                .collect(Collectors.toList());
        return new ResponseEntity<>(filteredCandidats, HttpStatus.OK);
    }
    """
    
    method_calls = analyze_method(java_code)
    print("Appels de méthodes trouvés:", method_calls)