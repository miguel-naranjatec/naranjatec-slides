"""Que muestra cada imagen de la biblioteca, para poder elegirla y para poder
ADVERTIR cuando no hay ninguna adecuada. ASCII puro.

El hallazgo que hace falta tener presente antes de elegir una foto: esta
biblioteca NO es un banco de imagenes por temas. Son mockups de las webs que ha
hecho el estudio, montadas sobre portatiles, moviles e iMacs, mas fotos de la
oficina y algunos logos. Por eso `pighen-store.jpg` no es una tienda: es la web
de Pig&Hen, y lo que se ve son pulseras.

De ahi que la etiqueta util no sea "tienda" sino el SECTOR del cliente cuya web
aparece en la pantalla, y el TIPO de plano (portatil, movil, oficina...).

    python brand/imagenes.py --list             # el catalogo por sector
    python brand/imagenes.py --sector alimentacion

Uso desde un deck o desde el skill:

    import brand.imagenes as IM
    IM.buscar(sector="alimentacion")            # -> ["importaco-macbookpro.jpg", ...]
    IM.advertencia("chocolate artesanal")       # -> texto que hay que decirle al usuario
"""

import json
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

IMG_DIR = Path(__file__).resolve().parent / "assets" / "img"

# Las fotos de STOCK son lo unico que no es un mockup de cliente: son fotografia de
# verdad, bajada a mano de Burst o Pexels y procesada por `scripts/add_stock.py`.
# Su ficha (sector, que se ve, tipo, credito) vive en un JSON al lado de las fotos,
# no aqui: la escribe el script, y este modulo solo la lee.
STOCK_DIR = IMG_DIR / "stock"
STOCK_META = STOCK_DIR / "stock.json"


def stock():
    """{nombre.jpg: {"sector","desc","tipo","autor","fuente","url"}}. Vacio si aun
    no se ha metido ninguna foto."""
    if not STOCK_META.exists():
        return {}
    return json.loads(STOCK_META.read_text(encoding="utf-8"))


# El sector de cada cliente: lo que se VE en la pantalla del mockup. Un deck de
# chocolate no quiere la web de una tienda de pulseras aunque el fichero se llame
# "store". `desc` es lo que aparece, en una linea.
CLIENTES = {
    "abordo":          ("nautica", "web y tienda de material nautico"),
    "accesoonline":    ("software", "panel de control de accesos"),
    "accompany":       ("servicios", "consultoria para empresas en Espana"),
    "babidu":          ("moda", "tienda de ropa infantil y de bebe"),
    "beyma":           ("industria", "altavoces y componentes de audio"),
    "canonbcn":        ("tecnologia", "impresoras y equipamiento de oficina"),
    "choptime":        ("generico", "escritorio con web en portatil"),
    "credo":           ("inmobiliaria", "promocion de proyectos inmobiliarios"),
    "ecco":            ("software", "panel de rutas y logistica"),
    "gracielahuam":    ("moda", "tienda de moda de mujer"),
    "holanda":         ("medios", "portal de noticias y turismo"),
    "imporaco":        ("alimentacion", "sala de reuniones (fichero mal llamado:"
                                        " deberia ser importaco)"),
    "importaco":       ("alimentacion", "industria alimentaria, planta y batas"),
    "kenon":           ("retail", "app de compra desde el coche"),
    "liteserver":      ("hosting", "logotipo de un proveedor de hosting"),
    "localpoints":     ("retail", "app de tarjeta de fidelizacion"),
    "naranjatec":      ("marca-propia", "marca NaranjaTec: logo, carteles, rotulos"),
    "odoo":            ("software", "ERP Odoo en escritorio"),
    "pighen":          ("moda", "tienda de pulseras y accesorios"),
    "publirevista":    ("medios", "editor de revistas y publicaciones"),
    "requena":         ("medios", "revista local con tienda online"),
    "rume":            ("generico", "portatil sobre fondo oscuro"),
    "sinrodeos":       ("retail", "tienda online en neerlandes"),
    "springvale":      ("mobiliario", "tienda de sofas y muebles"),
    "sunfer":          ("industria", "estructuras y parkings solares"),
    "superq":          ("software", "app social en movil"),
    "tuempresa":       ("software", "app de empresa con codigo QR"),
    "valenciapremium": ("inmobiliaria", "inmuebles y turismo de lujo"),
    # OJO: en miniatura parece producto gourmet. No lo es: son brochas de afeitar.
    "vielong":         ("cosmetica", "afeitado tradicional: brochas y cuidado masculino"),
}

# Carpetas propias, que no son mockups de cliente.
CARPETAS = {
    "oficina": ("marca-propia", "fotos reales de la oficina de NaranjaTec"),
    "avatars": ("marca-propia", "logotipos de cliente usados como avatar"),
}

# El tipo de plano se deduce del nombre del fichero, por palabra clave. El orden
# importa: gana la primera que aparece.
TIPOS = (
    ("logo", ("logo",)),
    ("movil", ("mobile", "iphone", "samsung", "movil")),
    ("tablet", ("ipad", "tablet")),
    ("escritorio", ("imac", "desktop", "-mac", "dashboard", "website", "home",
                    "shop", "store", "stats", "night", "routes", "capture")),
    ("portatil", ("laptop", "macbook", "portatil", "ibook", "mockup", "design",
                  "web", "landing", "map", "news", "editor", "worksheet")),
    ("personas", ("meeting", "office", "working", "reuniones", "equipos",
                  "employees", "create", "report", "hand", "scan")),
    ("marca", ("bus", "flag", "light", "posters", "tela", "render",
               "illustration", "guia")),
)


