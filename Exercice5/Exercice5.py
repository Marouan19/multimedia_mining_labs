import os
import cv2
import numpy as np
from math import log10
from PIL import Image
import matplotlib.pyplot as plt


def convertir_gif_en_png(dossier_racine, extensions=".gif", dossier_sortie="converted_images"):
    """
    Convertit les images GIF en format PNG dans le répertoire spécifié et les stocke dans un sous-répertoire.

    Args:
        dossier_racine (str): Répertoire racine pour rechercher les images
        extensions (str, optionnel): Extension de fichier à convertir. Par défaut ".gif"
        dossier_sortie (str): Répertoire où les images PNG seront stockées.
    """
    # Créer le dossier de sortie si nécessaire
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Parcourir tous les sous-répertoires
    for sous_dossier, dossiers, fichiers in os.walk(dossier_racine):
        for fichier in fichiers:
            # Vérifier l'extension du fichier
            ext = os.path.splitext(fichier)[-1].lower()
            if ext in extensions:
                # Chemin complet du fichier GIF
                chemin_gif = os.path.join(sous_dossier, fichier)
                print(f"Traitement : {chemin_gif}")

                # Ouvrir et enregistrer en PNG dans le dossier de sortie
                img = Image.open(chemin_gif)
                chemin_png = os.path.join(dossier_sortie, fichier.replace(extensions, ".png"))
                img.save(chemin_png, "png", optimize=True, quality=100)
                print(f"Converti en : {chemin_png}")


def comparer_moments_hu(imageA, imageB, methode=1):
    """
    Compare deux images en utilisant les Moments de Hu avec différentes méthodes de calcul.

    Args:
        imageA (numpy.ndarray): Première image en niveaux de gris
        imageB (numpy.ndarray): Deuxième image en niveaux de gris
        methode (int, optionnel): Méthode de comparaison. Par défaut 1.

    Returns:
        float: Distance/différence entre les images

    Raises:
        Exception: Si les images ont des caractéristiques fondamentalement différentes
    """
    eps = 1e-5  # Petite valeur epsilon pour éviter la division par zéro
    anyA = False
    anyB = False
    d = 0

    # Calculer les Moments de Hu pour les deux images
    momentA = cv2.moments(imageA)
    momentB = cv2.moments(imageB)
    momentsHuA = cv2.HuMoments(momentA)
    momentsHuB = cv2.HuMoments(momentB)

    # Trois méthodes de comparaison différentes
    if methode == 1:
        # Méthode 1 : Échelle logarithmique avec normalisation basée sur le signe
        for i in range(7):
            amA = abs(momentsHuA[i][0])
            amB = abs(momentsHuB[i][0])

            if amA > 0: anyA = True
            if amB > 0: anyB = True

            smA = 1 if momentsHuA[i] > 0 else (-1 if momentsHuA[i] < 0 else 0)
            smB = 1 if momentsHuB[i] > 0 else (-1 if momentsHuB[i] < 0 else 0)

            if amA > eps and amB > eps:
                amA = 1.0 / (smA * log10(amA))
                amB = 1.0 / (smB * log10(amB))
                d += abs(amB - amA)

    elif methode == 2:
        # Méthode 2 : Comparaison à l'échelle logarithmique
        for i in range(7):
            amA = abs(momentsHuA[i][0])
            amB = abs(momentsHuB[i][0])

            if amA > 0: anyA = True
            if amB > 0: anyB = True

            smA = 1 if momentsHuA[i] > 0 else (-1 if momentsHuA[i] < 0 else 0)
            smB = 1 if momentsHuB[i] > 0 else (-1 if momentsHuB[i] < 0 else 0)

            if amA > eps and amB > eps:
                amA = smA * log10(amA)
                amB = smB * log10(amB)
                d += abs(amB - amA)

    elif methode == 3:
        # Méthode 3 : Méthode de différence relative
        for i in range(7):
            amA = abs(momentsHuA[i][0])
            amB = abs(momentsHuB[i][0])

            if amA > 0: anyA = True
            if amB > 0: anyB = True

            smA = 1 if momentsHuA[i] > 0 else (-1 if momentsHuA[i] < 0 else 0)
            smB = 1 if momentsHuB[i] > 0 else (-1 if momentsHuB[i] < 0 else 0)

            if amA > eps and amB > eps:
                amA = smA * log10(amA)
                amB = smB * log10(amB)
                mmm = abs((amA - amB) / amA)
                d = max(d, mmm)

    if anyA != anyB:
        raise Exception("Les images ont des caractéristiques fondamentalement différentes")

    return d


