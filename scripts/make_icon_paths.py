"""Extrae los contornos de los iconos de marca a brand/icon_paths.py.

Los iconos NO se pintan como texto con la fuente instalada: se dibujan como
formas nativas (a:custGeom) con la geometria real del glifo. Motivo: un run de
texto con un codepoint PUA (U+E000-U+F8FF) depende de que el receptor tenga la
fuente instalada Y de que su PowerPoint enrute el caracter a esa fuente. Los
codepoints PUA no pertenecen a ningun script, asi que ese enrutado es ambiguo:
en PowerPoint for Mac falla de forma intermitente, y macOS tiene fuentes de
sistema que reclaman parte del rango PUA, con lo que a veces sale un glifo
ajeno en vez de nada. Como forma nativa no hay fuente que resolver.

Es el mismo razonamiento que ya llevo la estrella de add_quote a MSO_SHAPE
(lib/slides.py) y el mismo patron que blocks/: fuente portable + artefacto
generado y commiteado.

Requiere fonttools (solo para generar los paths, no para generar decks):

    pip install fonttools

Uso:
    python scripts/make_icon_paths.py
    python scripts/make_icon_paths.py --src ruta/a/otra.ttf
    python scripts/make_icon_paths.py --check    # no escribe; falla si cambiaria

Lee el .ttf de brand/assets/fonts/Material_Icons/ y escribe brand/icon_paths.py.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

FONT_DIR = ROOT / "brand" / "assets" / "fonts" / "Material_Icons"
DEFAULT_TTF = FONT_DIR / "MaterialSymbolsOutlined300-Regular.ttf"
OUT = ROOT / "brand" / "icon_paths.py"

# El espacio de salida se escala x2 respecto al em de la fuente. Motivo: los
# contornos TrueType son cuadraticas con puntos off-curve implicitos; al
# decodificarlos, el punto on-curve implicito cae en el PUNTO MEDIO de dos
# off-curve enteros, o sea en .5. Multiplicando por 2 todos los nodos vuelven a
# ser enteros y la conversion es exacta (cero redondeo).
SCALE = 2

# Area minima (en unidades de fuente al cuadrado) para que un contorno cuente.
# instantiateVariableFont deja slivers degenerados de ancho cero al congelar el
# eje wght (p.ej. mail tiene un contorno de area -30 y anchura literal 0). Con
# ellos dentro, el relleno even-odd y el non-zero DEJAN DE COINCIDIR, y ahi
# empieza a importar que regla use cada renderizador. Filtrados, coinciden en
# los 29 iconos: es lo que hace que el enfoque no dependa de resolver esa
# ambiguedad de la especificacion. Ver tests/test_icon_paths.py.
MIN_AREA = 50.0


def _load_codepoints(path):
    d = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            name, hexcode = line.split()
            d[name] = hexcode.lower()
    return d


def _build_pen(BasePen):
    class _PathPen(BasePen):
        """Recoge los contornos del glifo como listas de segmentos.

        Subclasear BasePen (en vez de leer la tabla glyf a mano) resuelve gratis
        los dos casos peliagudos de TrueType, que ESTAN presentes en esta
        fuente: contornos sin ningun punto on-curve (21 casos: el circulo de la
        cabeza de person, network...) y runs de hasta 16 off-curve seguidos con
        on-curve implicitos en los puntos medios. BasePen.qCurveTo ya sintetiza
        unos y descompone otros.
        """

        def __init__(self, glyph_set):
            BasePen.__init__(self, glyph_set)
            self.contours = []
            self._cur = None

        def _moveTo(self, pt):
            self._cur = [("m", pt)]

        def _lineTo(self, pt):
            self._cur.append(("l", pt))

        def _qCurveToOne(self, ctrl, end):
            self._cur.append(("q", ctrl, end))

        def _curveToOne(self, c1, c2, end):
            # No lo produce esta fuente (es TrueType puro), pero si algun dia
            # entra un glifo CFF, DrawingML tiene a:cubicBezTo nativo.
            self._cur.append(("c", c1, c2, end))

        def _closePath(self):
            if self._cur:
                self.contours.append(self._cur)
                self._cur = None

        def _endPath(self):
            self._closePath()

    return _PathPen


def _area(contour, AreaPen):
    pen = AreaPen()
    pen.moveTo(contour[0][1])
    for seg in contour[1:]:
        if seg[0] == "l":
            pen.lineTo(seg[1])
        elif seg[0] == "q":
            pen.qCurveTo(seg[1], seg[2])
        elif seg[0] == "c":
            pen.curveTo(seg[1], seg[2], seg[3])
    pen.closePath()
    return pen.value


def _emit(pt, upem):
    """Unidades de fuente -> espacio del path. Invierte Y (la fuente crece hacia
    ARRIBA desde la baseline; DrawingML crece hacia ABAJO) y escala x2."""
    x = pt[0] * SCALE
    y = (upem - pt[1]) * SCALE
    xi, yi = int(round(x)), int(round(y))
    if abs(x - xi) > 1e-6 or abs(y - yi) > 1e-6:
        raise ValueError("coordenada no entera tras escalar x%d: %r" % (SCALE, pt))
    return xi, yi


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src", help="ruta al .ttf (por defecto el de marca)")
    ap.add_argument("--check", action="store_true",
                    help="no escribe; falla si el fichero generado cambiaria")
    args = ap.parse_args(argv)

    try:
        from fontTools.pens.areaPen import AreaPen
        from fontTools.pens.basePen import BasePen
        from fontTools.ttLib import TTFont
    except ImportError:
        print("[error] falta fonttools. Instala con: pip install fonttools")
        return 1

    from make_icon_font import ICON_NAMES
    import brand.theme as T

    ttf = Path(args.src) if args.src else DEFAULT_TTF
    if not ttf.is_file():
        print("[error] no existe la fuente: %s" % ttf)
        return 1

    cps_file = ttf.with_suffix(".codepoints")
    if not cps_file.is_file():
        print("[error] falta el .codepoints junto al .ttf: %s" % cps_file)
        return 1
    codepoints = _load_codepoints(cps_file)

    font = TTFont(ttf)
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    PathPen = _build_pen(BasePen)

    out = {}
    for key in ICON_NAMES:
        google = ICON_NAMES[key]
        if google not in codepoints:
            print("[error] '%s' no existe en la fuente" % google)
            return 1
        cp = int(codepoints[google], 16)

        # La verdad del codepoint vive en la fuente; theme.ICON es una copia a
        # mano. Si divergen, el deck pinta otro icono en silencio: reventamos.
        esperado = T.ICON.get(key)
        if esperado is None:
            print("[error] theme.ICON no tiene la clave '%s'" % key)
            return 1
        if ord(esperado) != cp:
            print("[error] '%s': theme.ICON dice U+%04X y la fuente U+%04X. "
                  "Regenera theme.ICON con make_icon_font.py."
                  % (key, ord(esperado), cp))
            return 1

        if cp not in cmap:
            print("[error] U+%04X no esta en el cmap" % cp)
            return 1

        pen = PathPen(glyph_set)
        glyph_set[cmap[cp]].draw(pen)

        contours = []
        for c in pen.contours:
            if abs(_area(c, AreaPen)) < MIN_AREA:
                continue          # sliver degenerado del congelado de wght
            path = [("m",) + _emit(c[0][1], upem)]
            for seg in c[1:]:
                if seg[0] == "l":
                    path.append(("l",) + _emit(seg[1], upem))
                elif seg[0] == "q":
                    path.append(("q",) + _emit(seg[1], upem) + _emit(seg[2], upem))
                elif seg[0] == "c":
                    path.append(("c",) + _emit(seg[1], upem) + _emit(seg[2], upem)
                                + _emit(seg[3], upem))
            path.append(("z",))
            contours.append(path)

        if not contours:
            print("[error] '%s' se queda sin contornos tras filtrar" % key)
            return 1

        lim = upem * SCALE
        for path in contours:
            for seg in path:
                for v in seg[1:]:
                    if not 0 <= v <= lim:
                        print("[error] '%s': coordenada %d fuera de [0, %d]"
                              % (key, v, lim))
                        return 1
        out[key] = contours

    text = _render(out, upem * SCALE)
    if args.check:
        actual = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if actual != text:
            print("[error] %s esta desactualizado. Ejecuta: "
                  "python scripts/make_icon_paths.py" % OUT.relative_to(ROOT))
            return 1
        print("[ok] %s al dia" % OUT.relative_to(ROOT))
        return 0

    OUT.write_text(text, encoding="ascii")
    nodos = sum(len(p) for c in out.values() for p in c)
    print("[ok] %s  (%d iconos, %d contornos, %d nodos, %.1f KB)"
          % (OUT.relative_to(ROOT), len(out),
             sum(len(c) for c in out.values()), nodos,
             len(text) / 1024))
    return 0


def _render(paths, box):
    L = []
    L.append('"""Contornos de los iconos de marca. GENERADO: no editar a mano.')
    L.append("")
    L.append("Lo escribe scripts/make_icon_paths.py a partir del .ttf de")
    L.append("brand/assets/fonts/Material_Icons/. Para cambiarlo, edita el")
    L.append("generador y vuelve a ejecutarlo.")
    L.append("")
    L.append("ICON_PATHS[nombre] es una lista de contornos; cada contorno es una")
    L.append("lista de segmentos:")
    L.append("")
    L.append('    ("m", x, y)                 mover a')
    L.append('    ("l", x, y)                 linea a')
    L.append('    ("q", cx, cy, x, y)         cuadratica (1 punto de control)')
    L.append('    ("c", c1x, c1y, c2x, c2y, x, y)   cubica')
    L.append('    ("z",)                      cerrar')
    L.append("")
    L.append("Las coordenadas son enteras y viven en la caja [0, %d] x [0, %d]"
             % (box, box))
    L.append("(ICON_BOX), con Y creciendo hacia ABAJO, ya listas para DrawingML.")
    L.append("Esa caja es el cuadrado del em, que en Material Symbols coincide")
    L.append("con la rejilla de diseno 24x24: por eso todos los iconos comparten")
    L.append("rejilla sin ajustar nada. NO normalizar al bbox del glifo, o un")
    L.append("icono estrecho (arrow) se veria del mismo tamano que uno que llena")
    L.append("la caja (globe).")
    L.append('"""')
    L.append("")
    L.append("ICON_BOX = %d" % box)
    L.append("")
    L.append("ICON_PATHS = {")
    for key in paths:
        L.append('    "%s": [' % key)
        for contour in paths[key]:
            L.append("        [")
            linea = "           "
            for seg in contour:
                txt = " %s," % repr(seg).replace("'", '"')
                if len(linea) + len(txt) > 78:
                    L.append(linea)
                    linea = "           "
                linea += txt
            if linea.strip():
                L.append(linea)
            L.append("        ],")
        L.append("    ],")
    L.append("}")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
