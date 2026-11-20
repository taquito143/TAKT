"""Genera el ícono de TAKT para Android: una T en itálica con el estilo del título
(relleno oscuro, contorno claro y extrusión hacia abajo-izquierda, luz desde la derecha).

Uso:  python scripts/make-icons.py   (desde la carpeta takt; necesita Pillow y Arial Black)
Escribe en android/app/src/main/res: mipmap-*/ic_launcher*.png y values/ic_launcher_background.xml
"""
import os
from PIL import Image, ImageDraw, ImageFont

BG = (13, 14, 18, 255)       # --bg de la app
INK = (241, 241, 241, 255)   # contorno y extrusión
FONT = r"C:\Windows\Fonts\ariblk.ttf"
RES = os.path.join(os.path.dirname(__file__), "..", "android", "app", "src", "main", "res")
DENS = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}


def letter(size, scale):
    """La T sobre fondo transparente, de `size` px, ocupando `scale` del alto."""
    S = size * 4  # se dibuja grande y se achica al final (bordes suaves)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, int(S * scale))
    stroke = max(2, int(S * scale * 0.07))
    depth = int(S * scale * 0.18)
    box = d.textbbox((0, 0), "T", font=font, stroke_width=stroke)
    w, h = box[2] - box[0], box[3] - box[1]
    x0 = (S - w) / 2 - box[0] + depth * 0.28
    y0 = (S - h) / 2 - box[1] - depth * 0.5
    # extrusión: el contorno repetido hacia abajo-izquierda, en pasos de 1 px
    for k in range(depth, 0, -1):
        d.text((x0 - k * 0.55, y0 + k), "T", font=font, fill=INK, stroke_width=stroke, stroke_fill=INK)
    d.text((x0, y0), "T", font=font, fill=BG, stroke_width=stroke, stroke_fill=INK)
    # itálica: arriba se corre a la derecha
    sh = 0.2
    img = img.transform((S, S), Image.AFFINE, (1, sh, -sh * S / 2, 0, 1, 0), resample=Image.BICUBIC)
    return img.resize((size, size), Image.LANCZOS)


def legacy(size, round_):
    """Ícono clásico (Android < 8): fondo oscuro redondeado o circular con la T."""
    S = size * 4
    base = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    m = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(m)
    if round_:
        md.ellipse((0, 0, S - 1, S - 1), fill=255)
    else:
        md.rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * 0.2), fill=255)
    base.paste(Image.new("RGBA", (S, S), BG), (0, 0), m)
    base = base.resize((size, size), Image.LANCZOS)
    base.alpha_composite(letter(size, 0.62))
    return base


for name, f in DENS.items():
    folder = os.path.join(RES, f"mipmap-{name}")
    os.makedirs(folder, exist_ok=True)
    legacy(int(48 * f), False).save(os.path.join(folder, "ic_launcher.png"))
    legacy(int(48 * f), True).save(os.path.join(folder, "ic_launcher_round.png"))
    # adaptativo: 108 dp, con la T dentro de la zona segura de 66 dp
    letter(int(108 * f), 0.42).save(os.path.join(folder, "ic_launcher_foreground.png"))

with open(os.path.join(RES, "values", "ic_launcher_background.xml"), "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0D0E12</color>\n</resources>\n')

# splash de Android < 12: las imágenes de Capacitor eran blancas; se reemplazan por el fondo oscuro de la app
import glob
for f in glob.glob(os.path.join(RES, "drawable*", "splash.png")):
    with Image.open(f) as im:
        size = im.size
    Image.new("RGB", size, BG[:3]).save(f)

# vista previa grande para revisar
letter(512, 0.42).save(os.path.join(os.path.dirname(__file__), "..", "..", "icono-preview-fg.png"))
legacy(512, False).save(os.path.join(os.path.dirname(__file__), "..", "..", "icono-preview.png"))
print("listo")
