import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Charger la matrice depuis le fichier CSV
df = pd.read_csv('content.csv')

# Afficher les types de données
print("Types de données dans le DataFrame :")
print(df.dtypes)

# Convertir les colonnes non numériques en numériques si nécessaire
# Exemple : convertissons les colonnes de type object en numériques
df = df.apply(pd.to_numeric, errors='coerce')

# Gérer les valeurs manquantes : suppression ou imputation
df_cleaned = df.dropna()  # Supprimer les lignes contenant des NaN

# Sélectionner uniquement les colonnes numériques
df_numeric = df_cleaned.select_dtypes(include=['float64', 'int64'])

# Initialiser le normaliseur MinMaxScaler pour normaliser entre -1 et 1
scaler = MinMaxScaler(feature_range=(0, 1))

# Normaliser la matrice
df_normalized = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)

# Ajouter les autres colonnes non numériques (si nécessaire) à la matrice normalisée
df_normalized = pd.concat([df_cleaned.drop(df_numeric.columns, axis=1), df_normalized], axis=1)

# Sauvegarder la matrice normalisée dans un nouveau fichier CSV
df_normalized.to_csv('content.csv', index=False)

print("\nLa matrice normalisée a été sauvegardée sous 'fichier_normalise.csv'.")
