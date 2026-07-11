# Test technique – Ingénieur Vision

## Introduction

L'objectif de ce projet est de concevoir un système de vision permettant de détecter des pièces plastiques rouges et bleues sur un convoyeur afin de permettre leur préhension par un robot.

Ce document présente une première proposition d'architecture, les hypothèses retenues, les principaux risques techniques ainsi qu'une stratégie de validation adaptée au besoin.

## Analyse du besoin

Les principales exigences identifiées sont les suivantes :

### Exigences fonctionnelles

- Identifier la référence de chaque pièce selon les critères de tri définis par le client. Dans le cas présent, la couleur rouge ou bleue constitue une information discriminante disponible.
- Estimer la pose de chaque pièce à traiter, au minimum sa position et, si nécessaire pour la préhension, son orientation.
- Transmettre au robot la catégorie de la pièce, sa pose et les informations nécessaires à la synchronisation avec le convoyeur.
- Permettre l’ajout ou le changement d’une référence produit avec un minimum de modification du système.

### Contraintes techniques

- La précision demandée est de ±0,1 mm.
- Les conditions d'éclairage ambiant sont variables.
- Les pièces sont transportées sur un convoyeur en mouvement continu.
- Certaines pièces présentent des surfaces brillantes susceptibles de générer des reflets.
- Le budget alloué au système de vision (caméra et éclairage) doit rester raisonnable.


## Points bloquants à clarifier

Avant de valider l’architecture, les éléments suivants doivent être précisés :

* **Précision attendue** : définir si les ±0,1 mm concernent la vision seule, la répétabilité ou l’erreur finale de préhension.
* **Dimensions et champ de vision** : connaître les dimensions des pièces, la zone à couvrir et la distance de travail afin de dimensionner caméra et optique.
* **Convoyeur et cadence** : confirmer la vitesse, les variations de vitesse, la cadence, la présence d’un encodeur et la capacité du robot à suivre le convoyeur.
* **Géométrie et préhension** : vérifier que les pièces restent à plat, que leur hauteur est maîtrisée et préciser la pose ainsi que le point de prise attendus par le robot.
* **Conditions optiques** : caractériser les reflets, le convoyeur et les possibilités de capotage, d’éclairage diffus, polarisé ou stroboscopique.

Sans ces informations, la faisabilité de la précision, la robustesse de la détection et le choix du matériel ne peuvent pas être garantis.


## Hypothèses

La proposition repose sur les hypothèses suivantes :

* les pièces sont rigides et reposent à plat sur le convoyeur ;
* pour dimensionner une architecture conservatrice, l’exigence de ±0,1 mm est provisoirement considérée comme une exigence sur la chaîne complète. Cette interprétation devra être validée avec le client, car elle implique la vision, la synchronisation, la calibration et le robot.
* les pièces sont bien séparées et ne se chevauchent pas ;
* chaque pièce visible peut être traitée comme une instance indépendante ;
* les références actuelles présentent une géométrie connue et stable ;
* la couleur rouge ou bleue constitue un critère utile à la classification, sans être considérée comme nécessairement suffisante à elle seule ;
* le robot doit recevoir une pose 2D (x, y, θ) ;
* le point de préhension est défini pour chaque référence dans un repère local associé à la pièce ;
* la hauteur des pièces varie suffisamment peu pour permettre une calibration sur le plan du convoyeur ;
* la caméra est montée de manière fixe et rigide au-dessus du convoyeur ;
* un éclairage dédié et des réglages d’acquisition fixes peuvent être utilisés ;
* le convoyeur dispose d’un encodeur permettant de rattacher chaque détection à une position physique ;
* le changement de référence est réalisé par chargement d’une configuration contenant les paramètres de classification, le modèle géométrique et le point de préhension.


## Proposition d'architecture

### Architecture matérielle

L'architecture proposée repose sur une caméra RGB fixe placée au-dessus du convoyeur, associée à un éclairage dédié afin de limiter l'influence des variations de lumière ambiante.

Le convoyeur étant en mouvement continu, le système est synchronisé avec celui-ci afin de pouvoir relier chaque détection à une position physique de la pièce. Une calibration permet ensuite de convertir les coordonnées image dans un repère exploitable par le robot.

Les principaux composants sont les suivants :

