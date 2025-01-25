# Projet de Décomposition d'un Monolithe en Microservices

## Introduction

Ce projet vise à décomposer une application monolithique Java (basée sur le framework Spring Boot) en une architecture de microservices. L'objectif principal est de rendre l'application plus modulaire, flexible et facile à maintenir en isolant les différentes fonctionnalités dans des microservices indépendants. Ce processus est entièrement automatisé à l'aide d'une pipeline Python qui analyse, génère des matrices de dépendances, et applique des techniques d'apprentissage automatique pour visualiser et regrouper les services en microservices.

## Objectifs du Projet

- **Décomposer un monolithe en microservices** : Analyser un projet Java monolithique, extraire les points d'entrée, et identifier les relations entre les différentes parties du système.
- **Générer des matrices de dépendance** : Créer des matrices qui représentent les relations entre les différentes classes et composants du projet.
- **Visualisation des relations entre les classes** : Utiliser des techniques de réduction de dimensions (comme PCA et t-SNE) pour visualiser les dépendances et les embeddings du projet.
- **Analyse d'héritage** : Évaluer les relations d'héritage entre les classes pour mieux comprendre leur interconnexion et potentiellement identifier les services communs.

## Fonctionnement de la Pipeline

La pipeline du projet suit plusieurs étapes clés pour analyser et transformer le monolithe en microservices :

### 1. **Extraction du Code Source**
Le code source du projet Java est extrait depuis un fichier ZIP et préparé pour l'analyse. Cela inclut le déballage du projet et la préparation des fichiers Java.

### 2. **Génération du Graphe de Dépendance**
Une analyse du projet permet de générer un graphe de dépendance des classes Java. Ce graphe permet d'extraire les différents noeuds "nodes" et connexions entre ces noeuds "edges", ainsi que l'assignation à chaque noeud un index avec lesquels les noeuds seront traités.

### 3. **Mise à Jour du Graphe de Dépendance**
Une fois le graphe généré, les chemins relatifs des fichiers Java sont mis à jour pour s'assurer que toutes les classes et leurs relations sont correctement référencées.

### 4. **Identification des Points d'Entrée**
Les points d'entrée du projet sont analysés pour identifier comment chaque partie du projet interagit et comment elles peuvent être isolées pour créer des microservices.

### 5. **Génération de Matrices de Dépendance**
Le projet génère une matrice d'adjacence qui représente les dépendances structurelles entre les classes. Ces matrices sont utilisées pour comprendre les relations entre les classes et pour aider à la classification des services.

### 6. **Analyse des Relations d'Héritage**
Les relations d'héritage entre les classes sont analysées et une matrice d'héritage symétrique est générée. Cela permet de visualiser les dépendances d'héritage et de mieux comprendre la hiérarchie des classes dans le projet.

### 7. **Analyse des Méthodes des Classes**
Une analyse détaillée des méthodes de chaque classe permet de collecter des informations sur les appels de méthodes, les types de données utilisés, et les attributs de chaque classe, ce qui est essentiel pour comprendre les interactions et potentiellement isoler les microservices.

### 8. **Analyse Complète du Projet avec Héritage**
Une analyse complète du projet prend en compte les relations d'héritage, les dépendances entre les classes et les points d'entrée pour fournir une vue d'ensemble des microservices potentiels à extraire du monolithe.

### 9. **Génération de la Matrice X**
Les matrices générées précédemment (matrices EP, C et inheritance) sont fusionnées pour créer une matrice X. Les lignes contenant uniquement des zéros sont supprimées afin de nettoyer les données avant l'entraînement du modèle.

### 10. **Entraînement du Modèle de Clustering**
Une fois la matrice X préparée, elle est utilisée pour entraîner un modèle de clustering. Ce modèle permet de regrouper les différentes classes en microservices en fonction de leurs interactions et dépendances.

### 11. **Visualisation des Embeddings et des Outliers**
Les embeddings des classes sont visualisés à l'aide de techniques de réduction de dimensions telles que PCA et t-SNE. Cela permet d'identifier visuellement les groupes de classes qui devraient être regroupés dans un même microservice.

### 12. **Visualisation du Graphe de Décomposition**
Le résultat final est visualisé sous forme de graphique représentant la décomposition du monolithe en microservices. Ce graphique montre les relations entre les différents services et leurs composants.

## Prérequis

Avant de commencer, assurez-vous que votre environnement est correctement configuré avec les outils et bibliothèques nécessaires :

- **Python 3.9.0**
- **Bibliothèques Python** : `numpy`, `json`, `javalang`, `subprocess`, `scikit-learn`, `matplotlib`, etc.

## Lancer la Pipeline

La pipeline est déclenchée à partir de l'upload du projet SpringBoot côté client (UI). Et donc toutes les étapes décrites ci-dessus, du déballage du projet à l'entraînement du modèle et à la visualisation des résultats vont être effectuées.