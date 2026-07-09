"""Previsualiza un deck sin PowerPoint, usando LibreOffice headless.

Pensado para entornos sin PowerPoint (Claude Cowork, Linux, CI): convierte el
.pptx a PDF con LibreOffice y, si hay pdftoppm (poppler) disponible, rasteriza
cada pagina a PNG para poder revisarlas una a una.

Uso:
    python scripts/preview.py test              # genera el deck y lo previsualiza
    python scripts/preview.py nereidas --dpi 120
    python scripts/preview.py output/Otro.pptx  # previsualiza un .pptx existente
    python scripts/preview.py --install-fonts   # instala las fuentes de marca

Salida: output/preview/<nombre-del-deck>/pagina-NN.png (y el .pdf intermedio).

IMPORTANTE: sin las fuentes de marca instaladas en ESTA maquina, LibreOffice
sustituye la tipografia y los iconos salen como cajas. Ejecuta --install-fonts
una vez antes de la primera previsualizacion.
"""

import argparse
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FONTS_DIR = ROOT / "brand" / "assets" / "fonts"
PREVIEW_DIR = ROOT / "output" / "preview"

# LibreOffice no siempre esta en el PATH: probamos tambien las rutas tipicas.
SOFFICE_CANDIDATES = (
    "soffice",
    "libreoffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
)


def find_exe(candidates):
    """Devuelve el primer ejecutable disponible, o None."""
    for c in candidates:
        found = shutil.which(c)
        if found:
            return found
        p = Path(c)
        if p.is_file():
            return str(p)
    return None


def brand_font_files():
    """Los .ttf estaticos de las 4 familias + la fuente de iconos.

    Se ignoran las VariableFont: PowerPoint (y LibreOffice) no seleccionan bien
    los pesos de una fuente variable. La de iconos ya viene congelada a peso 300
    por scripts/make_icon_font.py.
    """
    files = [f for f in FONTS_DIR.glob("*/static/*.ttf")]
    icons = FONTS_DIR / "Material_Icons"
    files += list(icons.glob("*.ttf")) + list(icons.glob("*.otf"))
    return files


def install_fonts():
    """Instala las fuentes de marca para el usuario actual (Linux / macOS)."""
    fonts = brand_font_files()
    if not fonts:
        print("[error] no encuentro las fuentes en %s" % FONTS_DIR)
        return 1

    if sys.platform.startswith("win"):
        print("En Windows: selecciona los .ttf/.otf y clic derecho -> Instalar.")
        print("Detalle en brand/assets/fonts/README.md")
        return 1

    if sys.platform == "darwin":
        dest = Path.home() / "Library" / "Fonts"
    else:
        dest = Path.home() / ".local" / "share" / "fonts" / "naranjatec"

    dest.mkdir(parents=True, exist_ok=True)
    for f in fonts:
        shutil.copy2(f, dest / f.name)
    print("[ok] %d fuentes copiadas a %s" % (len(fonts), dest))

    fc_cache = shutil.which("fc-cache")
    if fc_cache:
        subprocess.run([fc_cache, "-f"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[ok] cache de fuentes regenerada (fc-cache -f)")
    return 0


def load_build():
    """Importa build/build.py sin depender de que sea un paquete."""
    spec = importlib.util.spec_from_file_location(
        "nt_build", ROOT / "build" / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_pptx(target):
    """Un alias de DECKS se genera al vuelo; una ruta se usa tal cual."""
    build = load_build()
    if target in build.DECKS:
        print("Generando el deck '%s'..." % target)
        return Path(build.generar(target))

    path = Path(target)
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        raise SystemExit(
            "No es un alias de DECKS ni un fichero existente: %s\n"
            "Alias disponibles: %s" % (target, ", ".join(build.DECKS)))
    return path


def to_pdf(pptx, outdir, soffice):
    """Convierte .pptx -> .pdf. Usa un perfil temporal para no chocar con una
    instancia de LibreOffice ya abierta (falla en silencio si comparten perfil).
    """
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            soffice,
            "-env:UserInstallation=file://%s" % Path(profile).as_posix(),
            "--headless", "--norestore",
            "--convert-to", "pdf",
            "--outdir", str(outdir),
            str(pptx),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    pdf = outdir / (pptx.stem + ".pdf")
    if not pdf.is_file():
        print("[error] LibreOffice no produjo el PDF.")
        if res.stdout.strip():
            print(res.stdout.strip())
        if res.stderr.strip():
            print(res.stderr.strip())
        raise SystemExit(1)
    return pdf


def to_png(pdf, outdir, dpi, pdftoppm):
    """Rasteriza el PDF a un PNG por pagina."""
    prefix = outdir / "pagina"
    cmd = [pdftoppm, "-r", str(dpi), "-png", str(pdf), str(prefix)]
    subprocess.run(cmd, check=True, timeout=600)
    return sorted(outdir.glob("pagina-*.png"))


def main(argv):
    ap = argparse.ArgumentParser(
        description="Previsualiza un deck con LibreOffice headless.")
    ap.add_argument("target", nargs="?",
                    help="alias de DECKS (test, nereidas) o ruta a un .pptx")
    ap.add_argument("--dpi", type=int, default=110,
                    help="resolucion de los PNG (por defecto 110)")
    ap.add_argument("--pdf-only", action="store_true",
                    help="no rasterizar a PNG, dejar solo el PDF")
    ap.add_argument("--install-fonts", action="store_true",
                    help="instalar las fuentes de marca y salir")
    args = ap.parse_args(argv)

    if args.install_fonts:
        return install_fonts()

    if not args.target:
        ap.print_help()
        return 1

    soffice = find_exe(SOFFICE_CANDIDATES)
    if not soffice:
        print("[error] no encuentro LibreOffice (soffice).")
        print("  Linux:  sudo apt-get install -y libreoffice-impress poppler-utils")
        print("  macOS:  brew install --cask libreoffice")
        return 1

    pptx = resolve_pptx(args.target)
    outdir = PREVIEW_DIR / pptx.stem

    print("Convirtiendo a PDF con LibreOffice...")
    pdf = to_pdf(pptx, outdir, soffice)
    print("  [ok] %s" % pdf.relative_to(ROOT))

    if args.pdf_only:
        return 0

    pdftoppm = find_exe(("pdftoppm",))
    if not pdftoppm:
        print("[aviso] falta pdftoppm (poppler): me quedo en el PDF.")
        print("  Linux: sudo apt-get install -y poppler-utils")
        print("  macOS: brew install poppler")
        return 0

    print("Rasterizando a PNG (%d dpi)..." % args.dpi)
    pages = to_png(pdf, outdir, args.dpi, pdftoppm)
    print("  [ok] %d paginas en %s" % (len(pages), outdir.relative_to(ROOT)))

    if not brand_font_files():
        return 0
    print("\nSi la tipografia no es la de marca o los iconos salen como cajas,")
    print("ejecuta: python scripts/preview.py --install-fonts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
