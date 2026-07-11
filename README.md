# Test technique – Ingénieur Vision

## Introduction

L'objectif de ce projet est de concevoir un système de vision permettant de détecter des pièces plastiques rouges et bleues sur un convoyeur, de permettre leur préhension par un robot, puis de transmettre les informations nécessaires au robot avec la précision requise.

Ce document présente une première proposition d'architecture, les hypothèses retenues, les principaux risques techniques ainsi qu'une stratégie de validation adaptée au besoin.

## 1. Analyse du besoin

Le système de vision doit permettre de détecter des pièces plastiques rouges et bleues se déplaçant sur un convoyeur, d'estimer leur pose dans un repère exploitable par le robot, puis de transmettre ces informations de manière fiable afin de permettre leur préhension.

Les principales exigences identifiées sont les suivantes :

### Exigences fonctionnelles

- Identifier la catégorie ou la référence de chaque pièce selon les critères de tri définis par le client. Dans le cas présent, la couleur rouge ou bleue constitue une information discriminante disponible.
- Estimer la pose de chaque pièce à traiter, au minimum sa position et, si nécessaire pour la préhension, son orientation.
- Transmettre au robot la catégorie de la pièce, sa pose et les informations nécessaires à la synchronisation avec le convoyeur.
- Permettre l’ajout ou le changement d’une référence produit avec un minimum de modification du système.

### Contraintes techniques

- Les pièces sont transportées sur un convoyeur en mouvement continu.
- Les conditions d'éclairage ambiant sont variables.
- Certaines pièces présentent des surfaces brillantes susceptibles de générer des reflets.
- Le budget alloué au système de vision (caméra et éclairage) doit rester raisonnable.
- La précision demandée est de ±0,1 mm.


### Conséquences sur la conception

Ces contraintes conduisent à privilégier une solution robuste vis-à-vis des variations d'éclairage, reposant sur une calibration métrique rigoureuse et une synchronisation avec le convoyeur. La précision demandée devra être considérée comme une exigence portant sur l'ensemble du système (vision, calibration, convoyeur et robot), et non uniquement sur l'algorithme de traitement d'image.


## 2 Hypothèses

La proposition repose sur les hypothèses suivantes:

* les pièces sont rigides et reposent à plat sur le convoyeur ;
* les pièces sont bien séparées et ne se chevauchent pas ;
* chaque pièce visible peut être traitée comme une instance indépendante ;
* les références actuelles présentent une géométrie connue et stable ;
* la couleur rouge ou bleue constitue un critère utile à la classification, sans être considérée comme nécessairement suffisante à elle seule ;
* le robot doit recevoir une pose 2D ((x,y,\theta)) ;
* le point de préhension est défini pour chaque référence dans un repère local associé à la pièce ;
* la hauteur des pièces varie suffisamment peu pour permettre une calibration sur le plan du convoyeur ;
* la caméra est montée de manière fixe et rigide au-dessus du convoyeur ;
* un éclairage dédié et des réglages d’acquisition fixes peuvent être utilisés ;
* le convoyeur dispose d’un encodeur permettant de rattacher chaque détection à une position physique ;
* Le robot peut recevoir les données nécessaires à la préhension et à la synchronisation avec le convoyeur ;
* le changement de référence est réalisé par chargement d’une configuration contenant les paramètres de classification, le modèle géométrique et le point de préhension.


## 3. Risques techniques

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

## 4. Proposition d'architecture

### 4.1 Architecture matérielle

L'architecture proposée repose sur une caméra RGB fixe placée au-dessus du convoyeur, associée à un éclairage dédié afin de limiter l'influence des variations de lumière ambiante.

Le convoyeur étant en mouvement continu, le système est synchronisé avec celui-ci afin de pouvoir relier chaque détection à une position physique de la pièce. Une calibration permet ensuite de convertir les coordonnées image dans un repère exploitable par le robot.

Les principaux composants sont les suivants :

* une caméra industrielle RGB à obturateur global ;
* un objectif adapté au champ de vision et à la précision recherchée (pour une précision de 0.1mm, 1 pixel doit typiquement correspondre à 0.05mm ou moins);
* un éclairage LED diffus, avec possibilité d'un fonctionnement stroboscopique si les essais mettent en évidence un flou de mouvement significatif ;
* un encodeur convoyeur permettant de suivre le déplacement des pièces entre l'acquisition et la préhension ;
* un ordinateur industriel assurant le traitement des images et la communication avec le robot ;
* le robot de préhension.

L'architecture fonctionnelle est illustrée ci-dessous:

'''text

                 Convoyeur
                     │
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
       classification + estimation de pose
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
'''

### 4.2 Pipeline de traitement d'image

### 4.3 Estimation de la pose

