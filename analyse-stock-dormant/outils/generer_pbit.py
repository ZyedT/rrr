"""Génère le modèle Power BI « Stock_dormant.pbit » (modèle de données + page de rapport).

Usage : python generer_pbit.py <dossier .pbix décompressé> <requete_Stock.pq> <mesures.dax> <sortie.pbit>

Le dossier .pbix décompressé fournit les parties reprises telles quelles (Version, Settings,
Metadata, thème du rapport) pour rester compatible avec la version de Power BI Desktop qui l'a créé.
"""
import json
import re
import secrets
import sys
import uuid
import zipfile
from pathlib import Path

SOURCE_DIR, PQ_FILE, DAX_FILE, OUTPUT = (Path(a) for a in sys.argv[1:5])

TABLE = "Stock"
PARAM_TABLE = "Seuil jours"
CSV_PARAMETER = "Chemin fichier CSV"
CSV_DEFAULT_PATH = r"C:\Users\zied.triki\Desktop\F1791382381807_ITMFCY.csv"
DEFAULT_THRESHOLD = 180


def guid():
    return str(uuid.uuid4())


def utf16(text):
    return text.encode("utf-16-le")


# ---------------------------------------------------------------- modèle de données

TEXT, DOUBLE, INT, DATE = "string", "double", "int64", "dateTime"
COLUMNS = [
    ("Production", TEXT), ("Site stockage", TEXT), ("Article", TEXT), ("Unité stock", TEXT),
    ("Poids de l'US", DOUBLE), ("Unité poids", TEXT), ("Unité achat", TEXT), ("Type emplact/défaut", TEXT),
    ("Type suggestion", TEXT), ("Type coût comptable", TEXT), ("Màj coût standard", TEXT),
    ("Mise à jour coût std actualisé", TEXT), ("Mise à jour coût std. budgété", TEXT),
    ("Màj coût simulation", TEXT), ("Alternative", INT), ("Coût", TEXT), ("Méthode valorisation", TEXT),
    ("Date création ITF", DATE), ("Date heure ITF", DATE), ("Opérateur création ITF", TEXT),
    ("Code comptable", TEXT), ("Section analytique", TEXT), ("Catégorie", TEXT), ("Statut article", TEXT),
    ("Code plus bas niveau", INT), ("Date création ITM", DATE), ("Date heure ITM", DATE),
    ("Opérateur création ITM", TEXT), ("Prix moyen pondéré", DOUBLE), ("Dernier prix d'achat", DOUBLE),
    ("Date dernier achat", DATE), ("Prix dernière entrée", DOUBLE), ("Date dernière entrée", DATE),
    ("Base montant PMP", DOUBLE), ("Date dernière sortie", DATE),
    ("Stock interne 'A'", DOUBLE), ("Stock interne 'Q'", DOUBLE), ("Stock interne 'R'", DOUBLE),
    ("Stock sous-trait 'A'", DOUBLE), ("Stock sous-trait 'Q'", DOUBLE), ("Stock sous-trait 'R'", DOUBLE),
    ("Stock prêté 'A'", DOUBLE), ("Stock prêté 'Q'", DOUBLE), ("Stock prêté 'R'", DOUBLE),
    ("STOCK TOTAL", DOUBLE), ("Montant", DOUBLE),
    ("Magasin", TEXT), ("Date dernier mouvement", DATE), ("Jours sans mouvement", INT),
    ("Jours sans sortie", INT), ("Date analyse", DATE),
]
NOT_SUMMED = {"Alternative", "Code plus bas niveau", "Jours sans mouvement", "Jours sans sortie"}


def column(name, data_type):
    col = {
        "name": name,
        "dataType": data_type,
        "sourceColumn": name,
        "lineageTag": guid(),
        "summarizeBy": "sum" if data_type in (DOUBLE, INT) and name not in NOT_SUMMED else "none",
        "annotations": [{"name": "SummarizationSetBy", "value": "Automatic"}],
    }
    if data_type == DATE:
        col["formatString"] = "dd/mm/yyyy"
        col["annotations"].append({"name": "UnderlyingDateTimeDataType", "value": "Date"})
    elif data_type == INT:
        col["formatString"] = "0"
    elif data_type == DOUBLE:
        col["annotations"].append({"name": "PBI_FormatHint", "value": "{\"isGeneralNumber\":true}"})
    return col


def read_m_query():
    """Code M de la requête, sans l'en-tête de commentaires destiné à la copie manuelle."""
    lines = PQ_FILE.read_text(encoding="utf-8").splitlines()
    return lines[next(i for i, l in enumerate(lines) if l.strip() == "let"):]


