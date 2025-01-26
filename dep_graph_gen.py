import os
import json
import javalang
from pathlib import Path

class SpringBootAnalyzer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.nodes = []
        self.edges = []
        self.node_id_map = {}
        self.import_map = {}
        self.next_id = 1
        self.excluded_classes = set()

    def should_exclude_class(self, node, package_name=""):
        # Check for embedded annotations
        has_embedded = any(
            annotation.name in ['Embeddable', 'EmbeddedId','SpringBootApplication','SpringBootTest']
            for annotation in node.annotations if hasattr(annotation, 'name')
        )
        
        # Check if it's a Builder class (either inner or standalone)
        is_builder = (
            node.name == "Builder" or 
            node.name.endswith("Builder") or
            any(isinstance(parent, javalang.tree.ClassDeclaration) for parent in getattr(node, '_position', []))
        )
        
        # Check if it's an inner class of an excluded class
        is_inner = any(
            isinstance(parent, javalang.tree.ClassDeclaration) and 
            f"{package_name}.{parent.name}" in self.excluded_classes
            for parent in getattr(node, '_position', [])
        )
        
        return has_embedded or is_builder or is_inner

    def analyze_java_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        try:
            tree = javalang.parse.parse(content)
            package_name = tree.package.name if tree.package else ""
            imports = {imp.path.split('.')[-1]: imp.path for imp in tree.imports}
            self.import_map.update(imports)

            # First pass: identify excluded classes
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                if self.should_exclude_class(node, package_name):
                    full_class_name = f"{package_name}.{node.name}"
                    self.excluded_classes.add(full_class_name)
                    self.excluded_classes.add(node.name)

            # Second pass: process remaining classes
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                full_class_name = f"{package_name}.{node.name}"
                if full_class_name in self.excluded_classes or node.name in self.excluded_classes:
                    continue

                class_id = self.get_node_id(full_class_name)

                if node.extends:
                    extends_name = self.resolve_class_name(node.extends.name, package_name)
                    if extends_name not in self.excluded_classes:
                        extends_id = self.get_node_id(extends_name)
                        self.add_relationship(class_id, extends_id)

                for field_path, field in tree.filter(javalang.tree.FieldDeclaration):
                    field_type = self.resolve_class_name(field.type.name, package_name)
                    if field_type not in self.excluded_classes:
                        field_id = self.get_node_id(field_type)
                        self.add_relationship(class_id, field_id)

                for method_path, method in tree.filter(javalang.tree.MethodDeclaration):
                    if method.return_type:
                        return_type = self.resolve_class_name(method.return_type.name, package_name)
                        if return_type not in self.excluded_classes:
                            return_id = self.get_node_id(return_type)
                            self.add_relationship(class_id, return_id)

                    for param in method.parameters:
                        param_type = self.resolve_class_name(param.type.name, package_name)
                        if param_type not in self.excluded_classes:
                            param_id = self.get_node_id(param_type)
                            self.add_relationship(class_id, param_id)

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    def get_node_id(self, class_name):
        if class_name not in self.node_id_map:
            self.node_id_map[class_name] = str(self.next_id)
            self.next_id += 1
            self.nodes.append({
                "id": self.node_id_map[class_name],
                "label": class_name,
                "entity_type": "class"
            })
        return self.node_id_map[class_name]

    def resolve_class_name(self, class_name, package_name):
        if class_name in self.import_map:
            return self.import_map[class_name]
        if '.' not in class_name:
            return f"{package_name}.{class_name}"
        return class_name

    def add_relationship(self, start_id, end_id):
        if start_id == end_id:
            return

        start_class = next((node['label'] for node in self.nodes if node['id'] == start_id), "")
        end_class = next((node['label'] for node in self.nodes if node['id'] == end_id), "")

        if any(pkg in start_class or pkg in end_class for pkg in ("java.", "javax.", "org.springframework.", "com.fasterxml.jackson.", "lombok.")):
            return

        for edge in self.edges:
            if edge["properties"]["start"] == start_id and edge["properties"]["end"] == end_id:
                edge["frequency"] += 1
                return

        self.edges.append({
            "properties": {"start": start_id, "end": end_id},
            "frequency": 1
        })

    def analyze(self):
        for java_file in self.root_path.rglob("*.java"):
            if not any(exclude in str(java_file) for exclude in ['./test/', 'target/', 'build/']):
                # print(f"Analyzing {java_file}")
                self.analyze_java_file(java_file)

        excluded_packages = {"java.", "javax.", "org.springframework.", "com.fasterxml.jackson.", "lombok."}
        excluded_types = {'int', 'long', 'double', 'float', 'boolean', 'char', 'byte', 'short', 'void', 'String', 'Long', 'Double', 'Float', 'Boolean', 'Integer'}

        filtered_nodes = [
            node for node in self.nodes
            if not any(node['label'].startswith(pkg) for pkg in excluded_packages)
            and not any(typ in node['label'] for typ in excluded_types)
            and not node['label'].endswith(".Builder")
            and not node['label'].split(".")[-1] == "Builder"
            and node['label'] not in self.excluded_classes
        ]

        id_map = {node['id']: str(index + 1) for index, node in enumerate(filtered_nodes)}

        for node in filtered_nodes:
            node['id'] = id_map[node['id']]

        filtered_edges = [
            edge for edge in self.edges
            if edge['properties']['start'] in id_map and edge['properties']['end'] in id_map
        ]
        for edge in filtered_edges:
            edge['properties']['start'] = id_map[edge['properties']['start']]
            edge['properties']['end'] = id_map[edge['properties']['end']]

        clusters = [{"nodes": list(id_map.values())}]

        result = {
            "nodes": filtered_nodes,
            "edges": [{"type": "inter_class_connections", "relationship": filtered_edges}],
            "clusters": clusters
        }

        return result
    def save_to_file(self, output_path):
        result = self.analyze()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

if __name__ == "__main__":
    analyzer = SpringBootAnalyzer("projet_SI_gestion_ECM")
    analyzer.save_to_file("dependency_graph.json")