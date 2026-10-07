# Analyse du stock dormant (Power BI)

**Question :** dans un magasin donné, quels articles en stock n'ont eu **aucun mouvement** (ni entrée ni sortie) depuis au moins **X jours** ? X se règle avec un curseur.

## Option 1 : ouvrir le modèle prêt à l'emploi (`Stock_dormant.pbit`)

1. Double-clique sur `Stock_dormant.pbit`.
2. Power BI demande **Chemin fichier CSV** : laisse `C:\Users\zied.triki\Desktop\F1791382381807_ITMFCY.csv` ou indique ton nouvel export X3, puis clique **Charger**.
3. La page **Stock dormant** s'affiche :
   - le curseur **Seuil jours** règle X (180 par défaut ; tu peux aussi taper une valeur) ;
   - la liste **Magasin** filtre un ou plusieurs magasins (SF, PF, CO…) ;
   - les cartes donnent le seuil appliqué, le nombre d'articles dormants, leur valeur, la part de la valeur du stock et la date d'analyse ;
   - le graphique montre la valeur dormante par magasin, et le tableau liste les articles dormants du plus coûteux au moins coûteux.
4. Enregistre le résultat en `.pbix`. À chaque nouvel export X3, il suffit de cliquer sur **Actualiser**.

Pour changer le chemin du fichier plus tard : **Transformer les données > Modifier les paramètres**.

## Option 2 : ajouter l'analyse dans ton fichier `analyse.pbix`

Utile si le modèle `.pbit` ne s'ouvre pas, ou si tu préfères tout construire toi-même.

1. **Accueil > Transformer les données**, sélectionne la requête `F1791382381807_ITMFCY`, puis **Accueil > Éditeur avancé**.
2. Colle le contenu de `requete_Stock.pq`. Dans la ligne `Source`, remplace `#"Chemin fichier CSV"` par `"C:\Users\zied.triki\Desktop\F1791382381807_ITMFCY.csv"` (avec les guillemets).
3. Renomme la requête en **Stock**, puis **Fermer et appliquer**.
4. **Modélisation > Nouveau paramètre > Plage numérique** : nom `Seuil jours`, nombre entier, minimum 0, maximum 1095, incrément 1, par défaut 180, et coche « Ajouter un segment à cette page ». Power BI crée une table `Seuil jours` avec une mesure (du type `Valeur Seuil jours`) : renomme cette mesure en `Seuil appliqué (jours)`.
5. Dans la table **Stock**, crée les mesures de `mesures.dax` une par une, à partir de `Articles en stock` (**Accueil > Nouvelle mesure**, puis colle le texte « Nom = formule »).
   - Si Power BI signale une erreur de syntaxe, c'est probablement qu'il attend des `;` au lieu des `,` (séparateurs régionaux) : remplace-les.
6. Construis les visuels :
   - segment `Stock[Magasin]` ;
   - cartes `Articles dormants`, `Valeur dormante`, `% valeur dormante` ;
   - graphique à barres : axe `Magasin`, valeur `Valeur dormante` ;
   - tableau : `Article`, `Magasin`, `Date dernière entrée`, `Date dernière sortie`, `Jours dormant`, `Quantité dormante`, `Valeur dormante`.

   Le tableau n'affiche que les articles dormants, car les mesures sont vides pour les autres.

## Règles de calcul

| Élément | Règle |
|---|---|
| Article dormant | `STOCK TOTAL > 0` **et** `Jours sans mouvement ≥ X` |
| Jours sans mouvement | Date d'actualisation − la plus récente des dates *dernière entrée* et *dernière sortie*. Sans aucun mouvement connu, c'est la *date de création* de l'article-site qui sert de référence. |
| Magasin | `Type emplact/défaut` sans l'étoile (`CO*` → `CO`, `SAV` et `SAV*` → `SAV`). Vide → `(non renseigné)` |
| Valeur | Colonne `Montant` de l'export (stock × PMP) |

Tu peux aussi utiliser la colonne `Jours sans sortie` : dans les mesures, remplace `'Stock'[Jours sans mouvement]` par `'Stock'[Jours sans sortie]` pour ne compter que les sorties (un article réapprovisionné mais jamais consommé sera alors considéré comme dormant).

## Limites de l'export actuel

- L'export `ITMFCY` donne **un seul stock par article pour tout le site SO1**. Le « magasin » est donc le **type d'emplacement par défaut** de l'article, pas l'endroit où le stock se trouve réellement. Pour un vrai découpage par magasin ou par emplacement, il faudrait un export du **stock par emplacement** de X3 (table `STOCK`), qui contient aussi les dates de dernière entrée et de dernière sortie par ligne de stock.
- Dans ton fichier d'origine, les stocks et le dernier prix d'achat étaient typés en **nombre entier**, ce qui arrondissait les KG, M et L. La requête fournie les passe en **nombre décimal**.
- Les dates vides de X3 (`  /  /`) sont converties en valeurs vides, alors qu'elles restaient du texte dans le fichier d'origine.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `Stock_dormant.pbit` | Modèle Power BI complet : requête, paramètre, mesures et page de rapport |
| `requete_Stock.pq` | Code Power Query de la table **Stock** |
| `mesures.dax` | Paramètre X et mesures DAX |
| `outils/generer_pbit.py` | Script qui régénère le `.pbit` |
