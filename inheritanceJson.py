import os
import json
import javalang
from pathlib import Path

class InheritanceAnalyzer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.inheritance_relations = []
        self.project_classes = set()

    def get_project_classes(self):
        """Collecte toutes les classes définies dans le projet"""
        for java_file in self.root_path.rglob("*.java"):
            if not any(exclude in str(java_file) for exclude in ['./test/', 'target/', 'build/']):
                try:
                    with open(java_file, 'r', encoding='utf-8') as file:
                        content = file.read()
                    tree = javalang.parse.parse(content)
                    if tree is not None:  # Vérification si l'arbre n'est pas None
                        for path, node in tree.filter(javalang.tree.ClassDeclaration):
                            self.project_classes.add(node.name)
                        # Ajout pour les interfaces
                        for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
                            self.project_classes.add(node.name)
                except Exception as e:
                    print(f"Info: Skipping class collection for {java_file}: {str(e)}")

    def analyze_java_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            tree = javalang.parse.parse(content)
            if tree is None:
                return

            # Analyse des classes
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                # Vérification de l'héritage via 'extends'
                if node.extends and node.extends.name in self.project_classes:
                    self.inheritance_relations.append({
                        "child": node.name,
                        "parent": node.extends.name,
                        "type": "extends"
                    })
                
                # Vérification de l'héritage via 'implements'
                if node.implements:
                    for interface in node.implements:
                        if interface.name in self.project_classes:
                            self.inheritance_relations.append({
                                "child": node.name,
                                "parent": interface.name,
                                "type": "implements"
                            })

            # Analyse des interfaces
            for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
                if node.extends:
                    for extended in node.extends:
                        if extended.name in self.project_classes:
                            self.inheritance_relations.append({
                                "child": node.name,
                                "parent": extended.name,
                                "type": "extends"
                            })

        except Exception as e:
            print(f"Info: Skipping analysis for {file_path}")

    def analyze(self):
        # Première passe : collecter toutes les classes du projet
        print("Collecting project classes...")
        self.get_project_classes()
        print(f"Found {len(self.project_classes)} classes/interfaces in the project")
        
        # Deuxième passe : analyser les relations d'héritage
        print("\nAnalyzing inheritance relations...")
        for java_file in self.root_path.rglob("*.java"):
            if not any(exclude in str(java_file) for exclude in ['./test/', 'target/', 'build/']):
                print(f"Analyzing {java_file}")
                self.analyze_java_file(java_file)

    def save_to_file(self, output_path):
        result = {
            "inheritance_relations": self.inheritance_relations
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"\nFound {len(self.inheritance_relations)} inheritance relations")
        print(f"Results saved to {output_path}")

if __name__ == "__main__":
    analyzer = InheritanceAnalyzer("projet_SI_gestion_ECM")
    analyzer.analyze()
    analyzer.save_to_file("inheritance_relations.json")