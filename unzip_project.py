import os
import zipfile
import shutil

def unzip_java_project(zip_path, base_project_dir):
    """
    Extrait un projet Java dans un sous-dossier de 'springboot-projects'.
    
    Args:
        zip_path (str): Chemin vers le fichier ZIP
        base_project_dir (str): Répertoire de base du projet
    
    Returns:
        str: Chemin du répertoire du projet extrait
    """
    # Créer le dossier springboot-projects s'il n'existe pas
    springboot_projects_dir = os.path.join(base_project_dir, 'springboot-projects')
    os.makedirs(springboot_projects_dir, exist_ok=True)
    
    # Nom du projet (sans extension)
    project_name = os.path.splitext(os.path.basename(zip_path))[0]
    project_dir = os.path.join(springboot_projects_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)
    
    # Extraire le contenu du ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(project_dir)
    
    # Nettoyer la structure si nécessaire
    items = os.listdir(project_dir)
    subdirs = [item for item in items if os.path.isdir(os.path.join(project_dir, item))]
    
    if len(subdirs) == 1:
        subdir_path = os.path.join(project_dir, subdirs[0])
        for item in os.listdir(subdir_path):
            shutil.move(os.path.join(subdir_path, item), project_dir)
        os.rmdir(subdir_path)
    
    return project_dir

# Exemple d'utilisation
if __name__ == "__main__":
    base_project_dir = os.getcwd()  # Répertoire courant du projet
    uploaded_zip = "projet_SI_gestion_ECM.zip"
    project_dir = unzip_java_project(uploaded_zip, base_project_dir)
    print(f"Projet extrait dans : {project_dir}")