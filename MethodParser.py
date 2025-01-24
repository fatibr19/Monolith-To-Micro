from pprint import pprint
import re

def remove_comments(code):
    # Supprimer les commentaires de bloc
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Supprimer les commentaires de ligne
    code = re.sub(r'//.*', '', code)
    return code

def readAnnotation(chaine_caractere):
    stack = []
    index_debut = -1
    index_fin = -1

    # Recherche du début de l'annotation
    index_debut = chaine_caractere.find('@')
    if index_debut == -1:
        return -1, -1  # Pas d'annotation trouvée

    # Recherche du début des paramètres de l'annotation
    index_fin = chaine_caractere.find('(', index_debut)
    if index_fin == -1:
        return -1, -1  # Pas de parenthèse ouvrante trouvée après @

    # Gestion des imbrications avec une pile
    for i in range(index_fin, len(chaine_caractere)):
        char = chaine_caractere[i]
        if char in '({':
            stack.append(char)
        elif char in ')}':
            if stack:
                last = stack.pop()
                if last == '(' and char == ')':
                    continue
                elif last == '{' and char == '}':
                    continue
        if not stack:
            index_fin = i
            break

    if stack:
        return -1, -1  # Annotation non fermée correctement

    return index_debut, index_fin + 1  # Inclusif pour l'index de fin

def delete_annotations(chaine_caractere):
    while True:
        index_debut, index_fin = readAnnotation(chaine_caractere)
        if index_debut == -1 or index_fin == -1:
            break
        chaine_caractere = chaine_caractere[:index_debut] + chaine_caractere[index_fin:]
    return chaine_caractere

def read_methode_parameter(chaine_caractere):
    stack = []
    index_debut = chaine_caractere.find('(')
    if index_debut == -1:
        return ''  # No parameters found or no parenthesis

    for i in range(index_debut, len(chaine_caractere)):
        char = chaine_caractere[i]
        if char == '(':
            stack.append(char)
        elif char == ')':
            if stack:
                stack.pop()
        if not stack:
            index_fin = i
            return chaine_caractere[index_debut+1:index_fin]  # Excludes the parentheses

    return ''  # In case of unbalanced parentheses or other errors

def extract_first_method_body(code):
    # Trouver la fin de la signature de la méthode (après la dernière parenthèse fermante de la signature)
    index_start = code.find(')')
    if index_start == -1:
        return ''  # Aucune méthode trouvée

    # Trouver l'accolade ouvrante après la fin de la signature de la méthode
    index_start = code.find('{', index_start)
    if index_start == -1:
        return ''  # Aucun corps de méthode trouvé

    # Initialiser la pile avec l'accolade ouvrante trouvée
    stack = ['{']
    end_index = index_start + 1

    # Parcourir le code à partir de l'accolade ouvrante
    while end_index < len(code) and stack:
        char = code[end_index]
        if char == '{':
            stack.append('{')
        elif char == '}':
            stack.pop()
        end_index += 1

    # Vérifier que toutes les accolades sont fermées
    if stack:
        return ''  # Les accolades ne sont pas correctement fermées

    # Extraire et retourner le corps de la méthode
    return code[index_start+1:end_index-1]  # Exclure les accolades extérieures

def extract_variables_from_method_body(method_body):
    # Regex pour capturer les déclarations de variables
    # \b assure que nous sommes à la limite d'un mot, pour éviter les correspondances partielles
    var_regex = re.compile(r'\b(\w[\w\s<>,]*)\s+(\w+)\s*(?:=|;)')
    matches = var_regex.findall(method_body)
    
    variables = {}
    for match in matches:
        var_type, var_name = match[0], match[1]
        # Nettoyer le type de variable pour enlever les espaces superflus
        var_type = ' '.join(var_type.split())
        variables[var_name] = var_type
    
    return variables

def extract_catch_blocks(method_body):
    # Regex pour capturer les blocs catch
    catch_regex = re.compile(r'catch\s*\((\w+)\s+(\w+)\)\s*\{')
    matches = catch_regex.findall(method_body)
    
    exceptions = []
    for match in matches:
        exception_type, exception_variable = match[0], match[1]
        exceptions.append((exception_type, exception_variable))
    
    return exceptions