def read_measures():
    """Lit mesures.dax : chaque bloc « Nom = expression » séparé par une ligne vide.
    Les lignes de commentaire // et la table calculée du paramètre sont ignorées ici."""
    text = DAX_FILE.read_text(encoding="utf-8")
    blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
    measures = {}
    for block in blocks:
        lines = [l for l in block.splitlines() if not l.lstrip().startswith("//")]
        if not lines:
            continue
        name, first = lines[0].split(" = ", 1) if " = " in lines[0] else (lines[0].rstrip(" ="), "")
        body = ([first.strip()] if first.strip() else []) + lines[1:]
        measures[name.strip()] = "\n".join(body).strip()
    return measures


MEASURES = read_measures()
FORMATS = {
    "Seuil appliqué (jours)": "0",
    "Articles en stock": "#,0",
    "Valeur du stock": "#,0",
    "Articles dormants": "#,0",
    "Valeur dormante": "#,0",
    "% valeur dormante": "0.0 %;-0.0 %;0.0 %",
    "% articles dormants": "0.0 %;-0.0 %;0.0 %",
    "Jours dormant": "0",
    "Analyse au": "dd/mm/yyyy",
}


def measure(name):
    m = {"name": name, "expression": MEASURES[name].splitlines(), "lineageTag": guid()}
    if name in FORMATS:
        m["formatString"] = FORMATS[name]
    return m


stock_measures = [n for n in MEASURES if n not in ("Seuil jours", "Seuil appliqué (jours)")]
param_series = MEASURES["Seuil jours"]

model = {
    "name": guid(),
    "compatibilityLevel": 1550,
    "model": {
        "culture": "fr-FR",
        "dataAccessOptions": {"legacyRedirects": True, "returnErrorValuesAsNull": True},
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "fr-FR",
        "tables": [
            {
                "name": TABLE,
                "lineageTag": guid(),
                "columns": [column(n, t) for n, t in COLUMNS],
                "partitions": [
                    {
                        "name": f"{TABLE}-{guid()}",
                        "mode": "import",
                        "source": {"type": "m", "expression": read_m_query()},
                    }
                ],
                "measures": [measure(n) for n in stock_measures],
                "annotations": [{"name": "PBI_ResultType", "value": "Table"}],
            },
            {
                "name": PARAM_TABLE,
                "lineageTag": guid(),
                "columns": [
                    {
                        "type": "calculatedTableColumn",
                        "name": PARAM_TABLE,
                        "dataType": "int64",
                        "isDataTypeInferred": True,
                        "sourceColumn": "[Value]",
                        "formatString": "0",
                        "lineageTag": guid(),
                        "summarizeBy": "none",
                        "extendedProperties": [
                            {"type": "json", "name": "ParameterMetadata", "value": {"version": 0}}
                        ],
                        "annotations": [{"name": "SummarizationSetBy", "value": "User"}],
                    }
                ],
                "partitions": [
                    {
                        "name": f"{PARAM_TABLE}-{guid()}",
                        "mode": "import",
                        "source": {"type": "calculated", "expression": param_series},
                    }
                ],
                "measures": [measure("Seuil appliqué (jours)")],
            },
        ],
        "expressions": [
            {
                "name": CSV_PARAMETER,
                "kind": "m",
                "expression": f'"{CSV_DEFAULT_PATH}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]',
                "lineageTag": guid(),
                "annotations": [{"name": "PBI_ResultType", "value": "Text"}],
            }
        ],
        "annotations": [
            {"name": "PBI_QueryOrder", "value": json.dumps([CSV_PARAMETER, TABLE], ensure_ascii=False)},
            {"name": "__PBI_TimeIntelligenceEnabled", "value": "0"},
            {"name": "PBIDesktopVersion", "value": "2.110.805.0 (22.10)"},
        ],
    },
}

# ---------------------------------------------------------------- rapport

z_counter = iter(range(0, 100000, 1000))


def lit(value):
    """Littéral du langage de requête des visuels : texte entre apostrophes, nombre suffixé, booléen."""
    if isinstance(value, bool):
        return {"expr": {"Literal": {"Value": "true" if value else "false"}}}
    if isinstance(value, int):
        return {"expr": {"Literal": {"Value": f"{value}L"}}}
    if isinstance(value, float):
        return {"expr": {"Literal": {"Value": f"{value}D"}}}
    return {"expr": {"Literal": {"Value": "'" + value.replace("'", "''") + "'"}}}


def alias(entity):
    return "s" if entity == TABLE else "p"