### 4.4 Calibration

### 4.5 Communication avec le robot

## 5. Format des données transmises

## 6. Stratégie de validation

## 7. Bonus : évolution vers des pièces plus variées

## Annexes

- Schéma d'architecture
- Pseudo-code
- Exemple de message envoyé au robot


## 2. Points à clarifier

#### Règle de tri et références produit

* Quelle est la règle de tri exacte ?
* Toutes les pièces doivent-elles être saisies ?
* les pièces différentes doivent-elles être déposées dans des zones différentes ?
* Une référence produit correspond-elle à une couleur, à une géométrie, à des dimensions ou à une combinaison de plusieurs caractéristiques ?
* Combien de références doivent être prises en charge dans la première version ?
* Que signifie concrètement un changement de référence « facile » : sélection d’une configuration existante, apprentissage d’une nouvelle pièce ou ajout sans modification du code ?

#### Géométrie et disposition des pièces

* Quelles sont les dimensions minimales et maximales des pièces ?
* Les pièces d’une même référence ont-elles une géométrie et des dimensions constantes ?
* Les pièces reposent-elles toujours à plat sur le convoyeur ?
* Peuvent-elles être retournées ou présenter plusieurs faces visibles ?
* Leur hauteur est-elle constante ?
* Peuvent-elles se toucher, se chevaucher ou être partiellement masquées ?
* Quelle distance minimale sépare deux pièces ?
* Certaines pièces peuvent-elles se trouver partiellement hors du champ de vision ?

#### Préhension

* Le robot a-t-il besoin d’une position 2D ((x,y)) ou d’une pose complète ((x,y,\theta)) ?
* Le point de préhension correspond-il au centre géométrique de la pièce ?
* Le point de préhension dépend-il de la référence produit ?
* Certaines orientations sont-elles équivalentes en raison de la symétrie de la pièce ou de la pince ?
* Quelle est la tolérance acceptable sur l’orientation ?
* La préhension est-elle réalisée avec une ventouse, une pince mécanique ou un autre outil ?

#### Précision

* À quoi correspond exactement l’exigence de ±0,1 mm ?
* S’agit-il de la précision de la vision seule ou de l’erreur finale au point de préhension ?
* S’agit-il d’une erreur maximale, d’une répétabilité ou d’une valeur statistique ?
* Cette précision doit-elle être garantie sur l’ensemble du champ de vision ?
* Quelle est la précision et la répétabilité du robot ?
* Quelle précision est disponible sur la position du convoyeur ?
* Quel moyen de mesure sera utilisé pour valider cette exigence ?

#### Convoyeur et cadence

* Quelle est la vitesse nominale et maximale du convoyeur ?
* La vitesse est-elle constante ou variable ?
* Le convoyeur est-il équipé d’un encodeur accessible au système de vision et au robot ?
* Existe-t-il un signal de déclenchement matériel pour la caméra ?
* Quelle est la cadence maximale de pièces ?
* Quelle est la distance entre la zone d’acquisition et la zone de préhension ?
* Le robot dispose-t-il d’une fonction de suivi de convoyeur ?
* Quelles sont les latences acceptables entre l’acquisition, le traitement et la prise ?

#### Caméra et environnement

* Quelle surface doit être couverte par une image ?
* Quelle distance de travail est disponible au-dessus du convoyeur ?
* Existe-t-il des contraintes d’encombrement pour la caméra, l’objectif et l’éclairage ?
* Peut-on installer un capot afin de limiter l’influence de la lumière ambiante ?
* Peut-on utiliser un éclairage stroboscopique ?
* Les pièces brillantes présentent-elles des reflets localisés ou des zones fortement saturées ?
* Le convoyeur est-il uniforme en couleur et en texture ?
* Le convoyeur peut-il vibrer ou se déplacer latéralement ?

#### Interface avec le robot

* Dans quel repère les coordonnées doivent-elles être transmises ?
* Quel protocole de communication doit être utilisé ?
* Quelles données le robot attend-il en plus de la pose : identifiant, référence, score de confiance, horodatage, position encodeur ?
* Comment les pièces doivent-elles être ordonnées si plusieurs sont visibles simultanément ?
* Que doit faire le système lorsqu’une pièce ne peut pas être identifiée ou localisée avec suffisamment de confiance ?
* Le robot doit-il recevoir également une destination de dépôt ?

#### Validation et exploitation

* Quel taux de réussite de préhension est attendu ?
* Quel taux de mauvaise classification est acceptable ?
* Combien d’échantillons seront disponibles pour le développement et la validation ?
* Les variations entre lots de fabrication doivent-elles être prises en compte ?
* Qui sera chargé d’ajouter une nouvelle référence produit ?