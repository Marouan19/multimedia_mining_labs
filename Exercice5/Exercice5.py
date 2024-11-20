import os
import cv2
import numpy as np
import json
from math import log10
from PIL import Image
import matplotlib.pyplot as plt


def convertir_gif_en_png(dossier_racine, extensions=".gif", dossier_sortie="converted_images"):
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    for sous_dossier, dossiers, fichiers in os.walk(dossier_racine):
        for fichier in fichiers:
            ext = os.path.splitext(fichier)[-1].lower()
            if ext == extensions:
                chemin_gif = os.path.join(sous_dossier, fichier)
                img = Image.open(chemin_gif)
                chemin_png = os.path.join(dossier_sortie, fichier.replace(extensions, ".png"))
                img.save(chemin_png, "png", optimize=True, quality=100)


def normaliser_vecteur(image, image_name=None, output_file="normalisation.json"):
    """
    Normalise une image ou un vecteur en ramenant les valeurs entre 0 et 1.
    Enregistre les calculs dans un fichier JSON.

    Args:
        image (numpy.ndarray): Image ou vecteur à normaliser
        image_name (str): Nom de l'image pour identification
        output_file (str): Nom du fichier JSON où enregistrer les calculs

    Returns:
        numpy.ndarray: Image ou vecteur normalisé
    """
    min_val = np.min(image)
    max_val = np.max(image)
    calculations = {
        "image_name": image_name,
        "min_value": float(min_val),
        "max_value": float(max_val),
        "normalization_formula": "normalized_value = (pixel_value - min_value) / (max_value - min_value)"
    }

    if max_val - min_val == 0:
        calculations["note"] = "No normalization performed (max == min)."
        normalized_image = image
    else:
        normalized_image = (image - min_val) / (max_val - min_val)

    # Enregistrer dans le fichier JSON
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(calculations)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    return normalized_image


def comparer_moments_hu(imageA, imageB, methode=1):
    eps = 1e-5
    d = 0
    momentsHuA = cv2.HuMoments(cv2.moments(imageA))
    momentsHuB = cv2.HuMoments(cv2.moments(imageB))

    for i in range(7):
        amA = abs(momentsHuA[i][0])
        amB = abs(momentsHuB[i][0])
        if amA > eps and amB > eps:
            smA = 1 if momentsHuA[i] > 0 else -1
            smB = 1 if momentsHuB[i] > 0 else -1
            amA = smA * log10(amA)
            amB = smB * log10(amB)
            if methode == 3:
                d = max(d, abs((amA - amB) / amA))
            else:
                d += abs(amB - amA)
    return d


def comparer_image_avec_autres(image_cible, images_path, top_n=3):
    image_cible_grayscale = cv2.imread(image_cible, cv2.IMREAD_GRAYSCALE)
    image_cible_normalisee = normaliser_vecteur(image_cible_grayscale, image_name=os.path.basename(image_cible))

    _, image_cible_binaire = cv2.threshold(image_cible_normalisee, 0.5, 1.0, cv2.THRESH_BINARY)

    distances = []
    for autre_image in images_path:
        if autre_image == image_cible:
            continue

        autre_image_grayscale = cv2.imread(autre_image, cv2.IMREAD_GRAYSCALE)
        autre_image_normalisee = normaliser_vecteur(autre_image_grayscale, image_name=os.path.basename(autre_image))
        _, autre_image_binaire = cv2.threshold(autre_image_normalisee, 0.5, 1.0, cv2.THRESH_BINARY)

        distance = comparer_moments_hu(image_cible_binaire, autre_image_binaire)
        distances.append({'image': autre_image, 'distance': distance})

    distances_tries = sorted(distances, key=lambda x: x['distance'])
    return distances_tries[:top_n]


def comparer_toutes_images(dossier_images, top_n=3):
    images = [os.path.join(dossier_images, f) for f in os.listdir(dossier_images) if f.endswith(".png")]

    for image_cible in images:
        correspondances = comparer_image_avec_autres(image_cible, images, top_n=top_n)
        print(f"\nImage cible : {os.path.basename(image_cible)}")

        for i, correspondance in enumerate(correspondances, 1):
            print(f"  {i}. {os.path.basename(correspondance['image'])} (Distance : {correspondance['distance']})")

        # Afficher l'image cible et ses correspondances visuellement
        plt.figure(figsize=(15, 5))
        plt.subplot(1, top_n + 1, 1)
        img_cible = plt.imread(image_cible)
        plt.imshow(normaliser_vecteur(img_cible), cmap='gray')
        plt.title("Image cible")

        for i, correspondance in enumerate(correspondances, 1):
            plt.subplot(1, top_n + 1, i + 1)
            img_corr = plt.imread(correspondance['image'])
            plt.imshow(normaliser_vecteur(img_corr), cmap='gray')
            plt.title(f"Similaire {i}")

        plt.tight_layout()
        plt.show()


def principale():
    dossier_source = "/Users/marouandgh/IdeaProjects/multi/Exercice5/Formes"
    dossier_converti = "converted_images"

    print("Conversion des images GIF en PNG...")
    convertir_gif_en_png(dossier_source, dossier_sortie=dossier_converti)

    print("\nComparaison des images normalisées...")
    comparer_toutes_images(dossier_converti, top_n=3)


if __name__ == "__main__":
    principale()
