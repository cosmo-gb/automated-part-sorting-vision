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


## 2. Points à clarifier et hypothèses

* Quelle est exactement la règle de tri : toutes les pièces doivent-elles être saisies, certaines doivent-elles être ignorées, ou chaque catégorie doit-elle être dirigée vers une destination différente ?
* Une référence produit correspond-elle à une couleur, à une géométrie, ou à une combinaison de plusieurs caractéristiques ?
* L’orientation de la pièce est-elle nécessaire à la préhension, ou une position 2D suffit-elle ?


## 3. Risques techniques

## 4. Proposition d'architecture

### 4.1 Architecture matérielle

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