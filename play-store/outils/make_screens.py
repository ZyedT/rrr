#!/usr/bin/env python3
"""Compose les nouvelles captures Play Store (1440x2560, ratio 9:16) a partir des
captures actuelles de la fiche (assets/sources/play-actuel-NN.png).

- Le fond est resynthetise a partir du degrade des captures actuelles (meme indigo).
- Le telephone (cadre S26 Ultra) est decoupe dans les captures actuelles.
- Les legendes sont en Inter Display (proche du Segoe UI des captures d'origine).

Usage : python3 make_screens.py  (chemins relatifs au dossier play-store/)
"""
import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "sources")
OUT_FR = os.path.join(ROOT, "assets", "screenshots-fr")
OUT_EN = os.path.join(ROOT, "assets", "screenshots-en")
W, H = 1440, 2560
PHONE_BOX = (254, 527, 1186, 2509)  # cadre du telephone dans les captures actuelles
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
FONT_SEMI = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"


def background():
    """Degrade identique aux captures actuelles : interpolation lineaire entre les
    colonnes de gauche et de droite de la capture 00."""
    base = np.asarray(Image.open(os.path.join(SRC, "play-actuel-00.png")).convert("RGB")).astype(np.float32)
    left, right = base[:, 0, :], base[:, W - 1, :]
    t = np.linspace(0, 1, W)[None, :, None]
    bg = left[:, None, :] * (1 - t) + right[:, None, :] * t
    return Image.fromarray(bg.astype(np.uint8), "RGB")


def phone(name, radius=100):
    im = Image.open(os.path.join(SRC, f"play-actuel-{name}.png")).convert("RGBA").crop(PHONE_BOX)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius=radius, fill=255)
    im.putalpha(mask)
    return im


def paste_with_shadow(canvas, im, xy, blur=40, offset=(0, 30), alpha=120):
    x, y = xy
    shadow = Image.new("RGBA", (im.size[0] + blur * 4, im.size[1] + blur * 4), (0, 0, 0, 0))
    sm = Image.new("L", im.size, 0)
    sm.paste(im.split()[3], (0, 0))
    shadow_layer = Image.new("RGBA", im.size, (0, 0, 0, alpha))
    shadow_layer.putalpha(Image.eval(im.split()[3], lambda a: a * alpha // 255))
    shadow.paste(shadow_layer, (blur * 2, blur * 2), shadow_layer)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(shadow, (x - blur * 2 + offset[0], y - blur * 2 + offset[1]))
    canvas.alpha_composite(im, (x, y))


def caption(canvas, title, subtitle, y=160, title_size=78, sub_size=42, badge=None):
    d = ImageDraw.Draw(canvas)
    if badge:
        fb = ImageFont.truetype(FONT_SEMI, 34)
        tw = d.textlength(badge, font=fb)
        bx0, by0 = (W - tw) / 2 - 36, y - 10
        d.rounded_rectangle((bx0, by0, bx0 + tw + 72, by0 + 60), radius=30, fill=(255, 255, 255, 46))
        d.text((W / 2, by0 + 30), badge, font=fb, fill="white", anchor="mm")
        y += 86
    ft = ImageFont.truetype(FONT_BOLD, title_size)
    d.multiline_text((W / 2, y), title, font=ft, fill="white", anchor="ma", align="center", spacing=8)
    lines = title.count("\n") + 1
    y2 = y + lines * (title_size + 8) + 22
    fs = ImageFont.truetype(FONT_MED, sub_size)
    d.multiline_text((W / 2, y2), subtitle, font=fs, fill=(232, 229, 255), anchor="ma", align="center", spacing=8)


def hero(out, title, subtitle):
    canvas = background().convert("RGBA")
    caption(canvas, title, subtitle, y=150, title_size=74, sub_size=42)
    p_left = phone("00")
    p_right = phone("06")
    scale = 0.74
    size = (int(p_left.size[0] * scale), int(p_left.size[1] * scale))
    p_left = p_left.resize(size, Image.LANCZOS)
    p_right = p_right.resize(size, Image.LANCZOS)
    paste_with_shadow(canvas, p_left, (34, 560))
    paste_with_shadow(canvas, p_right, (W - 34 - size[0], 760))
    canvas.convert("RGB").save(out, optimize=True)


def single(out, source, title, subtitle, badge=None):
    canvas = background().convert("RGBA")
    caption(canvas, title, subtitle, y=150 if not badge else 110, title_size=78, sub_size=42, badge=badge)
    p = phone(source)
    paste_with_shadow(canvas, p, (PHONE_BOX[0], PHONE_BOX[1]), blur=30, offset=(0, 20), alpha=90)
    canvas.convert("RGB").save(out, optimize=True)


def main():
    for d in (OUT_FR, OUT_EN):
        os.makedirs(d, exist_ok=True)

    # --- Francais : 8 captures dans l'ordre final de la fiche ---
    hero(os.path.join(OUT_FR, "01-hero.png"),
         "Décrivez votre app.\nRecevez-la, prête à installer.",
         "Conçue, fabriquée et testée pour vous. Sans coder.")
    shutil.copy(os.path.join(SRC, "play-actuel-00.png"), os.path.join(OUT_FR, "02-decrivez-prix-fixe.png"))
    shutil.copy(os.path.join(SRC, "play-actuel-06.png"), os.path.join(OUT_FR, "03-recevez-installez.png"))
    single(os.path.join(OUT_FR, "04-premiere-app-offerte.png"), "01",
           "Votre première app est offerte",
           "Crédits de bienvenue à l'inscription.\nPrix fixe annoncé avant de lancer.")
    shutil.copy(os.path.join(SRC, "play-actuel-02.png"), os.path.join(OUT_FR, "05-exemple-gantt.png"))
    shutil.copy(os.path.join(SRC, "play-actuel-03.png"), os.path.join(OUT_FR, "06-exemple-tableau-de-bord.png"))
    shutil.copy(os.path.join(SRC, "play-actuel-05.png"), os.path.join(OUT_FR, "07-exemple-plans.png"))
    shutil.copy(os.path.join(SRC, "play-actuel-04.png"), os.path.join(OUT_FR, "08-exemple-rapport-signe.png"))

    # --- Anglais : les deux nouvelles captures (les autres gardent leurs legendes FR) ---
    hero(os.path.join(OUT_EN, "01-hero-en.png"),
         "Describe your app.\nGet it, ready to install.",
         "Designed, built and tested for you. No coding.")
    single(os.path.join(OUT_EN, "04-first-app-free-en.png"), "01",
           "Your first app is on us",
           "Welcome credits when you sign up.\nFixed price before anything starts.")

    # Decoupe du telephone "app livree" pour l'image de presentation (render.js)
    phone("06").save(os.path.join(ROOT, "outils", "phone-06.png"))
    phone("00").save(os.path.join(ROOT, "outils", "phone-00.png"))
    print("ok")


if __name__ == "__main__":
    main()