def comparer_et_afficher_images(chemin_image1, chemin_image2):
    """
    Compare deux images et affiche les résultats de manière visuelle.

    Args:
        chemin_image1 (str): Chemin de la première image
        chemin_image2 (str): Chemin de la deuxième image
    """
    # Lire les images en niveaux de gris
    imageA = cv2.imread(chemin_image1, cv2.IMREAD_GRAYSCALE)
    imageB = cv2.imread(chemin_image2, cv2.IMREAD_GRAYSCALE)

    # Appliquer un seuillage binaire
    _, imA = cv2.threshold(imageA, 128, 255, cv2.THRESH_BINARY)
    _, imB = cv2.threshold(imageB, 128, 255, cv2.THRESH_BINARY)

    # Calculer les différences en utilisant plusieurs méthodes
    d1 = comparer_moments_hu(imA, imB)
    d2 = comparer_moments_hu(imA, imB, 2)
    d3 = comparer_moments_hu(imA, imB, 3)

    return {
        'image1': chemin_image1,
        'image2': chemin_image2,
        'diff_methode1': d1,
        'diff_methode2': d2,
        'diff_methode3': d3
    }


def comparer_toutes_images(dossier_images, top_n=5):
    """
    Compare toutes les images dans un dossier donné avec toutes les autres images.

    Args:
        dossier_images (str): Répertoire contenant les images à comparer
        top_n (int, optionnel): Nombre de paires d'images les plus similaires à afficher
    """
    images = [f for f in os.listdir(dossier_images) if f.endswith(".png")]
    images_path = [os.path.join(dossier_images, img) for img in images]

    # Stocker les résultats de comparaison
    resultats = []

    # Comparer chaque image avec toutes les autres
    for i in range(len(images_path)):
        for j in range(i + 1, len(images_path)):
            resultats.append(comparer_et_afficher_images(images_path[i], images_path[j]))

    # Trier les résultats par similarité (moyenne des différences)
    resultats_tries = sorted(resultats,
                             key=lambda x: (x['diff_methode1'] + x['diff_methode2'] + x['diff_methode3']) / 3)

    # Afficher les top N paires d'images les plus similaires
    print(f"\nTop {top_n} paires d'images les plus similaires :")
    for i, resultat in enumerate(resultats_tries[:top_n], 1):
        print(f"\nPaire {i}:")
        print(f"Image 1: {os.path.basename(resultat['image1'])}")
        print(f"Image 2: {os.path.basename(resultat['image2'])}")
        print(f"Différence Méthode 1 : {resultat['diff_methode1']}")
        print(f"Différence Méthode 2 : {resultat['diff_methode2']}")
        print(f"Différence Méthode 3 : {resultat['diff_methode3']}")

    # Afficher visuellement les images les plus similaires
    plt.figure(figsize=(15, 5 * top_n))
    for i, resultat in enumerate(resultats_tries[:top_n], 1):
        plt.subplot(top_n, 2, 2 * i - 1)
        img1 = plt.imread(resultat['image1'])
        plt.imshow(img1, cmap='gray')
        plt.title(f"Image 1 : {os.path.basename(resultat['image1'])}")

        plt.subplot(top_n, 2, 2 * i)
        img2 = plt.imread(resultat['image2'])
        plt.imshow(img2, cmap='gray')
        plt.title(f"Image 2 : {os.path.basename(resultat['image2'])}")

    plt.tight_layout()
    plt.show()


def principale():
    """
    Fonction principale pour démontrer la fonctionnalité du script
    """
    # Convertir GIF en PNG et les stocker dans un sous-répertoire
    convertir_gif_en_png("/Users/marouandgh/IdeaProjects/multi/Exercice5/Formes", dossier_sortie="converted_images")

    # Comparer toutes les images du dossier et afficher les plus similaires
    comparer_toutes_images("converted_images", top_n=5)


if __name__ == "__main__":
    principale()