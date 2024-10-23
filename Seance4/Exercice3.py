import cv2
from matplotlib import pyplot as plt


def main():
    # Lecture de l'image
    img = cv2.imread("../img/img_1.png", 1)

    if img is None:
        print("Erreur: Impossible de charger l'image.")
        return

    # Affichage de l'image originale
    cv2.imshow("Image originale", img)

    # Récupérer chaque canal séparément
    chans = cv2.split(img)
    colors = ("b", "g", "r")

    # Configuration du graphique pour l'histogramme
    plt.figure()
    plt.title("Histogramme couleur")
    plt.xlabel("Bins")
    plt.ylabel("Nombre de Pixels")

    # Boucle sur chaque canal et couleur
    for (chan, color) in zip(chans, colors):
        # Créer l'histogramme du canal courant
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    # Affichage de l'histogramme
    plt.show()

    # Attendre une interaction utilisateur avant de fermer les fenêtres
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
