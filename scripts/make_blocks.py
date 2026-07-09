"""Rasteriza los SVG de bloques a PNG para poder usarlos en los .pptx.

`python-pptx` NO acepta SVG (falla con UnidentifiedImageError), asi que el SVG es
la fuente portable -- reutilizable en web, Figma o cualquier otro proyecto -- y de
el se deriva un PNG transparente que es lo que se inserta en la diapositiva.

Se rasteriza con Edge en modo headless, igual que el logo blanco: en este entorno
no hay cairosvg ni inkscape, ni ruedas de reportlab para Python 3.14.

Uso:
    python scripts/make_blocks.py            # todos los SVG que hayan cambiado
    python scripts/make_blocks.py --force    # rehacer todos
    python scripts/make_blocks.py --scale 6  # mas resolucion (por defecto 4)

Entrada:  brand/assets/blocks/*.svg   (viewBox 320x180)
Salida:   brand/assets/blocks/png/*.png
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand" / "assets" / "blocks"
DST = SRC / "png"

# Tamano del viewBox de la biblioteca. Si cambia, cambiarlo aqui.
VB_W, VB_H = 320, 180

EDGE_CANDIDATES = (
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "msedge",
    "microsoft-edge",
    "google-chrome",
    "chromium",
)


def find_edge():
    for c in EDGE_CANDIDATES:
        p = Path(c)
        if p.is_file():
            return str(p)
        found = shutil.which(c)
        if found:
            return found
    return None


def rasterize(edge, svg, png, scale):
    """SVG -> PNG transparente, via captura headless."""
    w, h = VB_W * scale, VB_H * scale
    # El SVG se envuelve en un HTML para controlar el tamano exacto y que no
    # aparezcan barras ni margenes del navegador.
    html = (
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;background:transparent}"
        "img{display:block;width:%dpx;height:%dpx}</style>"
        "<img src='%s'>" % (w, h, svg.as_uri())
    )
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html, encoding="utf-8")
        shot = Path(tmp) / "shot.png"
        cmd = [
            edge, "--headless=new", "--disable-gpu",
            "--default-background-color=00000000",
            "--hide-scrollbars",
            "--screenshot=%s" % shot,
            "--window-size=%d,%d" % (w, h),
            page.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not shot.is_file():
            print("[error] %s: Edge no genero el PNG" % svg.name)
            if res.stderr.strip():
                print("  " + res.stderr.strip().splitlines()[-1])
            return False
        DST.mkdir(parents=True, exist_ok=True)
        shutil.copy2(shot, png)
    return True


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true",
                    help="rehacer aunque el PNG este al dia")
    ap.add_argument("--scale", type=int, default=4,
                    help="multiplicador de resolucion (por defecto 4 -> 1280x720)")
    args = ap.parse_args(argv)

    svgs = sorted(SRC.glob("*.svg"))
    if not svgs:
        print("[error] no hay SVG en %s" % SRC.relative_to(ROOT))
        return 1

    edge = find_edge()
    if not edge:
        print("[error] no encuentro Edge/Chrome para rasterizar.")
        print("  El SVG es la fuente; el PNG hace falta porque python-pptx no")
        print("  acepta SVG. En Linux: apt-get install chromium.")
        return 1

    hechos = 0
    for svg in svgs:
        png = DST / (svg.stem + ".png")
        if not args.force and png.is_file() and \
                png.stat().st_mtime >= svg.stat().st_mtime:
            print("  [--] %-22s al dia" % svg.name)
            continue
        if rasterize(edge, svg, png, args.scale):
            kb = png.stat().st_size / 1024.0
            print("  [ok] %-22s -> png/%s (%.0f KB)" % (svg.name, png.name, kb))
            hechos += 1
    print("Listo: %d de %d rasterizados." % (hechos, len(svgs)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
