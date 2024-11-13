import cv2
import numpy as np
from matplotlib import pyplot as plt

def build_filters():
    filters = []
    ksize = 15
    lambd = 10.0
    sigma = 5.0
    gamma = 0.5
    
    orientations = [0, 45, 90, 135]
    scales = [3, 5, 7]
    
    for theta in orientations:
        for scale in scales:
            kern = cv2.getGaborKernel((ksize, ksize), 
                                    sigma=sigma * scale/3,
                                    theta=theta*np.pi/180,
                                    lambd=lambd,
                                    gamma=gamma,
                                    psi=0,
                                    ktype=cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)
    return filters

def process_image(img, filters):

    features = []
    for kern in filters:
        filtered = cv2.filter2D(img, cv2.CV_8UC3, kern)
        features.append(filtered)
    return features

def extract_features(region, features):
    stats = []
    for feature in features:
        mean = np.mean(feature)
        std = np.std(feature)
        stats.extend([mean, std])
    return np.array(stats)

def compute_similarity(stats1, stats2):

    return np.sqrt(np.sum((stats1 - stats2)**2))

def extract_texture(image_path, x, y, width, height):
    # Lecture de l'image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Impossible de lire l'image")
    
    # Création des filtres de Gabor
    filters = build_filters()
    
    # Application des filtres à l'image entière
    features = process_image(img, filters)
    
    # Extraction de la région d'intérêt (ROI)
    roi = img[y:y+height, x:x+width]
    roi_features = process_image(roi, filters)
    roi_stats = extract_features(roi, roi_features)
    
    # Création de l'image résultat
    result = np.zeros_like(img)
    
    # Taille de la fenêtre glissante
    window_size = (height, width)
    
    # Parcours de l'image avec une fenêtre glissante
    for i in range(0, img.shape[0] - window_size[0], 4):
        for j in range(0, img.shape[1] - window_size[1], 4):
            window = img[i:i+window_size[0], j:j+window_size[1]]
            window_features = process_image(window, filters)
            window_stats = extract_features(window, window_features)
            
            # Calcul de la similarité
            similarity = compute_similarity(roi_stats, window_stats)
            
            # Seuillage de la similarité
            if similarity < 100:  # Ajuster ce seuil selon les besoins
                result[i:i+window_size[0], j:j+window_size[1]] = 255
    
    return result

# Fonction pour gérer la sélection de la région avec la souris
def select_roi(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    roi = cv2.selectROI("Sélectionner la région d'intérêt", img)
    cv2.destroyAllWindows()
    return roi

def main():
    # Chemin vers les images
    image_paths = ["Ex4/a.jpg", "Ex4/b.jpg", "Ex4/c.jpg"]
    
    for image_path in image_paths:
        # Sélection de la région d'intérêt
        x, y, w, h = select_roi(image_path)
        
        # Extraction de la texture
        result = extract_texture(image_path, x, y, w, h)
        
        # Affichage des résultats
        plt.figure(figsize=(12, 4))
        
        plt.subplot(131)
        plt.imshow(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), cmap='gray')
        plt.title('Image originale')
        
        plt.subplot(132)
        roi = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)[y:y+h, x:x+w]
        plt.imshow(roi, cmap='gray')
        plt.title('Région sélectionnée')
        
        plt.subplot(133)
        plt.imshow(result, cmap='gray')
        plt.title('Texture extraite')
        
        plt.show()

if __name__ == "__main__":
    main()