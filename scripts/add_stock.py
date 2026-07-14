# -*- coding: utf-8 -*-
"""Procesa las fotos que haya en `stock-entrada/` y las mete en la biblioteca.

La busqueda NO la hace este script: la haces tu, a mano, en Burst o en Pexels. Ese
es el punto. `brand/imagenes.py` existe porque elegir imagenes por palabra clave es
como acabas poniendo pulseras en una propuesta de chocolate; un script que busca
"chocolate" en una API y se baja los diez primeros resultados repite ese error
contra un catalogo de millones. Un deck necesita seis u ocho fotos: elegirlas es un
juicio. Lo mecanico, que es lo de abajo, si lo hace bien una maquina.

Dos modos, segun cuantas fotos traigas:

    python scripts/add_stock.py              # POCAS: pregunta foto a foto
    python scripts/add_stock.py --manifiesto # MUCHAS: escribe una tabla que rellenar
    python scripts/add_stock.py --aplicar    # ...y luego procesa lo que diga la tabla

El modo manifiesto existe porque el interactivo no escala: son seis preguntas por
foto, y sembrar la biblioteca de golpe (67 fotos de Burst) serian cuatrocientas
respuestas a mano. Con `--manifiesto` sale un TSV con una fila por foto; lo rellena
quien pueda MIRARLAS una a una (el agente lo hace barato, tu no), y tu lo revisas de
una sentada: cambias sectores, corriges descripciones y pones `no` en la columna
`usar` a lo que no quieras. Luego `--aplicar` procesa solo lo marcado con `si`.

    --dry-run    di que harias, sin escribir nada
    --keep       no vacies el buzon al terminar

Por cada foto: la optimiza (1920 px de ancho como el resto de la biblioteca, sin
EXIF), la renombra `sector-slug.jpg`, la mueve a `brand/assets/img/stock/` y la
registra en `stock.json`, que es de donde `brand/imagenes.py` saca el catalogo. Al
final reescribe `CREDITS.md`.

ASCII puro (es codigo). Las descripciones si pueden llevar acentos: van al TSV y al
JSON, que son UTF-8.
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
MANIFIESTO = BUZON / "manifiesto.tsv"
STOCK_DIR = ROOT / "brand" / "assets" / "img" / "stock"
META = STOCK_DIR / "stock.json"
CREDITS = STOCK_DIR / "CREDITS.md"

EXTS = (".jpg", ".jpeg", ".png", ".webp")

# Las mismas medidas que el resto de la biblioteca: 1920 de ancho, y con calidad 85
# los JPEG caen donde estan los demas (mediana 208 KB).
ANCHO_MAX = 1920
CALIDAD = 85

# `neutro` no es un cajon de sastre: es la etiqueta honesta de una foto que no habla
# de ningun sector (mar, ciudad, carretera) y que sirve de fondo de seccion o de
# portada. Llamarla "lugar" seria decir que ensena un sitio concreto del negocio.
TIPOS = ("producto", "lugar", "personas", "neutro")

FUENTES = {
    "burst": "Burst (Shopify)",
    "pexels": "Pexels",
    "pixabay": "Pixabay",
}

COLUMNAS = ("fichero", "usar", "sector", "tipo", "desc")
SI = ("si", "s", "yes", "y", "1", "x")


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


def _guardar(meta):
    """El JSON es la unica fuente de verdad: CREDITS.md se REGENERA de el, nunca al
    reves. Asi no pueden contradecirse."""
    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False,
                               sort_keys=True) + "\n", encoding="utf-8")
    CREDITS.write_text(_credits(meta), encoding="utf-8")


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


def _fotos():
    return sorted(p for p in BUZON.iterdir()
                  if p.is_file() and p.suffix.lower() in EXTS)


def _escribir_manifiesto(fotos, sectores):
    """Una fila por foto, con las columnas vacias. Las rellena quien MIRE las fotos
    (el agente), y las revisa el humano. No se deduce el sector del nombre del
    fichero: ese es exactamente el error que este repo lleva escrito en la pared."""
    lineas = [
        "# Manifiesto de stock. Una fila por foto; separado por TABULADORES.",
        "#",
        "# usar    si / no. Solo se procesan las 'si'.",
        "# sector  de que sector habla la foto. Los que ya existen:",
        "#         %s" % ", ".join(sectores),
        "#         Puedes inventar uno nuevo si ninguno encaja.",
        "# tipo    %s" % " / ".join(TIPOS),
        "#         'neutro' = no habla de ningun sector (mar, ciudad, carretera):",
        "#         sirve de fondo de seccion o de portada.",
        "# desc    que se ve, en una linea. De aqui sale el nombre del fichero.",
        "#",
        "# Cuando este a tu gusto:  python scripts/add_stock.py --aplicar",
        "",
        "\t".join(COLUMNAS),
    ]
    for p in fotos:
        lineas.append("\t".join([p.name, "", "", "", ""]))
    MANIFIESTO.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def _leer_manifiesto():
    """[(fichero, usar, sector, tipo, desc)] de las filas con datos."""
    filas = []
    for n, linea in enumerate(
            MANIFIESTO.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        campos = linea.split("\t")
        if campos[0].strip() == "fichero":          # la cabecera
            continue
        if len(campos) != len(COLUMNAS):
            raise SystemExit(
                "manifiesto.tsv, linea %d: %d columnas y esperaba %d. Separa con "
                "TABULADORES, no con espacios.\n  %r"
                % (n, len(campos), len(COLUMNAS), linea))
        filas.append(tuple(c.strip() for c in campos))
    return filas


def _nombre_libre(sector, desc, meta):
    base = "%s-%s" % (_slug(sector), _slug(desc))
    nombre = "%s.jpg" % base
    i = 2
    while nombre in meta:                # dos fotos con la misma desc: -2, -3...
        nombre = "%s-%d.jpg" % (base, i)
        i += 1
    return nombre


def _aplicar(args):
    """Procesa las filas del manifiesto marcadas con `usar=si`."""
    if not MANIFIESTO.exists():
        print("No hay manifiesto. Crealo con:  "
              "python scripts/add_stock.py --manifiesto")
        return 1
    filas = _leer_manifiesto()
    en_disco = {p.name: p for p in _fotos()}

    elegidas, descartadas, problemas = [], [], []
    for fich, usar, sector, tipo, desc in filas:
        if usar.lower() not in SI:
            descartadas.append(fich)
            continue
        if fich not in en_disco:
            problemas.append("%s: marcada como 'si' pero no esta en el buzon"
                             % fich)
        elif not sector or not desc:
            problemas.append("%s: falta %s" % (
                fich, "sector" if not sector else "desc"))
        elif tipo not in TIPOS:
            problemas.append("%s: tipo '%s'; tiene que ser uno de %s"
                             % (fich, tipo, ", ".join(TIPOS)))
        else:
            elegidas.append((en_disco[fich], sector, tipo, desc))

    if problemas:
        # No se procesa NADA a medias: o el manifiesto esta bien, o no se toca la
        # biblioteca. Un catalogo a medio escribir es peor que uno vacio.
        print("El manifiesto tiene %d problema(s):\n" % len(problemas))
        for p in problemas:
            print("  " + p)
        return 1

    print("%d elegidas, %d descartadas.\n" % (len(elegidas), len(descartadas)))
    meta = _cargar()
    hechas = []
    for p, sector, tipo, desc in elegidas:
        nombre = _nombre_libre(sector, desc, meta)
        w, h, kb = _optimizar(p, STOCK_DIR / nombre, dry_run=args.dry_run)
        meta[nombre] = {"sector": _slug(sector), "desc": desc, "tipo": tipo,
                        "autor": "no indicado", "fuente": FUENTES["burst"],
                        "url": ""}
        hechas.append(p)
        print("  %-46s -> stock/%s  (%dx%d, %s KB)"
              % (p.name, nombre, w, h, kb if kb else "?"))

    if args.dry_run:
        print("\n--dry-run: no se ha escrito nada.")
        return 0

    _guardar(meta)
    if not args.keep:
        for p in hechas:
            p.unlink()
        MANIFIESTO.unlink()

    print("\n%d foto(s) en la biblioteca. Total de stock: %d."
          % (len(hechas), len(meta)))
    if descartadas:
        # Las descartadas NO se borran: las bajaste tu, y borrarlas sin preguntar
        # es irreversible. El buzon esta gitignorado, asi que tampoco estorban.
        print("Quedan %d descartadas en el buzon. Borralas cuando quieras:"
              % len(descartadas))
        print("  rm stock-entrada/*.jpg")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifiesto", action="store_true",
                    help="escribe la tabla a rellenar, en vez de preguntar")
    ap.add_argument("--aplicar", action="store_true",
                    help="procesa las fotos marcadas con 'si' en la tabla")
    ap.add_argument("--dry-run", action="store_true",
                    help="di que harias, sin escribir nada")
    ap.add_argument("--keep", action="store_true",
                    help="no borres los originales del buzon")
    args = ap.parse_args(argv)

    entrantes = _fotos()
    if not entrantes:
        print("El buzon esta vacio: %s" % BUZON)
        print("Suelta ahi las fotos que bajes (ver stock-entrada/README.md).")
        return 0

    import brand.imagenes as IM
    sectores = IM.sectores()

    if args.manifiesto:
        _escribir_manifiesto(entrantes, sectores)
        print("%d foto(s) -> %s" % (len(entrantes), MANIFIESTO))
        print("Rellenalo (sector, tipo, desc, usar) y luego:")
        print("  python scripts/add_stock.py --aplicar")
        return 0

    if args.aplicar:
        return _aplicar(args)

    print("%d foto(s) en el buzon.\n" % len(entrantes))
    if len(entrantes) > 8:
        print("Son muchas para ir preguntando una a una (%d preguntas). Mejor:"
              % (len(entrantes) * 6))
        print("  python scripts/add_stock.py --manifiesto\n")
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

        nombre = _nombre_libre(sector, desc, meta)
        w, h, kb = _optimizar(p, STOCK_DIR / nombre, dry_run=args.dry_run)
        meta[nombre] = {"sector": sector, "desc": desc, "tipo": tipo,
                        "autor": autor, "fuente": FUENTES[fkey], "url": url}
        hechas.append(p)
        print("  -> stock/%s  %dx%d  %s KB\n"
              % (nombre, w, h, kb if kb else "?"))

    if args.dry_run:
        print("--dry-run: no se ha escrito nada.")
        return 0

    _guardar(meta)
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
