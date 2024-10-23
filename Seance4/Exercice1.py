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


# Eliminer la composante rouge à l'intérieur du disque
def traitement():
    tmpImg = np.zeros(img.shape, np.uint8)
    x = params['x1'] - params['x0']
    y = params['y1'] - params['y0']
    rayon = np.int32(np.linalg.norm([x, y]))
    cv2.circle(tmpImg, (params['x0'], params['y0']), rayon, (255, 255, 255), -1)

    # Inverser les couleurs dans la zone du cercle
    mask = tmpImg[:, :, 2] == 255
    img[mask, 2] = 255 - img[mask, 2]
    img[mask, 0] = 255 - img[mask, 0]
    img[mask, 1] = 255 - img[mask, 1]


# Déssiner le cercle
def dessinerCercle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        params['x0'] = x
        params['y0'] = y
        params['Pressed'] = True
    elif event == cv2.EVENT_LBUTTONUP:
        params['Pressed'] = False
        traitement()
        cv2.imshow('InvSelect', img)
    elif event == cv2.EVENT_MOUSEMOVE and params['Pressed']:
        params['x1'] = x
        params['y1'] = y
        rayon = np.int32(np.linalg.norm([params['x1'] - params['x0'], params['y1'] - params['y0']]))
        imgbis = img.copy()
        cv2.circle(imgbis, (params['x0'], params['y0']), rayon, (100, 0, 0), -1)
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
