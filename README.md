# TP1 : Ligne des toits - Diviser pour Régner

## Objectif du TP 

On veut dessiner la ligne des toits d'immeubles 
- **Entrée** : n immeubles (g, h, d) où g=gauche, h=hauteur, d=droite  
- **Sortie** : Ligne de toits sous forme de polyligne + fichier SVG

**Exemple** : 
- Immeubles : `(3,13,9), (1,11,5), (19,18,22), (3,6,7), (16,3,25), (12,7,16)`
- Ligne résultante : `(1,11)(3,13)(9,0)(12,7)(16,3)(19,18)(22,3)(25,0)`

### Q1.1

1) pas une ligne de toit car brisure entre (2,5) et (4,4)
2) Pas une ligne de toit car ça ne va pas en x croissant ( (2,0) À (1,4), de plus c’est une brisure)
3) Ligne de toit car elle vérifie toutes les contraintes (continue, en x croissant de gauche à droite)
4) pas une ligne de toit car pas en x croissant (6,7) à (5,0)
5) pas une ligne de toit car on revient sur ses pas (4,8) à (4,7) 

### Q1.2 : Conditions d'une ligne de toits
Une polyligne est une ligne de toits si :
- **Continue** : pas de rupture dans l'espace
- **Monotone** : x croissants de gauche à droite
- **Structure** : segments horizontaux et verticaux uniquement

### Q1.3
(1,0) (1,1)(5,1)(5,13)(9,13)(9,20)(12,20)(12,27)(16,27)(16,3)(19,3)(19,0)(22,0)(22,3)(25,3)(25,0)

Comment se fait la transfo ? Il faut décomposer pour faire en sorte que chaque couple de coordonnées partage une donnée en commun. L’abscisse du point qui suit avec l’ordonnée du point qui précéde




### Q2 : Approche par tableau de pixels
Il faut balayer sur un rectangle de dimension (max x – min x)* (max y – min y ) = complexité, pour chaque case (de longueur x = 1 et de hauteur y = 1), on considére ça comme un pixel, si ce carré = 1 alors c’est rempli, sinon c’est vide. La ligne de crête c’est la limite entre les 0 et 1. Pas besoin de savoir l’emplacement des immeubles


| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 |


Passage en 1D :

| 0 | 3 | 4 | 4 | 0 | 0 | 0 |



-> Principe : Créer un tableau 2D, marquer les pixels occupés, extraire la crête
-> Complexité : O((max_x - min_x) × (max_y - min_y))
-> Problème : Pseudo-polynomiale, dépend des valeurs des coordonnées, il faut d’abord construire le tableau et ensuite re-balayer le tableau pour avoir la ligne de crête 

### Q3 : Approche incrémentielle



### Principe
Construire la ligne en ajoutant les immeubles un par un. un immeuble est représenté par un quadruplet de tuples décomposé depuis (g,h,d): 
à partir de (g,h,d) on a (g,0)(g,h)(d,h)(d,0) 

on a une ligne de toit dèjà existante, le but est de remplacer les segments en fonction du triplet (g,h,d)
on doit trouver le point où on doit insérer la ligne de toit, sachant que c’est en x croissant, les x sont à gauche , on a donc la zone de changement entre g et d  


### Algorithme d'insertion
Pour insérer un immeuble `(g,h,d)` dans une ligne existante :

1. Copier la partie avant : (tous les points x < g)
2. Gérer le début : créer un mur vertical en x=g si changement de hauteur
3. Zone de changement : [g,d]** : prendre max(hauteur_existante, h) 
4. Gérer la fin : : créer un mur vertical en x=d si nécessaire
5. Copier le reste : (tous les points x > d)

### Complexité
- Par insertion : O(n) où n = nombre de points dans la ligne
- Total : O(n²) pour n immeubles
- Pourquoi O(n²) ? Dans le pire cas, chaque insertion parcourt toute la ligne existante

## Implémentation de l'algo

### Q4 : Algorithme de fusion

**Principe** : Fusionner deux lignes de toits comme dans le tri fusion.

