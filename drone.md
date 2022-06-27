# Drone

Pour determiner le chemin que va suivre le drone on detemine l'ensemble des sommets
qui permette d'avoir une vue sur chaque aretes de notre graphe (vertex cover problem)

## Conditions
- si deux noeud sont relies la route est droite

# Iterations:
1. on calcule tous les points d'interets qui nous premettraient d'avoir une
vision sur toute les aretes
2. le drone parcourt l'ensemble des noeuds trouve de proche en proche jusqu'a
avoir tout visite.
3. On colorie le graphe au fur et a mesure du parcours du drone.

# couverture par sommets

pour trouver l'ensemble des sommets interessants, on cherche le couplage maximal
de notre graphe, puis on insere chaque pair de sommets dans notre solution.

Pour trouver un couplage maximal, on cherche les plus courte chaine
ameliorante tant qu'il y en a en utilisant l'algo de ford-fulkerson ou celui
d'edmond.

## problemes
1. le parcours de ces points d'interet n'est peut etre pas le plus court en terme
de distance cumulee.
2. la solution pour trouver nos point d'interet est au pire deux fois plus grande
que la solution optimale.
3. on imagine que toutes les routes sont droite ou que la quantite de neige sur
la route est a peut pres homogene.

# resolution des problemes
1. (a venir soon)
2. on parcours tous les point d'interet on marque chaque arete adjacente avec le 
nb du sommet, puis on reparcours tout et on vire les sommets dont les aretes
possede un autre marquage que le sommet lui meme.
3. soit on rajoute des noeuds aux virages soit on considere que le drone peut
voir apres le virage

# Iterations 2:
1. on identifie les emplacement ou la route n'est pas droite et on rajoute un
sommet pour avoir deux routes droite
2. on calcule tous les points d'interets qui nous premettraient d'avoir une
vision sur toute les aretes
3. le drone parcourt l'ensemble des noeuds trouve de proche en proche jusqu'a
avoir tout visite.
4. On colorie le graphe au fur et a mesure du parcours du drone.