def col_ref(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Source": alias(entity)}}, "Property": prop}}


def measure_ref(entity, prop):
    return {"Measure": {"Expression": {"SourceRef": {"Source": alias(entity)}}, "Property": prop}}


def field(kind, entity, prop):
    ref = col_ref(entity, prop) if kind == "col" else measure_ref(entity, prop)
    return {**ref, "Name": f"{entity}.{prop}"}


def query(fields, order_by=None):
    entities = []
    for _, entity, _ in fields:
        if entity not in entities:
            entities.append(entity)
    q = {
        "Version": 2,
        "From": [{"Name": alias(e), "Entity": e, "Type": 0} for e in entities],
        "Select": [field(*f) for f in fields],
    }
    if order_by:
        kind, entity, prop, direction = order_by
        ref = col_ref(entity, prop) if kind == "col" else measure_ref(entity, prop)
        q["OrderBy"] = [{"Direction": direction, "Expression": ref}]
    return q


def title(text):
    return {"title": [{"properties": {"show": lit(True), "text": lit(text)}}]}


def container(x, y, w, h, single_visual):
    z = next(z_counter)
    config = {
        "name": secrets.token_hex(10),
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h}}],
        "singleVisual": single_visual,
    }
    return {
        "x": x, "y": y, "z": z, "width": w, "height": h,
        "config": json.dumps(config, ensure_ascii=False, separators=(",", ":")),
        "filters": "[]",
    }


def textbox(x, y, w, h, text, note):
    return container(x, y, w, h, {
        "visualType": "textbox",
        "drillFilterOtherVisuals": True,
        "objects": {"general": [{"properties": {"paragraphs": [
            {"textRuns": [{"value": text, "textStyle": {"fontWeight": "bold", "fontSize": "16pt"}}]},
            {"textRuns": [{"value": note, "textStyle": {"fontSize": "9pt"}}]},
        ]}}]},
    })


def card(x, y, w, h, entity, measure_name):
    f = ("measure", entity, measure_name)
    return container(x, y, w, h, {
        "visualType": "card",
        "projections": {"Values": [{"queryRef": f"{entity}.{measure_name}"}]},
        "prototypeQuery": query([f]),
        "drillFilterOtherVisuals": True,
    })


def slicer_list(x, y, w, h, entity, column_name):
    f = ("col", entity, column_name)
    return container(x, y, w, h, {
        "visualType": "slicer",
        "projections": {"Values": [{"queryRef": f"{entity}.{column_name}", "active": True}]},
        "prototypeQuery": query([f], order_by=("col", entity, column_name, 1)),
        "drillFilterOtherVisuals": True,
        "objects": {
            "data": [{"properties": {"mode": lit("Basic")}}],
            "selection": [{"properties": {"selectAllCheckboxEnabled": lit(True)}}],
        },
    })


def slicer_single_value(x, y, w, h, entity, column_name, default):
    f = ("col", entity, column_name)
    selected = {
        "Version": 2,
        "From": [{"Name": alias(entity), "Entity": entity, "Type": 0}],
        "Where": [{"Condition": {"Comparison": {
            "ComparisonKind": 0,
            "Left": col_ref(entity, column_name),
            "Right": {"Literal": {"Value": f"{default}L"}},
        }}}],
    }
    return container(x, y, w, h, {
        "visualType": "slicer",
        "projections": {"Values": [{"queryRef": f"{entity}.{column_name}"}]},
        "prototypeQuery": query([f]),
        "drillFilterOtherVisuals": True,
        "objects": {
            "data": [{"properties": {"mode": lit("Single")}}],
            "general": [{"properties": {"filter": {"filter": selected}}}],
        },
    })


def bar_chart(x, y, w, h):
    category = ("col", TABLE, "Magasin")
    value = ("measure", TABLE, "Valeur dormante")
    tooltip = ("measure", TABLE, "Articles dormants")
    return container(x, y, w, h, {
        "visualType": "clusteredBarChart",
        "projections": {
            "Category": [{"queryRef": f"{TABLE}.Magasin", "active": True}],
            "Y": [{"queryRef": f"{TABLE}.Valeur dormante"}],
            "Tooltips": [{"queryRef": f"{TABLE}.Articles dormants"}],
        },
        "prototypeQuery": query([category, value, tooltip], order_by=("measure", TABLE, "Valeur dormante", 2)),
        "drillFilterOtherVisuals": True,
        "hasDefaultSort": True,
        "objects": {"labels": [{"properties": {"show": lit(True)}}]},
        "vcObjects": title("Valeur dormante par magasin"),
    })


