"""Generador de presentaciones de NaranjaTec.

Uso:
    python build/build.py            # genera TODAS las presentaciones
    python build/build.py test       # genera solo el muestrario de disenos
    python build/build.py --list     # lista los decks disponibles

Cada deck es un modulo de contenido (en content/ o templates/) que expone:
    OUTFILE : nombre del .pptx de salida
    build(prs) : funcion que anade las diapositivas

El resultado se guarda en output/.
"""

import importlib
import sys
from pathlib import Path

# Permite ejecutar el script desde cualquier sitio: anade la raiz del proyecto
# (carpeta padre de build/) al path para importar brand/, lib/, content/...
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import lib.slides as s  # noqa: E402

# Mapa de alias -> modulo de contenido.
# Solo se registra el muestrario de disenos (una diapositiva de cada tipo). Los
# decks de cliente NO viven en este repo publico: se generan a partir del
# documento del cliente donde este, y su .pptx (con datos reales) no se versiona.
DECKS = {
    "test": "content.muestrario",
}


def generar(alias):
    modname = DECKS[alias]
    mod = importlib.import_module(modname)
    prs = s.new_presentation()
    mod.build(prs)
    out_dir = ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / mod.OUTFILE
    prs.save(str(out_path))
    print("  [ok] %-14s -> output/%s (%d diapositivas)"
          % (alias, mod.OUTFILE, len(prs.slides._sldIdLst)))
    return out_path


def main(argv):
    if argv and argv[0] in ("--list", "-l"):
        print("Decks disponibles:")
        for alias, mod in DECKS.items():
            print("  %-14s %s" % (alias, mod))
        return 0

    if argv:
        alias = argv[0]
        if alias not in DECKS:
            print("Deck desconocido: %s" % alias)
            print("Usa uno de: %s" % ", ".join(DECKS))
            return 1
        objetivos = [alias]
    else:
        objetivos = list(DECKS)

    print("Generando presentaciones NaranjaTec...")
    for alias in objetivos:
        generar(alias)
    print("Listo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
