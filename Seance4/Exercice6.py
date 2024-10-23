import cv2
import numpy as np

# Point centre du carré fixe de 1 cm x 1 cm
params = {
    'x0': -1,
    'y0': -1,
    'Pressed': False
}

# Charger l'image
img = cv2.imread('../img/img_1.png', 1)

if img is None:
    print("Erreur: Impossible de charger l'image.")
    exit()

# Créer une image vide (noire)
img_blank = np.zeros(img.shape, np.uint8)

# Paramètres pour calculer la taille du carré (1 cm en pixels)
dpi = 96  # Suppose que l'image a une résolution de 96 DPI (points par pouce)
cm_to_pixels = int(dpi / 2.54)  # 1 cm = 2.54 pouces, conversion en pixels
square_size = cm_to_pixels  # Taille du carré en pixels (1 cm x 1 cm)

# Détection des couleurs à l'intérieur du carré de 1 cm
def traitement():
    global img_blank
    img_blank = np.zeros(img.shape, np.uint8)

    # Définir les coordonnées du carré (fixe à 1 cm x 1 cm)
    x_min = max(0, params['x0'] - square_size // 2)
    y_min = max(0, params['y0'] - square_size // 2)
    x_max = min(img.shape[1], params['x0'] + square_size // 2)
    y_max = min(img.shape[0], params['y0'] + square_size // 2)

    # Extraire les pixels à l'intérieur du carré
    square_roi = img[y_min:y_max, x_min:x_max]

    # Calculer la plage de couleurs (min et max)
    min_color = np.min(square_roi, axis=(0, 1))  # Couleur minimale dans la sélection
    max_color = np.max(square_roi, axis=(0, 1))  # Couleur maximale dans la sélection

    # Créer un masque pour les pixels qui sont dans la plage de couleurs détectées
    mask = cv2.inRange(img, min_color, max_color)

    # Appliquer le masque sur l'image: pixels détectés deviennent blancs, les autres noirs
    img_blank[mask == 255] = [255, 255, 255]  # Pixels dans la plage de couleurs deviennent blancs
    img_blank[mask == 0] = [0, 0, 0]  # Pixels hors de la plage deviennent noirs


# Déssiner le carré (aperçu)
def dessinerCarre(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        params['x0'] = x
        params['y0'] = y
        params['Pressed'] = True
    elif event == cv2.EVENT_LBUTTONUP:
        params['Pressed'] = False
        traitement()
        cv2.imshow('InvSelect', img_blank)  # Montrer l'image modifiée avec les couleurs détectées
    elif event == cv2.EVENT_MOUSEMOVE and params['Pressed']:
        imgbis = img.copy()
        # Définir les coordonnées du carré pour le dessin
        x_min = max(0, x - square_size // 2)
        y_min = max(0, y - square_size // 2)
        x_max = min(img.shape[1], x + square_size // 2)
        y_max = min(img.shape[0], y + square_size // 2)
        cv2.rectangle(imgbis, (x_min, y_min), (x_max, y_max), (100, 0, 0), 2)  # Rectangle temporaire de 1 cm x 1 cm
        cv2.imshow('InvSelect', imgbis)


def main():
    cv2.namedWindow('InvSelect')
    cv2.imshow('InvSelect', img)
    # Gestion de la souris
    cv2.setMouseCallback('InvSelect', dessinerCarre)

    while True:
        if cv2.waitKey(20) & 0xFF == 27:  # 'Esc' pour quitter
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