def detail_table(x, y, w, h):
    fields = [
        ("col", TABLE, "Article"),
        ("col", TABLE, "Magasin"),
        ("col", TABLE, "Statut article"),
        ("col", TABLE, "Unité stock"),
        ("col", TABLE, "Date dernière entrée"),
        ("col", TABLE, "Date dernière sortie"),
        ("measure", TABLE, "Jours dormant"),
        ("measure", TABLE, "Quantité dormante"),
        ("measure", TABLE, "Valeur dormante"),
    ]
    return container(x, y, w, h, {
        "visualType": "tableEx",
        "projections": {"Values": [{"queryRef": f"{e}.{p}"} for _, e, p in fields]},
        "prototypeQuery": query(fields, order_by=("measure", TABLE, "Valeur dormante", 2)),
        "columnProperties": {
            f"{TABLE}.Jours dormant": {"displayName": "Jours sans mouvement"},
            f"{TABLE}.Quantité dormante": {"displayName": "Stock"},
            f"{TABLE}.Valeur dormante": {"displayName": "Valeur"},
        },
        "drillFilterOtherVisuals": True,
        "vcObjects": title("Articles dormants (du plus coûteux au moins coûteux)"),
    })


original_layout = json.loads((SOURCE_DIR / "Report" / "Layout").read_bytes().decode("utf-16-le"))

cards = ["Seuil appliqué (jours)", "Articles dormants", "Valeur dormante", "% valeur dormante", "Analyse au"]
visuals = [
    textbox(
        20, 5, 1240, 60,
        "Stock dormant : articles en stock sans mouvement depuis au moins X jours",
        "Dormant = STOCK TOTAL > 0 et aucune entrée ni sortie depuis X jours (comptés jusqu'à la date "
        "d'actualisation). Magasin = type d'emplacement par défaut de l'article-site, sans l'étoile.",
    ),
    slicer_single_value(20, 70, 240, 110, PARAM_TABLE, PARAM_TABLE, DEFAULT_THRESHOLD),
    slicer_list(20, 190, 240, 520, TABLE, "Magasin"),
]
for i, name in enumerate(cards):
    entity = PARAM_TABLE if name == "Seuil appliqué (jours)" else TABLE
    visuals.append(card(280 + i * 198, 70, 188, 100, entity, name))
visuals += [bar_chart(280, 180, 330, 530), detail_table(620, 180, 640, 530)]

layout = {
    "id": 0,
    "resourcePackages": original_layout["resourcePackages"],
    "sections": [{
        "id": 0,
        "name": "ReportSection",
        "displayName": "Stock dormant",
        "filters": "[]",
        "ordinal": 0,
        "visualContainers": visuals,
        "config": "{}",
        "displayOption": 1,
        "width": 1280,
        "height": 720,
    }],
    "config": original_layout["config"],
    "layoutOptimization": 0,
}

diagram = {
    "version": "1.1.0",
    "diagrams": [{
        "ordinal": 0,
        "scrollPosition": {"x": 0, "y": 0},
        "nodes": [
            {"location": {"x": 0, "y": 0}, "nodeIndex": TABLE, "size": {"height": 300, "width": 234}, "zIndex": 0},
            {"location": {"x": 300, "y": 0}, "nodeIndex": PARAM_TABLE, "size": {"height": 104, "width": 234}, "zIndex": 1},
        ],
        "name": "Toutes les tables",
        "zoomValue": 100,
        "pinKeyFieldsToTop": False,
        "showExtraHeaderInfo": False,
        "hideKeyFieldsWhenCollapsed": False,
    }],
    "selectedDiagram": "Toutes les tables",
    "defaultDiagram": "Toutes les tables",
}

content_types = (
    '\ufeff<?xml version="1.0" encoding="utf-8"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="json" ContentType="" />'
    '<Override PartName="/Version" ContentType="" />'
    '<Override PartName="/DataModelSchema" ContentType="" />'
    '<Override PartName="/DiagramLayout" ContentType="" />'
    '<Override PartName="/Report/Layout" ContentType="" />'
    '<Override PartName="/Settings" ContentType="application/json" />'
    '<Override PartName="/Metadata" ContentType="application/json" />'
    '</Types>'
)

theme = "Report/StaticResources/SharedResources/BaseThemes/CY22SU09.json"
with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as pbit:
    pbit.writestr("Version", (SOURCE_DIR / "Version").read_bytes())
    pbit.writestr("[Content_Types].xml", content_types.encode("utf-8"))
    pbit.writestr("DataModelSchema", utf16(json.dumps(model, ensure_ascii=False, indent=2)))
    pbit.writestr("DiagramLayout", utf16(json.dumps(diagram, ensure_ascii=False, separators=(",", ":"))))
    pbit.writestr("Report/Layout", utf16(json.dumps(layout, ensure_ascii=False, separators=(",", ":"))))
    pbit.writestr("Settings", (SOURCE_DIR / "Settings").read_bytes())
    pbit.writestr("Metadata", (SOURCE_DIR / "Metadata").read_bytes())
    pbit.writestr(theme, (SOURCE_DIR / theme).read_bytes())

print(f"{OUTPUT} : {len(stock_measures) + 1} mesures, {len(visuals)} visuels")
