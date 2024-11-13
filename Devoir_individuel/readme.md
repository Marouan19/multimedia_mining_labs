# Analyse des Images par Histogrammes et Couleurs Dominantes
Une implémentation Python pour l'analyse et la comparaison d'images basée sur leurs caractéristiques colorimétriques utilisant OpenCV.

## 🔍 Description du Projet
Ce projet implémente plusieurs techniques d'analyse d'images :
- **Histogrammes Couleurs** : Calcul et visualisation des distributions RGB
- **Couleurs Dominantes** : Extraction des couleurs principales (>95% de présence)
- **Calcul de Similarité** : Comparaison d'images basée sur leurs caractéristiques

## 📥 Installation
```bash
git clone https://github.com/Marouan19/multimedia_mining_labs.git
cd multimedia_mining_labs/Devoir_individuel
```

## 🏗️ Structure du Projet
```
Devoir_individuel/
├── code_source.ipynb
├── histograms.json
├── images/
│   └── DVI1/
└── README.md
```

## 🔧 Fonctionnalités Principales
### 1. Analyse des Histogrammes
- Calcul des histogrammes RGB
- Visualisation des distributions de couleurs
- Stockage des résultats dans un fichier JSON

### 2. Extraction des Couleurs Dominantes
- Utilisation de K-means (K>16)
- Identification des couleurs représentant 95% de l'image
- Nombre variable de couleurs dominantes par image

### 3. Calcul de Similarité
- Comparaison basée sur les histogrammes
- Comparaison basée sur les couleurs dominantes
- Distance globale combinant les deux approches

## 📊 Processus de Recherche d'Images
1. **Phase Offline**
   - Traitement du dossier de 16 images (4 par catégorie)
   - Calcul et stockage des caractéristiques

2. **Phase Online**
   - Sélection d'une image requête
   - Calcul des caractéristiques
   - Comparaison avec la base de données
   - Tri des résultats par similarité

## 🖼️ Visualisation des Résultats
```python
# Format d'affichage
|- Image Requête
|- Top 3 Images Similaires
   |- Image 1 (Distance: X.XX)
   |- Image 2 (Distance: X.XX)
   ...
```

## 🛠️ Comment Utiliser
```python
# Exemple d'utilisation du code
# Chargement d'une image
img = cv2.imread('path_to_image.jpg')

# Calcul de l'histogramme
histogram = calculate_histogram(img)

# Extraction des couleurs dominantes
dominant_colors = extract_dominant_colors(img, k=16)

# Calcul de similarité
similarity = calculate_similarity(query_image, database_image)
```

## 📈 Paramètres Importants
- **K-means** : K > 16 pour l'extraction des couleurs
- **Seuil de présence** : 95% pour les couleurs dominantes
- **Nombre de résultats** : 6 images similaires minimum

## 🗃️ Structure des Données
### Format du fichier histograms.json
```json
{
    "image_name": {
        "histogram": [...],
        "dominant_colors": [
            {"color": [R,G,B], "percentage": XX.XX},
            ...
        ]
    }
}
```

## 👨‍💻 Auteur
- **DAGHMOUMI Marouan**
  - MST: Intelligence Artificielle et Science des Données
  - Faculté des Sciences et Techniques - Tanger
  - Université Abdelmalek Essaâdi

### Encadré par
- **Pr. M'hamed AIT KBIR**

## 📝 Notes Importantes
- Les images doivent être au format RGB
- Le système est optimisé pour traiter des lots de 16 images
- Les résultats peuvent varier selon la méthode de distance choisie

---
*Pour plus d'information sur les autres projets de traitement d'images, visitez le [dépôt principal](https://github.com/Marouan19/multimedia_mining_labs).*

