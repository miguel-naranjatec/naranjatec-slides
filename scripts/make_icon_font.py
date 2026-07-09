"""Construye la fuente de iconos de marca a partir de Material Symbols.

Google distribuye Material Symbols Outlined como fuente VARIABLE (ejes FILL,
GRAD, opsz, wght). PowerPoint no sabe elegir una instancia de un eje variable,
asi que aqui la "congelamos": se fija wght al peso que queremos y se guarda un
.ttf estatico que si se puede instalar y usar.

La familia resultante se llama "Material Symbols Outlined <peso>" (p.ej.
"Material Symbols Outlined 300"), NO "Material Symbols Outlined" a secas. Es
deliberado: si usara el nombre estandar y alguien tuviera ya instalada la fuente
oficial de Google, PowerPoint cogeria esa (peso 400) y el deck se veria mal sin
que nadie lo notase. Con un nombre propio, si la fuente falta salen cajas: un
fallo ruidoso, que se arregla.

Requiere fonttools (solo para construir la fuente, no para generar decks):

    pip install fonttools

Uso:
    python scripts/make_icon_font.py                # peso 300 (el de marca)
    python scripts/make_icon_font.py --weight 250
    python scripts/make_icon_font.py --src ruta/a/MaterialSymbolsOutlined.ttf

Escribe en brand/assets/fonts/Material_Icons/ el .ttf y el .codepoints, e
imprime el dict ICON listo para pegar en brand/theme.py.
"""

import argparse
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "brand" / "assets" / "fonts" / "Material_Icons"

BASE = ("https://raw.githubusercontent.com/google/material-design-icons"
        "/master/variablefont")
VAR_NAME = "MaterialSymbolsOutlined%5BFILL%2CGRAD%2Copsz%2Cwght%5D"

# Nombre semantico -> nombre del icono en Material Symbols. La clave es la que
# se usa en el codigo (T.ICON["cloud"]); el valor es el nombre oficial de Google,
# que es lo unico estable entre versiones (los codepoints cambian).
ICON_NAMES = {
    "globe": "public", "cloud": "cloud", "server": "dns", "rack": "lan",
    "network": "hub", "mail": "mail", "lock": "lock", "cert": "verified",
    "shield": "shield", "wrench": "build", "gear": "settings",
    "monitor": "desktop_windows", "cart": "shopping_cart",
    "mobile": "smartphone", "code": "code", "person": "person",
    "people": "groups", "storage": "storage", "bolt": "bolt", "sync": "sync",
    "pulse": "monitor_heart", "check": "check_circle", "phone": "call",
    "quote": "format_quote", "star": "grade", "idea": "lightbulb",
    "arrow": "arrow_forward", "location": "location_on", "tick": "check",
}


def download(url, dst):
    with urllib.request.urlopen(url, timeout=120) as r:
        dst.write_bytes(r.read())
    return dst


def load_codepoints(path):
    d = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            name, hexcode = line.split()
            d[name] = hexcode.lower()
    return d


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--weight", type=int, default=300,
                    help="peso a congelar (100-700; por defecto 300)")
    ap.add_argument("--src", help="ruta a la variable ya descargada (opcional)")
    args = ap.parse_args(argv)

    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
    except ImportError:
        print("[error] falta fonttools. Instala con: pip install fonttools")
        return 1

    tmp = Path(tempfile.mkdtemp())
    if args.src:
        var_ttf = Path(args.src)
        cps = var_ttf.with_suffix(".codepoints")
        if not cps.is_file():
            cps = download("%s/%s.codepoints" % (BASE, VAR_NAME),
                           tmp / "src.codepoints")
    else:
        print("Descargando Material Symbols Outlined (variable)...")
        var_ttf = download("%s/%s.ttf" % (BASE, VAR_NAME), tmp / "src.ttf")
        cps = download("%s/%s.codepoints" % (BASE, VAR_NAME),
                       tmp / "src.codepoints")

    codepoints = load_codepoints(cps)
    faltan = [k for k, n in ICON_NAMES.items() if n not in codepoints]
    if faltan:
        print("[error] iconos sin equivalente en la fuente: %s" % faltan)
        return 1

    family = "Material Symbols Outlined %d" % args.weight
    print("Congelando wght=%d (FILL=0, GRAD=0, opsz=24)..." % args.weight)
    font = TTFont(var_ttf)
    instancer.instantiateVariableFont(
        font, {"wght": args.weight, "FILL": 0, "GRAD": 0, "opsz": 24},
        inplace=True, updateFontNames=False)

    # Nombre de familia propio: ver el docstring (fallo ruidoso > silencioso).
    ps_name = "MaterialSymbolsOutlined%d-Regular" % args.weight
    name_table = font["name"]
    for nid, value in ((1, family), (2, "Regular"),
                       (4, family), (6, ps_name)):
        name_table.setName(value, nid, 3, 1, 0x409)  # Windows / Unicode BMP
        name_table.setName(value, nid, 1, 0, 0)      # Mac / Roman
    # Los nombres tipograficos (16/17) confundirian a PowerPoint: fuera.
    for nid in (16, 17):
        name_table.removeNames(nameID=nid)

    DEST.mkdir(parents=True, exist_ok=True)
    out_ttf = DEST / ("%s.ttf" % ps_name)
    font.save(out_ttf)
    print("[ok] %s  (%.1f MB)" % (out_ttf.relative_to(ROOT),
                                  out_ttf.stat().st_size / 1048576))

    out_cps = out_ttf.with_suffix(".codepoints")
    out_cps.write_bytes(cps.read_bytes())
    print("[ok] %s" % out_cps.relative_to(ROOT))

    print("\nFONT_ICON = \"%s\"\n" % family)
    print("ICON = {")
    items = list(ICON_NAMES)
    for i in range(0, len(items), 4):
        chunk = items[i:i + 4]
        line = "    " + " ".join(
            '"%s": "\\u%s",' % (k, codepoints[ICON_NAMES[k]].upper())
            for k in chunk)
        print(line)
    print("}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
