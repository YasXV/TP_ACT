def fusion_lignes_toits(ligne1, ligne2):
    """
    Q4: Fusionne deux lignes de toits en O(n)
    
    Args:
        ligne1: Liste de tuples (x, y) représentant la première ligne de toits
        ligne2: Liste de tuples (x, y) représentant la deuxième ligne de toits
    
    Returns:
        Liste de tuples (x, y) représentant la ligne de toits fusionnée
    
    Principe: À chaque abscisse x, on prend max(hauteur_ligne1, hauteur_ligne2)
    """
    #cas de base
    if not ligne1:
        return ligne2
    if not ligne2:
        return ligne1
    
    resultat = []
    i = j = 0  # Indices pour parcourir ligne1 et ligne2
    h1 = h2 = 0  # Hauteurs courantes des deux lignes
    
    # On parcourt les deux lignes simultanément
    while i < len(ligne1) or j < len(ligne2):
        
        # on détermine le prochain x à traiter
        # min des prochains x dispo
        if i >= len(ligne1):
            # Plus de points dans ligne1, on prend ligne2
            x = ligne2[j][0]
        elif j >= len(ligne2):
            # Plus de points dans ligne2, on prend ligne1
            x = ligne1[i][0]
        else:
            # On prend le plus petit x
            x = min(ligne1[i][0], ligne2[j][0])
        
        # Mettre à jour les hauteurs courantes si on atteint un point de changement
        if i < len(ligne1) and ligne1[i][0] == x:
            h1 = ligne1[i][1]  # Nouvelle hauteur pour ligne1
            i += 1
        if j < len(ligne2) and ligne2[j][0] == x:
            h2 = ligne2[j][1]  # Nouvelle hauteur pour ligne2
            j += 1
        
        # La nouvelle hauteur est le maximum des deux hauteurs courantes
        nouvelle_hauteur = max(h1, h2)
        
        # On ajoute le point seulement si la hauteur change
        # (pour éviter les points redondants sur une ligne horizontale)
        if not resultat or resultat[-1][1] != nouvelle_hauteur:
            resultat.append((x, nouvelle_hauteur))
    
    return resultat


def ligne_toits_diviser_regner(immeubles):
    """
    Q5: Algorithme principal diviser-pour-régner en O(n log n)
    
    Args:
        immeubles: Liste de tuples (g, h, d) représentant les immeubles
                  où g=gauche, h=hauteur, d=droite
    
    Returns:
        Liste de tuples (x, y) représentant la ligne de toits complète
    
    Principe: 
    1. Cas de base: 0 ou 1 immeuble
    2. Diviser: couper la liste en deux parties égales
    3. Régner: résoudre récursivement sur chaque moitié
    4. Combiner: fusionner les deux lignes obtenues
    """
    
    # Cas de base 1: aucun immeuble
    if not immeubles:
        return []
    
    # Cas de base 2: un seul immeuble
    if len(immeubles) == 1:
        g, h, d = immeubles[0]
        if h == 0:
            return []  # Immeuble de hauteur 0 = pas d'immeuble
        # Un immeuble crée 4 points: (g,0)->(g,h)->(d,h)->(d,0)
        # En représentation compacte: (g,h) et (d,0)
        return [(g, h), (d, 0)]
    
    # Étape 1: Diviser
    # On coupe la liste d'immeubles en deux parties de taille égale (à 1 près)
    milieu = len(immeubles) // 2
    immeubles_gauche = immeubles[:milieu]
    immeubles_droite = immeubles[milieu:]
    
    # Étape 2: Régner
    # Résoudre récursivement sur chaque moitié
    ligne_gauche = ligne_toits_diviser_regner(immeubles_gauche)
    ligne_droite = ligne_toits_diviser_regner(immeubles_droite)
    
    # Étape 3: Combiner
    # Fusionner les deux lignes de toits obtenues
    return fusion_lignes_toits(ligne_gauche, ligne_droite)


def ligne_vers_svg(ligne_toits, filename="ligne_toits.svg", scale=10):
    """
    Utilitaire pour générer le fichier SVG (version corrigée)
    
    Args:
        ligne_toits: Liste de tuples (x, y) en représentation compacte
        filename: Nom du fichier SVG à créer
        scale: Facteur d'échelle pour l'affichage
    """
    if not ligne_toits:
        return
    
    # Convertir en représentation complète pour SVG
    points_complets = []
    
    for i in range(len(ligne_toits)):
        x, y = ligne_toits[i]
        
        if i == 0:
            # Premier point: on part de (x, 0) puis on monte à (x, y)
            points_complets.extend([(x, 0), (x, y)])
        else:
            # Points intermédiaires: ligne horizontale puis verticale
            x_prev, y_prev = ligne_toits[i-1]
            points_complets.extend([(x, y_prev), (x, y)])
    
    # Dernier point: retour au sol
    if points_complets:
        dernier_x = points_complets[-1][0]
        points_complets.append((dernier_x, 0))
    
    # Trouver les dimensions réelles
    min_x = min(x for x, y in points_complets)
    max_x = max(x for x, y in points_complets)
    max_y = max(y for x, y in points_complets)
    
    # Calculer les dimensions du SVG avec une marge
    marge = 2
    largeur_reelle = max_x - min_x + 2 * marge
    hauteur_reelle = max_y + 2 * marge
    
    # Taille finale du SVG
    svg_width = largeur_reelle * scale
    svg_height = hauteur_reelle * scale
    
    # Générer les coordonnées pour SVG
    points_str = " ".join([f"{x},{y}" for x, y in points_complets])
    
    # Créer le fichier SVG avec des dimensions raisonnables
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" 
         width="{svg_width}" height="{svg_height}" 
         viewBox="{min_x - marge} -{max_y + marge} {largeur_reelle} {hauteur_reelle}">
    <polyline points="{points_str}" 
              stroke="red" stroke-width="0.2" fill="none" 
              transform="scale(1,-1)"/>
</svg>'''
    
    with open(filename, 'w') as f:
        f.write(svg_content)
    print(f"Fichier SVG créé: {filename} ({svg_width}x{svg_height} pixels)")


# Exemple d'utilisation et test
if __name__ == "__main__":
    # Test avec l'exemple du TP
    immeubles = [(3,13,9), (1,11,5), (19,18,22), (3,6,7), (16,3,25), (12,7,16)]
    
    print("Immeubles:", immeubles)
    
    # Calcul de la ligne de toits
    ligne = ligne_toits_diviser_regner(immeubles)
    print("Ligne de toits (compacte):", ligne)
    
    # Test de la fusion avec l'exemple de la Q4
    print("\n--- Test fusion Q4 ---")
    ligne1 = [(1,10), (5,6), (8,0), (10,8), (12,0)]
    ligne2 = [(2,12), (7,0), (9,4), (11,2), (14,0)]
    fusion = fusion_lignes_toits(ligne1, ligne2)
    print("Ligne 1:", ligne1)
    print("Ligne 2:", ligne2)
    print("Fusion:", fusion)
    print("Attendu: [(1,10), (2,12), (7,6), (8,0), (9,4), (10,8), (12,2), (14,0)]")
    
    # Génération du fichier SVG
    ligne_vers_svg(ligne)