* une caméra industrielle RGB à obturateur global ;
* un objectif adapté au champ de vision et à la précision recherchée, avec un échantillonnage initial visé de l’ordre de 0,05 mm/pixel ou meilleur dans le plan objet. Cette valeur devra être confirmée par un budget d’erreur intégrant notamment la localisation dans l’image, les résidus de calibration, la variation de hauteur des pièces, la synchronisation avec le convoyeur et la répétabilité du robot ;
* un éclairage LED diffus, éventuellement stroboscopique si les essais mettent en évidence un flou de mouvement significatif ;
* un système de polarisation croisée, à évaluer pour limiter les reflets sur les pièces brillantes ;
* un capotage opaque autour de la zone d’acquisition afin de limiter l’influence de la lumière ambiante et de garantir des conditions d’éclairage reproductibles ;
* un encodeur de convoyeur permettant de suivre le déplacement des pièces entre l’acquisition et la préhension ;
* un ordinateur industriel assurant le traitement des images et la communication avec le robot ;
* le robot de préhension.


L'architecture fonctionnelle est illustrée ci-dessous:



                 Convoyeur
                     │
                     ▼
          ┌──────────┴──────────┐
          │                     │
      Encodeur              Pièces
          │                     │
          │              Caméra + éclairage
          │                     │
          └──────────┬──────────┘
                     ▼
              Acquisition image
          + lecture position encodeur
                     │
                     ▼
              Traitement d’image
                     │
                     ▼
              Segmentation des pièces
                     │
                     ▼
              Classification des pièces
                     │
                     ▼
              Estimation de pose des pièces
                     │
                     ▼
       Application de la calibration
        pixels → repère convoyeur/robot
                     │
                     ▼
      Compensation du déplacement
            du convoyeur
                     │
                     ▼
          Communication robot

La calibration est réalisée lors de l’installation du système, puis ses paramètres sont appliqués à chaque détection.


### Pipeline de traitement d'image

Le traitement proposé repose sur une approche déterministe, adaptée à un environnement contrôlé et à des pièces de géométrie connue.

Les étapes sont les suivantes :

1. **Acquisition de l'image**

   Une image RGB est acquise à l'aide d'une caméra industrielle. Les paramètres d'acquisition (temps d'exposition, gain, balance des blancs) sont fixés afin de garantir des conditions d'observation reproductibles.

2. **Prétraitement et calibration**

   L’image est corrigée de la distorsion optique à l’aide de la calibration intrinsèque de la caméra. Les coordonnées détectées sont ensuite converties du repère image vers le repère convoyeur, puis vers le repère robot, à l’aide des transformations calculées lors de l’installation.


3. **Segmentation des pièces**
   
   La segmentation vise à distinguer les pièces du fond du convoyeur, puis à extraire chaque pièce comme une région indépendante. La segmentation peut s’appuyer sur un espace colorimétrique adapté, comme HSV ou Lab, puis sur des seuils pour produire un masque binaire pièce/fond. Des opérations morphologiques permettent ensuite de supprimer le bruit et de séparer les régions détectées. Une image de référence du convoyeur vide peut également être utilisée pour renforcer la détection.
   

4. **Classification des pièces**

   Les pièces extraites sont classifiées à partir de caractéristiques colorimétriques et géométriques. Si le nombre de références ou la complexité des formes rend cette approche insuffisante, un modèle de classification supervisée pourra être envisagé, sous réserve de disposer d’un jeu de données annoté représentatif et de respecter les contraintes de cadence. L’estimation précise de la pose restera traitée séparément.


5. **Estimation de la pose des pièces**

   Pour chaque pièce isolée, le contour est extrait afin d’estimer sa géométrie. Selon la référence, le centroïde, les dimensions et une orientation principale peuvent être calculés directement. Pour une forme complexe ou lorsque ces descripteurs sont insuffisants, un matching géométrique avec un modèle de référence peut être utilisé afin d’estimer la translation et la rotation de la pièce, ainsi qu’un score de correspondance. Les éventuelles symétries doivent être prises en compte pour définir l’orientation réellement utile au robot.
   À ce stade, la pose est connue dans le repère image, puis convertie dans le repère convoyeur ou robot à l’aide des paramètres de calibration.


6. **Association de la pose à la position encodeur**

   L’acquisition est déclenchée matériellement, ou horodatée avec mémorisation de la valeur encodeur correspondant à l’exposition. Chaque pose est transmise avec cette position encodeur afin que le robot ou le contrôleur de suivi convoyeur puisse extrapoler la position jusqu’à l’instant de préhension.

