#!/usr/bin/env python3
"""Extrait l'icone adaptative (fond + premier plan) d'un APK livre par AppForge et
l'ecrit en SVG, telle qu'un lanceur Android l'affiche (zone centrale 72/108, coins arrondis).

Usage : python3 make_app_icons.py <nom> <chemin.apk> [<nom> <chemin.apk> ...]
Sortie : assets/exemples/icones/<nom>.svg  (rendu PNG par render_gallery.js)
Depend d'androguard (pip install androguard).
"""
import os
import re
import sys
from xml.etree import ElementTree as ET

from androguard.core.apk import APK
from androguard.core.axml import AXMLPrinter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "exemples", "icones")
NS = "{http://schemas.android.com/apk/res/android}"


def argb_to_svg(value):
    """'#AARRGGBB' ou '#RRGGBB' -> (couleur, opacite)."""
    v = value.strip()
    if len(v) == 9:
        return "#" + v[3:], int(v[1:3], 16) / 255.0
    return v, 1.0


class Icon:
    def __init__(self, apk_path):
        self.apk = APK(apk_path)
        self.arsc = self.apk.get_android_resources()
        self.defs = []

    def gradient_def(self, path):
        """Un <gradient> aapt (degrade inline d'un fillColor) -> definition SVG, rend son id."""
        node = self.xml(path)
        a = node.attrib
        gid = f"g{len(self.defs)}"
        stops = []
        for item in node:
            c, o = argb_to_svg(item.attrib.get(NS + "color", "#FF000000"))
            stops.append(f'<stop offset="{float(item.attrib.get(NS + "offset", 0)):.3f}" stop-color="{c}" stop-opacity="{o:.3f}"/>')
        if not stops:
            for key, off in (("startColor", 0), ("centerColor", 0.5), ("endColor", 1)):
                if NS + key in a:
                    c, o = argb_to_svg(a[NS + key])
                    stops.append(f'<stop offset="{off}" stop-color="{c}" stop-opacity="{o:.3f}"/>')
        gtype = a.get(NS + "type", "0")
        if gtype == "1":
            self.defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{a.get(NS + "centerX", 54)}" '
                             f'cy="{a.get(NS + "centerY", 54)}" r="{a.get(NS + "gradientRadius", 54)}">{"".join(stops)}</radialGradient>')
        else:
            self.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{a.get(NS + "startX", 0)}" '
                             f'y1="{a.get(NS + "startY", 0)}" x2="{a.get(NS + "endX", 0)}" y2="{a.get(NS + "endY", 108)}">{"".join(stops)}</linearGradient>')
        return gid

    def resolve(self, ref):
        rid = int(ref[1:], 16)
        vals = self.arsc.get_resolved_res_configs(rid)
        return str(vals[0][1]) if vals else None

    def xml(self, path):
        text = AXMLPrinter(self.apk.get_file(path)).get_xml().decode("utf-8", "replace")
        for ref in sorted(set(re.findall(r"@7F[0-9A-F]{6}", text))):
            val = self.resolve(ref)
            if val:
                text = text.replace(ref, val)
        return ET.fromstring(text)

    def vector_to_svg_group(self, node):
        parts = []
        for child in node:
            tag = child.tag.split("}")[-1]
            if tag == "group":
                a = child.attrib
                g = lambda k, d: float(a.get(NS + k, d))
                px, py = g("pivotX", 0), g("pivotY", 0)
                t = (f"translate({g('translateX', 0)} {g('translateY', 0)}) translate({px} {py}) "
                     f"rotate({g('rotation', 0)}) scale({g('scaleX', 1)} {g('scaleY', 1)}) translate({-px} {-py})")
                parts.append(f'<g transform="{t}">{self.vector_to_svg_group(child)}</g>')
            elif tag == "path":
                a = child.attrib
                attrs = [f'd="{a.get(NS + "pathData", "")}"']
                fill = a.get(NS + "fillColor")
                if fill and fill.endswith(".xml"):
                    attrs.append(f'fill="url(#{self.gradient_def(fill)})"')
                elif fill:
                    c, o = argb_to_svg(fill)
                    o *= float(a.get(NS + "fillAlpha", 1))
                    attrs.append(f'fill="{c}"')
                    if o < 1:
                        attrs.append(f'fill-opacity="{o:.3f}"')
                else:
                    attrs.append('fill="none"')
                stroke = a.get(NS + "strokeColor")
                if stroke:
                    c, o = argb_to_svg(stroke)
                    o *= float(a.get(NS + "strokeAlpha", 1))
                    attrs.append(f'stroke="{c}" stroke-width="{a.get(NS + "strokeWidth", 1)}"')
                    if o < 1:
                        attrs.append(f'stroke-opacity="{o:.3f}"')
                    cap = {"0": "butt", "1": "round", "2": "square"}.get(a.get(NS + "strokeLineCap", "0"), "butt")
                    join = {"0": "miter", "1": "round", "2": "bevel"}.get(a.get(NS + "strokeLineJoin", "0"), "miter")
                    attrs.append(f'stroke-linecap="{cap}" stroke-linejoin="{join}"')
                parts.append(f"<path {' '.join(attrs)}/>")
        return "".join(parts)

    def layer_svg(self, value):
        """Un calque d'icone adaptative : couleur unie ou drawable vectoriel."""
        if value.startswith("#"):
            c, o = argb_to_svg(value)
            return f'<rect x="0" y="0" width="108" height="108" fill="{c}" fill-opacity="{o:.3f}"/>'
        if value.endswith(".xml"):
            node = self.xml(value)
            vw = float(node.attrib.get(NS + "viewportWidth", 108))
            vh = float(node.attrib.get(NS + "viewportHeight", 108))
            return f'<g transform="scale({108 / vw} {108 / vh})">{self.vector_to_svg_group(node)}</g>'
        raise ValueError(f"calque non gere : {value}")

    def svg(self):
        icon_path = self.apk.get_app_icon()
        if not icon_path or not icon_path.endswith(".xml"):
            raise ValueError(f"icone non vectorielle : {icon_path}")
        node = self.xml(icon_path)
        layers = {c.tag.split("}")[-1]: c.attrib.get(NS + "drawable") for c in node}
        bg = self.layer_svg(layers["background"])
        fg = self.layer_svg(layers["foreground"])
        # Zone visible d'un lanceur : 72x72 au centre, coins arrondis (~24 %).
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="18 18 72 72">'
            f'<defs><clipPath id="m"><rect x="18" y="18" width="72" height="72" rx="17" ry="17"/></clipPath>{"".join(self.defs)}</defs>'
            f'<g clip-path="url(#m)">{bg}{fg}</g></svg>'
        )


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    pairs = list(zip(argv[::2], argv[1::2]))
    for name, apk_path in pairs:
        icon = Icon(apk_path)
        out = os.path.join(OUT, f"{name}.svg")
        with open(out, "w", encoding="utf-8") as f:
            f.write(icon.svg())
        print("ok", os.path.relpath(out, ROOT), "|", icon.apk.get_app_name(), "|", icon.apk.get_package())


if __name__ == "__main__":
    main(sys.argv[1:])
