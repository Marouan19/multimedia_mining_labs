import os
import cv2
import numpy as np
from sklearn.cluster import KMeans


# Fonction pour calculer les couleurs dominantes d'une image
def calculCouleursDominantes(image_path, num_colors=5):
    # Lire l'image
    img = cv2.imread(image_path)

    if img is None:
        print(f"Erreur lors du chargement de l'image : {image_path}")
        return None

    # Redimensionner pour accélérer le calcul
    img = cv2.resize(img, (100, 100))

    # Convertir en espace de couleur Lab (pour meilleure précision)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)

    # Convertir l'image en tableau de pixels (chaque pixel est un point 3D dans l'espace Lab)
    pixels = img_lab.reshape(-1, 3)

    # Appliquer KMeans pour trouver les couleurs dominantes
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=100)
    kmeans.fit(pixels)

    # Récupérer les centres des clusters, qui représentent les couleurs dominantes
    couleursDominantes = kmeans.cluster_centers_.astype(int)

    return couleursDominantes


# Fonction pour calculer la distance moyenne entre deux ensembles de couleurs
def calcul_dist(colors1, colors2):
    # Calcul de la somme des distances entre chaque paire de couleurs
    sommedistances = 0
    for color1 in colors1:
        for color2 in colors2:
            distance = np.linalg.norm(color1 - color2)
            sommedistances += distance

    # Calculer la moyenne des distances
    moyenneDistances = sommedistances / (len(colors1) * len(colors2))

    return moyenneDistances


# Chemin vers le dossier contenant les images
dossier = '../img/'

# Nombre de couleurs à calculer
nColors = 5

# Lecture des fichiers dans le dossier
fichiers = os.listdir(dossier)

# Liste pour stocker les couleurs dominantes de chaque image
colors = []

# Parcourir les fichiers et calculer les couleurs dominantes
for fichier in fichiers:
    # Filtrer pour ne traiter que les fichiers d'image (par exemple .jpg, .png)
    if fichier.endswith(('.jpg', '.jpeg', '.png')):
        couleursDominantes = calculCouleursDominantes(dossier + fichier, nColors)
        if couleursDominantes is not None:
            colors.append(couleursDominantes)

# Comparer les couleurs dominantes de chaque paire d'images
for i in range(len(colors)):
    for j in range(len(colors)):
        if i != j:
            d = calcul_dist(colors[i], colors[j])
            print(f"Distance ({fichiers[i]}, {fichiers[j]}) = {d:.2f}")
