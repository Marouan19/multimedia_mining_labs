import cv2
import numpy as np

# Point Centre et point bord du cercle
params = {
    'x0': -1,
    'y0': -1,
    'x1': -1,
    'y1': -1,
    'Pressed': False
}

# Charger l'image
img = cv2.imread('../img/img_1.png', 1)

if img is None:
    print("Erreur: Impossible de charger l'image.")
    exit()

# Créer une image vide (noire)
img_blank = np.zeros(img.shape, np.uint8)


# Remplacer l'intérieur du disque par du blanc
def traitement():
    tmpImg = np.zeros(img.shape, np.uint8)
    x = params['x1'] - params['x0']
    y = params['y1'] - params['y0']
    rayon = np.int32(np.linalg.norm([x, y]))

    # Dessiner le cercle blanc sur l'image vide (noire ailleurs)
    cv2.circle(tmpImg, (params['x0'], params['y0']), rayon, (255, 255, 255), -1)

    # Appliquer ce masque blanc à l'image vide
    global img_blank
    img_blank[tmpImg[:, :, 0] == 255] = [255, 255, 255]  # Mettre la zone du cercle en blanc


# Déssiner le cercle (apercu)
def dessinerCercle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        params['x0'] = x
        params['y0'] = y
        params['Pressed'] = True
    elif event == cv2.EVENT_LBUTTONUP:
        params['Pressed'] = False
        traitement()
        cv2.imshow('InvSelect', img_blank)  # Montrer l'image modifiée avec le cercle blanc
    elif event == cv2.EVENT_MOUSEMOVE and params['Pressed']:
        params['x1'] = x
        params['y1'] = y
        rayon = np.int32(np.linalg.norm([params['x1'] - params['x0'], params['y1'] - params['y0']]))
        imgbis = img.copy()
        cv2.circle(imgbis, (params['x0'], params['y0']), rayon, (100, 0, 0), 2)  # Cercle temporaire en couleur
        cv2.imshow('InvSelect', imgbis)


def main():
    cv2.namedWindow('InvSelect')
    cv2.imshow('InvSelect', img)
    # Gestion de la souris
    cv2.setMouseCallback('InvSelect', dessinerCercle)

    while True:
        if cv2.waitKey(20) & 0xFF == 27:  # 'Esc' pour quitter
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