```python
def fusion_lignes_toits(ligne1, ligne2):
    # Parcourir les deux lignes simultanément
    # À chaque position x : nouvelle_hauteur = max(h1, h2)
    # Complexité : O(n)
```

#### Pourquoi ça marche ?
- On maintient les hauteurs courantes `h1, h2` des deux lignes
- On traite les abscisses dans l'ordre croissant (comme tri fusion)
- À chaque x, la hauteur résultante = maximum des deux hauteurs
- Complexité O(n) car on parcourt chaque ligne une seule fois

#### Exemple :
- Ligne 1 : `(1,10)(5,6)(8,0)(10,8)(12,0)`
- Ligne 2 : `(2,12)(7,0)(9,4)(11,2)(14,0)`  
- Résultat : `(1,10)(2,12)(7,6)(8,0)(9,4)(10,8)(12,2)(14,0)`

### Q5 : Algorithme principal

**Structure diviser-pour-régner** :
```python
def ligne_toits_diviser_regner(immeubles):
    if len(immeubles) <= 1:
        return cas_de_base()
    
    # 1. DIVISER
    milieu = len(immeubles) // 2
    gauche = immeubles[:milieu] 
    droite = immeubles[milieu:]
    
    # 2. RÉGNER (appels récursifs)
    ligne_gauche = ligne_toits_diviser_regner(gauche)
    ligne_droite = ligne_toits_diviser_regner(droite)
    
    # 3. COMBINER
    return fusion_lignes_toits(ligne_gauche, ligne_droite)
```

## Q5 complexité 

**T(n) = 2T(n/2) + Θ(n)**

**Décomposition détaillée** :
- **2T(n/2)** : Deux appels récursifs sur des sous-listes de taille ⌊n/2⌋ et ⌈n/2⌉
- **Θ(n)** : Le coût de la fusion de deux lignes de longueur maximale n

**Justification du coût de fusion** :  
La fonction `fusion_lignes_toits` parcourt les deux lignes une seule fois avec deux pointeurs, créant au plus |ligne₁| + |ligne₂| points dans le résultat. Dans le pire cas, chaque ligne contient O(n) points, donc la fusion coûte exactement Θ(n).

### Master Theorem

**Forme générale** : T(n) = aT(n/b) + f(n)

**paramètres** :
- a = 2 (nombre de sous-problèmes)  
- b = 2 (facteur de division)
- f(n) = $\Theta(n)$ (coût de la fusion)

**Calcul du seuil critique** :  
$n^{log_b(a)} = n^{log₂(2)} = n^1 = n$

->f(n) = $\Theta(n) = \Theta(n^{log_b(a)})$, nous sommes dans le **cas 2** du Master Theorem.

**Conclusion** : **$T(n) = \Theta(n log n)$**

### Preuve intuitive de la complexité

**Structure en arbre de récursion** :
```
                    T(n)
                  /      \
              T(n/2)      T(n/2)
             /    \      /    \
         T(n/4) T(n/4) T(n/4) T(n/4)
         ...
```

**Analyse niveau par niveau** :
- **Hauteur de l'arbre** : h = ⌈log₂(n)⌉ (car on divise par 2 à chaque niveau)
- **Nombre de nœuds au niveau i** : 2^i
- **Taille des sous-problèmes au niveau i** : n/2^i  
- **Coût total au niveau i** : 2^i × Θ(n/2^i) = Θ(n)

**Coût total** :  
$\sum_{i=0}^{log₂(n)} \Theta(n) = \Theta(n) × (log₂(n) + 1) = \Theta(n log n)$

Cette complexité est **optimale** car :
1. Il faut examiner tous les n immeubles au moins une fois 
2. Le problème a une structure qui nécessite O(log n) comparaisons (similaire au tri)


## Utilisation

```python
# Exemple d'utilisation
immeubles = [(3,13,9), (1,11,5), (19,18,22), (3,6,7), (16,3,25), (12,7,16)]
ligne = ligne_toits_diviser_regner(immeubles)
ligne_vers_svg(ligne, "resultat.svg")
```

On obtient un algorithme en O(n log n), optimal pour ce problème !