def extract_all_info(chaine_caractere):
    # Remove annotations from the method
    chaine_caractere = delete_annotations(chaine_caractere)

    # Remove comments from the method
    chaine_caractere = remove_comments(chaine_caractere)
    
    # Extract method body and parameters
    body = extract_first_method_body(chaine_caractere)
    parameters = read_methode_parameter(chaine_caractere)
    
    # Extract variables from the method body
    variables = extract_variables_from_method_body(body)
    
    # Extract exceptions from catch blocks
    exceptions = extract_catch_blocks(body)
    
    # Prepare the list to compile all data
    all_data = []
    
    # Process parameters (assuming parameters are listed as 'Type variableName, Type variableName')
    if parameters:
        param_pairs = parameters.split(',')
        for param in param_pairs:
            parts = param.strip().split()
            if len(parts) >= 2:
                all_data.append((parts[0], parts[1]))  # Append (type, variable_name)
    
    # Add variable declarations
    for var_name, var_type in variables.items():
        all_data.append((var_type, var_name))  # Append (type, variable_name)
    
    # Add exceptions
    for exception_type, exception_variable in exceptions:
        all_data.append((exception_type, exception_variable))  # Append (type, variable_name)
    
    return all_data

def substitute_variables_with_classes(method_body, variables_dict, class_attributes):
    # Préparer le pattern pour identifier les noms de variables dans le corps de la méthode
    # Exclure les correspondances précédées par un '.' ou suivies par '('
    pattern = r'(?<!\.)\b(' + '|'.join(re.escape(key) for key in variables_dict.keys()) + r')\b(?!\()'
    
    # Fonction pour remplacer chaque correspondance par la classe associée
    def replace_match(match):
        var_name = match.group(0)
        # Retourner le type de classe associé à la variable si disponible
        return class_attributes.get(variables_dict.get(var_name, ''), var_name)
    
    # Remplacer dans le corps de la méthode
    substituted_body = re.sub(pattern, replace_match, method_body)
    return substituted_body

def perform_substitution(body, all_info, attribute_dict):
    # Créer un dictionnaire pour le mapping variable: type basé sur all_info
    var_to_class = {info[1]: attribute_dict.get(info[1], info[0]) for info in all_info}

    # Ajouter les attributs de classe avec leurs types correspondants
    var_to_class.update(attribute_dict)

    # Fonction pour remplacer chaque correspondance par la classe associée
    # Ajout de conditions pour exclure les appels de méthodes (précédés par '.' ou suivis par '(')
    def replacer(match):
        var_name = match.group(0)
        # Vérifier si le match est précédé par '.' ou suivi par '(' (dans le texte original)
        preceding_char = body[match.start() - 1] if match.start() > 0 else ''
        following_char = body[match.end()] if match.end() < len(body) else ''
        if preceding_char == '.' or following_char == '(':
            return var_name  # Retourner le nom original sans substitution
        return var_to_class.get(var_name, var_name)  # Remplacer si possible

    pattern = r'\b(' + '|'.join(re.escape(name) for name in var_to_class.keys()) + r')\b'
    substituted_body = re.sub(pattern, replacer, body)
    return substituted_body

def extract_method_calls(method_body):

    # Regex étendue pour inclure les appels de méthodes sur des variables ou classes, incluant les types génériques
    method_call_regex = re.compile(r'\b([A-Za-z0-9_]+(?:<[A-Za-z0-9_ ,]+>)?)\.([A-Za-z0-9_]+)\(')
    matches = method_call_regex.findall(method_body)
    
    method_calls = []
    for match in matches:
        class_or_instance, method_name = match
        method_calls.append((class_or_instance, method_name))
    
    return method_calls

if __name__=="__main__":
    # Example usage
    chaine_caractere = """@GetMapping("/getAll")
        public ResponseEntity<List<Candidat>> getAllCandidats(){
            List<Candidat> candidats = candidatService.getAllCandidats();
            // Filter out candidates with 'refused' and 'accepted' statuses
            List<Candidat> filteredCandidats = candidats.stream()
                    .filter(candidat -> !("Refused".equals(candidat.getStatut()) || "Accepted".equals(candidat.getStatut())))
                    .collect(Collectors.toList());
            return new ResponseEntity<>(filteredCandidats, HttpStatus.OK);
        }"""



    # Obtenir les informations et le corps de la méthode
    chaine_caractere = delete_annotations(chaine_caractere)
    
    body = extract_first_method_body(chaine_caractere)

    all_info = extract_all_info(chaine_caractere)

    # Dictionnaire des attributs (existant)
    attribute_dict =   {'candidatService': 'CandidatService','storageService':'StorageService'}
    # Appliquer la substitution
    substituted_body = perform_substitution(body, all_info, attribute_dict)
    print(substituted_body)
    method_and_classes_called = extract_method_calls(substituted_body)

    print("methode and classes called")
    print(method_and_classes_called)