7. **Transmission au robot**

   La catégorie de la pièce, sa pose et les informations nécessaires à la synchronisation sont transmises au robot.


## Risques techniques

* Précision insuffisante : l’objectif de ±0,1 mm peut être incompatible avec le champ de vision, la résolution, l’optique, la calibration ou la répétabilité du robot.
* Flou de mouvement : le déplacement continu du convoyeur peut dégrader le contour et donc l’estimation de la pose.
* Synchronisation imparfaite : une erreur entre l’instant d’acquisition et la prise robot peut produire un décalage important.
* Variations d’éclairage : la lumière ambiante peut modifier l’apparence des couleurs et perturber la segmentation.
* Reflets sur les pièces brillantes : ils peuvent créer des zones saturées, masquer le contour ou fausser la classification.
* Erreur liée à la hauteur des pièces : une calibration 2D unique devient inexacte si les surfaces observées ne sont pas dans le même plan.
* Instabilité mécanique : vibrations ou déplacement de la caméra peuvent invalider la calibration.
* Ambiguïté de forme : certaines géométries peuvent rendre l’orientation difficile ou indéterminée.
* Changement de référence mal maîtrisé : une nouvelle géométrie, couleur ou hauteur peut nécessiter une nouvelle configuration ou calibration.
* Détection non fiable transmise au robot : une mauvaise classification ou une pose erronée peut entraîner une prise incorrecte.


## Format des données transmises

Chaque pièce détectée est décrite par sa référence, sa pose, sa position encodeur, les informations de synchronisation avec le convoyeur et un score de confiance. Par exemple :

```json
{
  "id": 42,
  "reference": "piece_rouge",
  "pose": {
    "x_mm": 125.4,
    "y_mm": 83.7,
    "theta_deg": 32.1
  },
  "encoder_position": 184520,
  "timestamp": 1712345678,
  "confidence": 0.97,
  "frame": "conveyor",
  "status": "valid"
}
```

Le protocole et le format de sérialisation définitifs dépendront de l’interface disponible côté robot.

## Stratégie de validation

La validation doit être réalisée progressivement, d’abord sur chaque fonction du système, puis sur la chaîne complète jusqu’à la préhension robotique.

Un jeu de test représentatif sera constitué avec plusieurs pièces rouges et bleues, différentes orientations et positions dans le champ de vision, ainsi que des variations contrôlées d’éclairage, de vitesse du convoyeur et de reflets. Des cas dégradés seront également inclus : pièce partiellement visible, contraste faible, orientation ambiguë ou détection incertaine.

Les performances suivantes seront mesurées :

* taux de détection et de classification correcte ;
* erreur de position et d’orientation dans le repère robot ;
* répétabilité des mesures pour une même pièce ;
* robustesse aux variations d’éclairage et aux reflets ;
* temps de traitement et compatibilité avec la cadence du convoyeur ;
* taux de réussite de préhension.

La validation sera réalisée en deux étapes : une validation du système de vision, convoyeur à l'arrêt, afin de vérifier la précision de localisation et de calibration, puis une validation sur la cellule complète en fonctionnement, en mesurant le taux de réussite de la préhension et la précision globale du système sur un ensemble représentatif de pièces.

Enfin, un test d’endurance sera réalisé sur une série suffisamment longue de pièces afin d’identifier les erreurs intermittentes, les dérives de calibration et les problèmes de synchronisation. Les seuils d’acceptation devront être définis avec le client avant la validation finale.

## Bonus : évolution vers des pièces plus variées

Avec des formes plus variables et des couleurs moins discriminantes, une segmentation et une classification reposant principalement sur des seuils colorimétriques deviendraient moins fiables. L’approche devrait davantage exploiter la géométrie, la texture et l’apparence globale des pièces.

Selon le niveau de variabilité, on pourrait utiliser un matching géométrique plus avancé ou un modèle d’apprentissage supervisé pour détecter et classifier les pièces. Cela nécessiterait un jeu de données représentatif, comprenant les différentes références, orientations, conditions d’éclairage et défauts possibles.

L’estimation de pose resterait une étape distincte afin de fournir au robot une position précise et exploitable. Le changement de référence passerait alors davantage par l’ajout de nouvelles données et la mise à jour du modèle que par la simple modification de seuils ou de paramètres de configuration.

