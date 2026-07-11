## Annexes - Points à clarifier

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