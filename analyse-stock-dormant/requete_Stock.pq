// Requête « Stock » : export Sage X3 article-site (ITMFCY) préparé pour l'analyse du stock dormant.
// Remplace le code de ta requête F1791382381807_ITMFCY (Accueil > Transformer les données > Éditeur avancé),
// puis renomme la requête en « Stock ».
// Si tu n'utilises pas le paramètre « Chemin fichier CSV », remplace #"Chemin fichier CSV" par le chemin entre guillemets :
// "C:\Users\zied.triki\Desktop\F1791382381807_ITMFCY.csv"
let
    Source = Csv.Document(File.Contents(#"Chemin fichier CSV"), [Delimiter = ";", Columns = 47, Encoding = 65001, QuoteStyle = QuoteStyle.None]),
    #"En-têtes promus" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    // La 47e colonne de l'export est vide (point-virgule final) : on la supprime.
    #"Colonne vide supprimée" = Table.RemoveColumns(#"En-têtes promus", {""}, MissingField.Ignore),
    // Dans X3, une date vide est exportée « / / » : on la transforme en valeur nulle au lieu d'une erreur.
    ConvertirDate = (valeur) => try Date.FromText(Text.Trim(valeur), "fr-FR") otherwise null,
    #"Dates converties" = Table.TransformColumns(
        #"Colonne vide supprimée",
        {
            {"Date dernier achat", ConvertirDate, type date},
            {"Date dernière entrée", ConvertirDate, type date},
            {"Date dernière sortie", ConvertirDate, type date}
        }
    ),
    // Les quantités et prix passent en nombre décimal (avant : entier, ce qui arrondissait les KG, M, L...).
    #"Type modifié" = Table.TransformColumnTypes(
        #"Dates converties",
        {
            {"Production", type text}, {"Site stockage", type text}, {"Article", type text}, {"Unité stock", type text},
            {"Poids de l'US", type number}, {"Unité poids", type text}, {"Unité achat", type text},
            {"Type emplact/défaut", type text}, {"Type suggestion", type text}, {"Type coût comptable", type text},
            {"Màj coût standard", type text}, {"Mise à jour coût std actualisé", type text},
            {"Mise à jour coût std. budgété", type text}, {"Màj coût simulation", type text},
            {"Alternative", Int64.Type}, {"Coût", type text}, {"Méthode valorisation", type text},
            {"Date création ITF", type date}, {"Date heure ITF", type date}, {"Opérateur création ITF", type text},
            {"Code comptable", type text}, {"Section analytique", type text}, {"Catégorie", type text},
            {"Statut article", type text}, {"Code plus bas niveau", Int64.Type},
            {"Date création ITM", type date}, {"Date heure ITM", type date}, {"Opérateur création ITM", type text},
            {"Prix moyen pondéré", type number}, {"Dernier prix d'achat", type number},
            {"Prix dernière entrée", type number}, {"Base montant PMP", type number},
            {"Stock interne 'A'", type number}, {"Stock interne 'Q'", type number}, {"Stock interne 'R'", type number},
            {"Stock sous-trait 'A'", type number}, {"Stock sous-trait 'Q'", type number}, {"Stock sous-trait 'R'", type number},
            {"Stock prêté 'A'", type number}, {"Stock prêté 'Q'", type number}, {"Stock prêté 'R'", type number},
            {"STOCK TOTAL", type number}, {"Montant", type number}
        }
    ),
    // Date à laquelle on mesure l'ancienneté : le jour de l'actualisation.
    DateAnalyse = Date.From(DateTime.LocalNow()),
    // Magasin = type d'emplacement par défaut sans l'étoile (CO* -> CO, SF* -> SF, SAV et SAV* -> SAV...).
    #"Magasin ajouté" = Table.AddColumn(
        #"Type modifié",
        "Magasin",
        each
            let
                code = if [#"Type emplact/défaut"] = null then "" else Text.Upper(Text.Trim(Text.Remove([#"Type emplact/défaut"], {"*"})))
            in
                if code = "" then "(non renseigné)" else code,
        type text
    ),
    // Dernier mouvement = la plus récente des dates de dernière entrée et de dernière sortie.
    // Sans aucun mouvement connu, on prend la date de création de l'article-site.
    #"Dernier mouvement ajouté" = Table.AddColumn(
        #"Magasin ajouté",
        "Date dernier mouvement",
        each
            let
                dernier = List.Max(List.RemoveNulls({[Date dernière entrée], [Date dernière sortie]}))
            in
                if dernier = null then [Date création ITF] else dernier,
        type date
    ),
    #"Jours sans mouvement ajoutés" = Table.AddColumn(
        #"Dernier mouvement ajouté",
        "Jours sans mouvement",
        each if [Date dernier mouvement] = null then null else Duration.Days(DateAnalyse - [Date dernier mouvement]),
        Int64.Type
    ),
    // Pour information : ancienneté de la dernière sortie (consommation, vente...).
    #"Jours sans sortie ajoutés" = Table.AddColumn(
        #"Jours sans mouvement ajoutés",
        "Jours sans sortie",
        each
            let
                reference = if [Date dernière sortie] = null then [Date création ITF] else [Date dernière sortie]
            in
                if reference = null then null else Duration.Days(DateAnalyse - reference),
        Int64.Type
    ),
    #"Date analyse ajoutée" = Table.AddColumn(#"Jours sans sortie ajoutés", "Date analyse", each DateAnalyse, type date)
in
    #"Date analyse ajoutée"