def _tipo(nombre):
    n = nombre.lower()
    for tipo, claves in TIPOS:
        if any(k in n for k in claves):
            return tipo
    return "otro"


def _cliente(rel):
    if "/" in rel:
        carpeta = rel.split("/", 1)[0]
        if carpeta in CARPETAS:
            return carpeta, CARPETAS[carpeta]
    base = rel.split("/")[-1]
    for pref in sorted(CLIENTES, key=len, reverse=True):
        if base.startswith(pref):
            return pref, CLIENTES[pref]
    return None, None


def catalogo():
    """[(ruta relativa, sector, tipo, desc)] de todas las imagenes en disco."""
    st = stock()
    filas = []
    for p in sorted(IMG_DIR.rglob("*.jpg")):
        rel = p.relative_to(IMG_DIR).as_posix()
        if rel.startswith("stock/"):
            # El stock no se deduce del nombre: se sabe, porque alguien lo miro y
            # lo dijo al meterlo. Si la foto esta en disco pero no en el JSON, se
            # canta como sin catalogar en vez de inventarle un sector.
            m = st.get(rel.split("/", 1)[1])
            if m is None:
                filas.append((rel, "desconocido", "otro",
                              "stock sin registrar en stock.json"))
            else:
                filas.append((rel, m["sector"], m["tipo"], m["desc"]))
            continue
        pref, meta = _cliente(rel)
        if meta is None:
            filas.append((rel, "desconocido", _tipo(rel), "sin catalogar"))
        else:
            filas.append((rel, meta[0], _tipo(rel), meta[1]))
    return filas


def sectores():
    return sorted({s for _, s, _, _ in catalogo()})


def buscar(sector=None, tipo=None):
    """Rutas relativas (las que come `T.img`) que cumplen sector y/o tipo."""
    return [r for r, s, t, _ in catalogo()
            if (sector is None or s == sector) and (tipo is None or t == tipo)]


# La verdad incomoda del catalogo, y la razon de que exista este modulo: la parte
# PROPIA de la biblioteca no tiene fotografia de producto de ningun sector. Ni
# chocolate, ni un obrador, ni un escaparate. Hay webs de clientes dentro de un
# portatil. Contar cuantas imagenes "son del sector" y darlo por cubierto es el
# error que provoco que una propuesta de chocolate saliera con una portada de
# pulseras.
#
# Lo unico que rompe eso es el STOCK (`brand/assets/img/stock/`): fotografia de
# verdad, bajada a mano y catalogada una a una. Por eso la advertencia lo CONSULTA
# antes de hablar, en vez de negarlo con una constante: en cuanto metes fotos de
# chocolate, decir que no las hay pasa a ser mentira.


def fotos_de_producto(sector):
    """Las fotos de stock de un sector: fotografia real, no mockups de web."""
    return sorted(rel for rel, s, _, _ in catalogo()
                  if rel.startswith("stock/") and s == sector)


def advertencia(sector, minimo=3):
    """Que decirle al usuario sobre las imagenes de este sector. SIEMPRE devuelve
    texto: incluso con stock, sigue siendo fotografia generica y no su negocio."""
    reales = fotos_de_producto(sector)
    mockups = [r for r in buscar(sector=sector) if not r.startswith("stock/")]
    neutras = len(buscar(tipo="portatil")) + len(buscar(tipo="movil"))
    if reales:
        return (
            "Del sector '%s' hay %d foto(s) de STOCK (fotografia real, elegida a "
            "mano) y %d mockup(s) de web. Las de stock hablan del negocio; los "
            "mockups, de la web que le haremos. Aun asi el stock es generico por "
            "definicion: si el cliente aporta fotos SUYAS, el deck sube otro "
            "escalon." % (sector, len(reales), len(mockups)))
    if len(mockups) >= minimo:
        return (
            "Del sector '%s' hay %d imagenes, pero son MOCKUPS de la web de otro "
            "cliente dentro de un portatil o un movil, no fotografia del "
            "producto. Sirven para hablar de la web; no para ensenar el negocio. "
            "Si el cliente aporta fotos suyas, el deck cambia de nivel. Y se "
            "pueden bajar fotos a mano al buzon `stock-entrada/` y procesarlas "
            "con `python scripts/add_stock.py`." % (sector, len(mockups)))
    return (
        "No hay practicamente nada del sector '%s': %d imagen(es), y son mockups "
        "de web. Lo demas son webs de otros sectores (%d planos de portatil y "
        "movil) y fotos de la oficina: neutros, pero no hablan de este negocio. "
        "Conviene pedir fotos al cliente, o bajar stock a mano al buzon "
        "`stock-entrada/` y procesarlo con `python scripts/add_stock.py`."
        % (sector, len(mockups), neutras))


def _main(argv):
    if "--sector" in argv:
        s = argv[argv.index("--sector") + 1]
        for r in buscar(sector=s):
            print(r)
        print("\n" + advertencia(s))
        return 0
    porsector = {}
    for rel, s, t, _ in catalogo():
        porsector.setdefault(s, []).append((rel, t))
    for s in sorted(porsector):
        print("%-14s %d imagenes" % (s, len(porsector[s])))
    print("\n%d imagenes en %d sectores." % (len(catalogo()), len(porsector)))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
