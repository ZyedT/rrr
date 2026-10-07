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
    if badge:
        # Pastille translucide composee sur un calque a part (ImageDraw n'alpha-compose pas).
        fb = ImageFont.truetype(FONT_SEMI, 34)
        tw = ImageDraw.Draw(canvas).textlength(badge, font=fb)
        bx0, by0 = (W - tw) / 2 - 36, y - 10
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle((bx0, by0, bx0 + tw + 72, by0 + 60), radius=30, fill=(255, 255, 255, 46))
        canvas.alpha_composite(layer)
        ImageDraw.Draw(canvas).text((W / 2, by0 + 30), badge, font=fb, fill="white", anchor="mm")
        y += 86
    d = ImageDraw.Draw(canvas)
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


def screen_rect(frame_rgb):
    """Rectangle de l'ecran a l'interieur du cadre (la bordure noire est detectee
    sur la ligne et la colonne du milieu)."""
    a = np.asarray(frame_rgb)
    dark = a.max(axis=2) < 40
    H, W = dark.shape

    def inner(line):
        idx = np.where(line)[0]
        lo, hi = int(idx.min()), int(idx.max())
        while line[lo]:
            lo += 1
        while line[hi]:
            hi -= 1
        return lo, hi

    x0, x1 = inner(dark[H // 2])
    y0, y1 = inner(dark[:, W // 2])
    return x0, y0, x1, y1


def game(out, shot_path, title, subtitle, badge, status_bar=0.043, nav_bar=0.06):
    """Une capture reelle prise sur un telephone (barre d'etat et barre de navigation
    retirees) placee dans le cadre S26 des autres captures, avec legende."""
    canvas = background().convert("RGBA")
    caption(canvas, title, subtitle, y=110, title_size=78, sub_size=42, badge=badge)
    frame = phone("00")
    x0, y0, x1, y1 = screen_rect(frame.convert("RGB"))
    sw, sh = x1 - x0 + 1, y1 - y0 + 1
    shot = Image.open(shot_path).convert("RGB")
    w0, h0 = shot.size
    shot = shot.crop((0, int(h0 * status_bar), w0, h0 - int(h0 * nav_bar)))
    scale = max(sw / shot.size[0], sh / shot.size[1])
    shot = shot.resize((round(shot.size[0] * scale), round(shot.size[1] * scale)), Image.LANCZOS)
    cx, cy = (shot.size[0] - sw) // 2, (shot.size[1] - sh) // 2
    shot = shot.crop((cx, cy, cx + sw, cy + sh)).convert("RGBA")
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=80, fill=255)
    frame.paste(shot, (x0, y0), mask)
    paste_with_shadow(canvas, frame, (PHONE_BOX[0], PHONE_BOX[1]), blur=30, offset=(0, 20), alpha=90)
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
    game(os.path.join(OUT_FR, "08-jeu-3d.png"), os.path.join(SRC, "ping-crepuscule-04.jpg"),
         "Même des jeux 3D",
         "Décrit en une phrase, livré prêt à jouer.",
         badge="Exemple réel · Ping Crépuscule, créé avec AppForge")
    # Le 4e ecran ChantierPro reste disponible en extra (Play n'accepte que 8 captures).
    os.makedirs(os.path.join(OUT_FR, "extras"), exist_ok=True)
    shutil.copy(os.path.join(SRC, "play-actuel-04.png"), os.path.join(OUT_FR, "extras", "exemple-rapport-signe.png"))
    for old in ("08-exemple-rapport-signe.png",):
        if os.path.exists(os.path.join(OUT_FR, old)):
            os.remove(os.path.join(OUT_FR, old))

    # --- Anglais : les captures specifiques (les autres gardent leurs legendes FR) ---
    hero(os.path.join(OUT_EN, "01-hero-en.png"),
         "Describe your app.\nGet it, ready to install.",
         "Designed, built and tested for you. No coding.")
    single(os.path.join(OUT_EN, "04-first-app-free-en.png"), "01",
           "Your first app is on us",
           "Welcome credits when you sign up.\nFixed price before anything starts.")
    game(os.path.join(OUT_EN, "08-3d-game-en.png"), os.path.join(SRC, "ping-crepuscule-04.jpg"),
         "Even 3D games",
         "Described in one sentence, delivered ready to play.",
         badge="Real example · Ping Crépuscule, made with AppForge")

    # Decoupe du telephone "app livree" pour l'image de presentation (render.js)
    phone("06").save(os.path.join(ROOT, "outils", "phone-06.png"))
    phone("00").save(os.path.join(ROOT, "outils", "phone-00.png"))
    print("ok")


if __name__ == "__main__":
    main()
