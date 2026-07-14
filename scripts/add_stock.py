# -*- coding: utf-8 -*-
"""Procesa las fotos que haya en `stock-entrada/` y las mete en la biblioteca.

La busqueda NO la hace este script: la haces tu, a mano, en Burst o en Pexels. Ese
es el punto. `brand/imagenes.py` existe porque elegir imagenes por palabra clave es
como acabas poniendo pulseras en una propuesta de chocolate; un script que busca
"chocolate" en una API y se baja los diez primeros resultados repite ese error
contra un catalogo de millones. Un deck necesita seis u ocho fotos: elegirlas es un
juicio. Lo mecanico, que es lo de abajo, si lo hace bien una maquina.

    python scripts/add_stock.py              # procesa el buzon, preguntando
    python scripts/add_stock.py --dry-run    # dice que haria, sin tocar nada
    python scripts/add_stock.py --keep       # no vacia el buzon al terminar

Por cada foto: pregunta sector, que se ve, tipo y credito; la optimiza (1920 px de
ancho como el resto de la biblioteca, sin EXIF), la renombra `sector-slug.jpg`, la
mueve a `brand/assets/img/stock/` y la registra en `stock.json`, que es de donde
`brand/imagenes.py` saca el catalogo. Al final reescribe `CREDITS.md`.

ASCII puro (es codigo). Las descripciones que escribas si pueden llevar acentos:
van al JSON, que es UTF-8.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BUZON = ROOT / "stock-entrada"
STOCK_DIR = ROOT / "brand" / "assets" / "img" / "stock"
META = STOCK_DIR / "stock.json"
CREDITS = STOCK_DIR / "CREDITS.md"

EXTS = (".jpg", ".jpeg", ".png", ".webp")

# Las mismas medidas que el resto de la biblioteca: 1920 de ancho, y con calidad 85
# los JPEG caen donde estan los demas (mediana 208 KB).
ANCHO_MAX = 1920
CALIDAD = 85

TIPOS = ("producto", "lugar", "personas")

FUENTES = {
    "burst": "Burst (Shopify)",
    "pexels": "Pexels",
    "pixabay": "Pixabay",
}


def _slug(texto):
    """'Bombones artesanos!' -> 'bombones-artesanos'. Sin acentos: es un nombre de
    fichero, y la biblioteca entera es ASCII."""
    s = unicodedata.normalize("NFKD", texto)
    s = s.encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-{2,}", "-", s)


def _cargar():
    if META.exists():
        return json.loads(META.read_text(encoding="utf-8"))
    return {}


def _preguntar(prompt, defecto=None, opciones=None):
    pista = ""
    if opciones:
        pista = " [%s]" % "/".join(opciones)
    if defecto:
        pista += " (%s)" % defecto
    while True:
        try:
            r = input("  %s%s: " % (prompt, pista)).strip()
        except EOFError:
            r = ""
        if not r and defecto:
            return defecto
        if not r:
            print("    (obligatorio)")
            continue
        if opciones and r not in opciones:
            print("    tiene que ser uno de: %s" % ", ".join(opciones))
            continue
        return r


def _optimizar(origen, destino, dry_run=False):
    """A JPEG, maximo ANCHO_MAX de ancho, sin EXIF. Devuelve (ancho, alto, KB).

    El `with` no es cosmetico: en Windows, un Image.open sin cerrar deja el fichero
    BLOQUEADO, y luego vaciar el buzon revienta con PermissionError."""
    with Image.open(origen) as src:
        # Un PNG con transparencia, sobre fondo blanco: el deck no usa alfa.
        if src.mode in ("RGBA", "LA", "P"):
            im = src.convert("RGBA")
            fondo = Image.new("RGB", im.size, (255, 255, 255))
            fondo.paste(im, mask=im.split()[-1])
            im = fondo
        else:
            im = src.convert("RGB")
    if im.width > ANCHO_MAX:
        alto = round(im.height * ANCHO_MAX / im.width)
        im = im.resize((ANCHO_MAX, alto), Image.LANCZOS)
    if dry_run:
        return im.width, im.height, 0
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Sin `exif=`: Pillow no copia los metadatos, que es lo que queremos (pueden
    # llevar GPS y modelo de camara, y engordan el fichero para nada).
    im.save(destino, "JPEG", quality=CALIDAD, optimize=True, progressive=True)
    return im.width, im.height, destino.stat().st_size // 1024


def _credits(meta):
    """Reescribe CREDITS.md entero desde el JSON: una sola fuente de verdad."""
    lineas = [
        "# Creditos de las fotos de stock",
        "",
        "Generado por `scripts/add_stock.py`. No editar a mano: se reescribe.",
        "",
        "Ninguna de estas licencias EXIGE atribucion, pero se anota igual: saber de",
        "donde salio cada foto es lo que permite responder si algun dia alguien",
        "pregunta, y reemplazarla si cambia su licencia.",
        "",
    ]
    porfuente = {}
    for fich, m in sorted(meta.items()):
        porfuente.setdefault(m["fuente"], []).append((fich, m))
    for fuente in sorted(porfuente):
        lineas.append("## %s" % fuente)
        lineas.append("")
        for fich, m in porfuente[fuente]:
            autor = m.get("autor") or ""
            credito = ("Autor no indicado" if autor in ("", "no indicado")
                       else "Foto de %s" % autor)
            url = m.get("url") or ""
            sufijo = " - %s" % url if url else ""
            lineas.append("- `%s` - %s. %s%s"
                          % (fich, m["desc"], credito, sufijo))
        lineas.append("")
    lineas.append("%d fotos." % len(meta))
    lineas.append("")
    return "\n".join(lineas)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="di que harias, sin escribir nada")
    ap.add_argument("--keep", action="store_true",
                    help="no borres los originales del buzon")
    args = ap.parse_args(argv)

    entrantes = sorted(p for p in BUZON.iterdir()
                       if p.is_file() and p.suffix.lower() in EXTS)
    if not entrantes:
        print("El buzon esta vacio: %s" % BUZON)
        print("Suelta ahi las fotos que bajes (ver stock-entrada/README.md).")
        return 0

    import brand.imagenes as IM
    sectores = IM.sectores()
    print("%d foto(s) en el buzon.\n" % len(entrantes))
    print("Sectores que ya existen: %s" % ", ".join(sectores))
    print("(puedes escribir uno nuevo si ninguno encaja)\n")

    meta = _cargar()
    hechas = []
    for p in entrantes:
        with Image.open(p) as im:
            w0, h0 = im.width, im.height
        print("%s  %dx%d  %d KB" % (p.name, w0, h0, p.stat().st_size // 1024))
        sector = _slug(_preguntar("sector"))
        desc = _preguntar("que se ve (una linea)")
        tipo = _preguntar("tipo", defecto="producto", opciones=list(TIPOS))
        autor = _preguntar("autor", defecto="no indicado")
        fkey = _preguntar("fuente", defecto="burst",
                          opciones=list(FUENTES)).lower()
        url = _preguntar("url de la foto", defecto="-")
        url = "" if url == "-" else url

        nombre = "%s-%s.jpg" % (sector, _slug(desc))
        if nombre in meta:
            # Dos fotos con la misma descripcion: -2, -3...
            i = 2
            while "%s-%s-%d.jpg" % (sector, _slug(desc), i) in meta:
                i += 1
            nombre = "%s-%s-%d.jpg" % (sector, _slug(desc), i)

        destino = STOCK_DIR / nombre
        w, h, kb = _optimizar(p, destino, dry_run=args.dry_run)
        meta[nombre] = {"sector": sector, "desc": desc, "tipo": tipo,
                        "autor": autor, "fuente": FUENTES[fkey], "url": url}
        hechas.append(p)
        print("  -> stock/%s  %dx%d  %s KB\n"
              % (nombre, w, h, kb if kb else "?"))

    if args.dry_run:
        print("--dry-run: no se ha escrito nada.")
        return 0

    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False,
                               sort_keys=True) + "\n", encoding="utf-8")
    CREDITS.write_text(_credits(meta), encoding="utf-8")
    if not args.keep:
        for p in hechas:
            p.unlink()

    print("%d foto(s) en la biblioteca. Total de stock: %d."
          % (len(hechas), len(meta)))
    print("Comprueba con:  python brand/imagenes.py --sector %s"
          % meta[list(meta)[-1]]["sector"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
