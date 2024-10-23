import numpy as np
import cv2

# Fonction callback pour la Trackbar (peut rester vide)
def f(x):
    pass

def main():
    # Chargement de l'image en niveaux de gris
    a = cv2.imread("../img/img_1.png", 0)
    if a is None:
        print("Erreur: Impossible de charger l'image.")
        return

    cv2.imshow('Originale', a)

    # Seuil de binarisation initial
    seuil = 128
    b = np.uint8((a >= seuil) * 255)

    # Calcul de l'histogramme
    histSize = 256
    hist = cv2.calcHist([a], [0], None, [histSize], [0, histSize])

    # Dimensions de l'image de l'histogramme
    imHistW = 512
    imHistH = 400
    bord = 10
    binHistW = (imHistW - 2 * bord) / histSize

    # Image blanche pour dessiner l'histogramme
    histImage = np.ones((imHistH, imHistW), dtype=np.uint8) * 255

    # Normalisation de l'histogramme par rapport à la hauteur de l'image
    hist = cv2.normalize(hist, hist, 0, imHistH - bord, cv2.NORM_MINMAX)

    # Dessin de l'histogramme
    for i in range(1, histSize):
        cv2.line(histImage,
                 (int(bord + binHistW * (i - 1)), int(imHistH - bord - hist[i - 1])),
                 (int(bord + binHistW * i), int(imHistH - bord - hist[i])),
                 0)

    # Ajouter une bordure autour de l'histogramme
    cv2.rectangle(histImage, (bord, bord), (imHistW - bord, imHistH - bord), 0)

    # Créer une copie de l'image de l'histogramme pour y ajouter la ligne du seuil
    histImagePlusLigne = histImage.copy()
    cv2.line(histImagePlusLigne,
             (int(bord + binHistW * seuil), imHistH - bord),
             (int(bord + binHistW * seuil), bord), 128)

    # Affichage des résultats
    cv2.imshow('Binarisation', b)
    cv2.imshow('Histogramme', histImagePlusLigne)

    # Création de la Trackbar pour ajuster le seuil
    cv2.createTrackbar('Seuil : ', 'Histogramme', 0, 255, f)
    cv2.setTrackbarPos('Seuil : ', 'Histogramme', seuil)

    while True:
        # Récupérer la position de la trackbar
        seuil = cv2.getTrackbarPos('Seuil : ', 'Histogramme')

        # Recalculer la binarisation avec le nouveau seuil
        b = np.uint8((a >= seuil) * 255)
        cv2.imshow('Binarisation', b)

        # Recalculer l'histogramme avec la ligne correspondant au seuil
        histImagePlusLigne = histImage.copy()
        cv2.line(histImagePlusLigne,
                 (int(bord + binHistW * seuil), imHistH - bord),
                 (int(bord + binHistW * seuil), bord), 128)
        cv2.imshow('Histogramme', histImagePlusLigne)

        # Appuyer sur 'Esc' pour quitter
        if cv2.waitKey(100) & 0xFF == 27:
            break

    # Fermer les fenêtres
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
