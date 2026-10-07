#!/usr/bin/env python3
"""A partir d'un enregistrement d'ecran du telephone (portrait, sans barre d'etat),
fabrique les extraits video prets a monter :

  video/clips/<nom>-9x16.mp4      : l'extrait nettoye en 1080x1920 (Reels, TikTok, fiche)
  video/clips/<nom>-16x9-fr.mp4   : 1920x1080, le telephone dans le cadre S26 sur le fond
  video/clips/<nom>-16x9-en.mp4     de la marque, avec legende (plan B-roll pour la video Play)
  assets/sources/<nom>-05-cinematique.jpg : une image fixe du plan large

Usage : python3 make_clip.py <enregistrement.mp4> [nom]
Depend de ffmpeg et des fonctions de make_screens.py (meme dossier).
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_screens import FONT_BOLD, FONT_MED, FONT_SEMI, phone, screen_rect  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(ROOT, "video", "clips")
W, H = 1920, 1080

TEXT = {
    "fr": {"badge": "Exemple réel · Ping Crépuscule, créé avec AppForge", "title": "Même des jeux 3D",
           "sub": "Décrit en une phrase,\nlivré prêt à jouer.", "brand": "AppForge"},
    "en": {"badge": "Real example · Ping Crépuscule, made with AppForge", "title": "Even 3D games",
           "sub": "Described in one sentence,\ndelivered ready to play.", "brand": "AppForge"},
}


def gradient(w, h):
    """Degrade diagonal de la marque (indigo -> violet), comme l'image de presentation."""
    import numpy as np
    c0, c1, c2 = (46, 42, 140), (79, 70, 229), (126, 58, 237)
    yy, xx = np.mgrid[0:h, 0:w]
    t = (xx / w * 0.6 + yy / h * 0.4)
    t1 = np.clip(t / 0.52, 0, 1)[..., None]
    t2 = np.clip((t - 0.52) / 0.48, 0, 1)[..., None]
    a = np.array(c0) * (1 - t1) + np.array(c1) * t1
    b = a * (1 - t2) + np.array(c2) * t2
    return Image.fromarray(b.astype("uint8"), "RGB").convert("RGBA")


def overlay(lang):
    """Fond + legende + cadre du telephone avec un trou transparent a la place de l'ecran.
    Rend (chemin du PNG, rectangle du trou)."""
    t = TEXT[lang]
    canvas = gradient(W, H)
    frame = phone("00")
    sx0, sy0, sx1, sy1 = screen_rect(frame.convert("RGB"))
    scale = 1000 / frame.size[1]
    fw, fh = round(frame.size[0] * scale), 1000
    frame = frame.resize((fw, fh), Image.LANCZOS)
    fx, fy = W - fw - 150, (H - fh) // 2
    # trou transparent (coins arrondis) a l'emplacement de l'ecran
    hole = (fx + round(sx0 * scale), fy + round(sy0 * scale), fx + round((sx1 + 1) * scale), fy + round((sy1 + 1) * scale))
    hole_mask = Image.new("L", frame.size, 255)
    ImageDraw.Draw(hole_mask).rounded_rectangle(
        (round(sx0 * scale), round(sy0 * scale), round((sx1 + 1) * scale) - 1, round((sy1 + 1) * scale) - 1),
        radius=round(80 * scale), fill=0)
    alpha = Image.eval(frame.split()[3], lambda v: v)
    alpha = Image.composite(alpha, Image.new("L", frame.size, 0), hole_mask)
    frame.putalpha(alpha)
    # ombre du telephone, puis cadre
    from make_screens import paste_with_shadow
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_with_shadow(layer, frame, (fx, fy), blur=30, offset=(0, 18), alpha=110)
    # le trou doit rester transparent apres l'ombre
    hole_full = Image.new("L", (W, H), 255)
    ImageDraw.Draw(hole_full).rounded_rectangle((hole[0], hole[1], hole[2] - 1, hole[3] - 1), radius=round(80 * scale), fill=0)
    canvas = Image.composite(Image.alpha_composite(canvas, layer), Image.new("RGBA", (W, H), (0, 0, 0, 0)), hole_full)
    # legende a gauche
    d = ImageDraw.Draw(canvas)
    fb, ft, fs, fbr = (ImageFont.truetype(FONT_SEMI, 30), ImageFont.truetype(FONT_BOLD, 96),
                       ImageFont.truetype(FONT_MED, 44), ImageFont.truetype(FONT_BOLD, 40))
    x = 150
    # marque
    d.rounded_rectangle((x, 150, x + 56, 206), radius=14, fill=(255, 255, 255, 40))
    d.polygon([(x + 28, 158), (x + 33, 173), (x + 48, 178), (x + 33, 183), (x + 28, 198), (x + 23, 183), (x + 8, 178), (x + 23, 173)], fill="white")
    d.text((x + 72, 178), t["brand"], font=fbr, fill="white", anchor="lm")
    # pastille
    tw = d.textlength(t["badge"], font=fb)
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((x, 300, x + tw + 56, 356), radius=28, fill=(255, 255, 255, 46))
    canvas = Image.alpha_composite(canvas, pill)
    d = ImageDraw.Draw(canvas)
    d.text((x + 28, 328), t["badge"], font=fb, fill="white", anchor="lm")
    d.text((x, 410), t["title"], font=ft, fill="white")
    d.multiline_text((x, 560), t["sub"], font=fs, fill=(232, 229, 255), spacing=10)
    out = os.path.join(CLIPS, f"_overlay_{lang}.png")
    canvas.save(out)
    return out, hole


def run(cmd):
    print("$", " ".join(cmd[:6]), "…")
    subprocess.run(cmd, check=True)


def main(src, name="ping-crepuscule"):
    os.makedirs(CLIPS, exist_ok=True)
    loud = "loudnorm=I=-16:TP=-1.5:LRA=11"
    # 1) extrait 9:16 (le haut, avec le score, est garde ; on rogne le bas)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src,
         "-vf", "crop=in_w:min(in_h\\,in_w*16/9):0:0,scale=1080:1920,fps=30,format=yuv420p",
         "-af", loud, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
         "-movflags", "+faststart", os.path.join(CLIPS, f"{name}-9x16.mp4")])
    # 2) B-roll 16:9 FR / EN : la video dans le trou du cadre
    for lang in ("fr", "en"):
        png, (hx0, hy0, hx1, hy1) = overlay(lang)
        hw, hh = hx1 - hx0, hy1 - hy0
        filt = (f"[0:v]scale={hw}:{hh}:force_original_aspect_ratio=increase,crop={hw}:{hh},fps=30[v];"
                f"color=c=black:s={W}x{H}:r=30[bg];[bg][v]overlay={hx0}:{hy0}:shortest=1[tmp];"
                f"[tmp][1:v]overlay=0:0,format=yuv420p")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-i", png,
             "-filter_complex", filt, "-af", loud, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", os.path.join(CLIPS, f"{name}-16x9-{lang}.mp4")])
        os.remove(png)
    # 3) une image fixe du plan large (vers 5,5 s)
    still = os.path.join(ROOT, "assets", "sources", f"{name}-05-cinematique.jpg")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "5.5", "-i", src, "-frames:v", "1", "-q:v", "2", still])
    print(json.dumps({"clips": sorted(os.listdir(CLIPS)), "still": os.path.relpath(still, ROOT)}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], *(sys.argv[2:3]))
