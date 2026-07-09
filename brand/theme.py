"""Identidad de marca de NaranjaTec.

Colores muestreados directamente del logo oficial (brand/assets/logo.png):
el logotipo usa amarillo dorado ("naranja") y azul ("tec"), con un naranja
de acento procedente del degradado del isotipo hexagonal.

Este modulo centraliza la paleta, la tipografia y las medidas para que todas
las presentaciones compartan la misma marca.
"""

from pathlib import Path

from pptx.dml.color import RGBColor
from pptx.util import Emu, Pt

# --- Paleta de marca (muestreada del logo) ---
AMARILLO = RGBColor(0xFF, 0xCD, 0x33)      # dorado del wordmark "naranja"
AZUL = RGBColor(0x10, 0x99, 0xED)          # azul del wordmark "tec"
NARANJA = RGBColor(0xFF, 0x9E, 0x2C)       # naranja de acento (degradado del isotipo)
AZUL_OSCURO = RGBColor(0x0B, 0x3D, 0x66)   # azul profundo para fondos de seccion
GRIS_TEXTO = RGBColor(0x2B, 0x2F, 0x36)    # texto principal
GRIS_SUAVE = RGBColor(0x6B, 0x72, 0x80)    # texto secundario / apoyos
GRIS_FONDO = RGBColor(0xF4, 0xF6, 0xF8)    # fondos suaves de tarjetas
GRIS_BORDE = RGBColor(0xE2, 0xE6, 0xEA)    # bordes sutiles
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

# Tintes suaves para bloques (estilo premium)
AMARILLO_TINT = RGBColor(0xFF, 0xF3, 0xD1)  # amarillo muy claro
AZUL_TINT = RGBColor(0xE7, 0xF2, 0xFD)      # azul muy claro

# Extremos claros para el degradado de los chips de icono
AZUL_CHIP = RGBColor(0x1B, 0x5C, 0x8F)      # azul marino mas claro (top-left)
AMARILLO_CLARO = RGBColor(0xFF, 0xDE, 0x6E)  # dorado claro (top-left)

# Fondo blanco calido (mas elegante que el blanco puro); las tarjetas blancas
# resaltan sutilmente sobre el.
BG = RGBColor(0xFA, 0xF9, 0xF6)

# --- Tipografia ---
# Se usan familias con el PESO en el nombre (p.ej. "Poppins SemiBold") para
# controlar el grosor con precision. La libreria ignora el flag de negrita cuando
# el nombre ya incluye un peso. Poppins (geometrica, redondeada) es afin al logo;
# Inter aporta un cuerpo muy legible.
# FONT_TITLE se usa SOLO en los titulos grandes (portada, seccion, titulos de
# slide). Cambiar esta constante alterna entre un look editorial (serif elegante)
# y uno tech (sans). Georgia es una serif elegante y disponible en todo Windows.
FONT_TITLE = "Google Sans"           # titulos grandes (sans; el peso via bold=True)
FONT_TITLE_EMPH = "Playfair Display"  # palabras marcadas con *enfasis* en un titulo
                                      # -> serif editorial en cursiva, contraste sans/serif
FONT_HEAD = "Google Sans Medium"     # subtitulos / titulos de tarjeta (peso 500)
FONT_HEAD_MED = "Google Sans Medium" # apoyos
FONT_NUM = "Google Sans"             # cifras grandes (mismo sans que titulos, con peso)
FONT_BODY = "Instrument Sans"        # cuerpo (regular)
FONT_BODY_MED = "Instrument Sans Medium"  # cuerpo con algo mas de peso
FONT_MONO = "Geist Mono"             # botones/pills y etiquetas con estilo mono
# Iconos monolinea multiplataforma: Material Symbols Outlined (Google, Apache 2.0),
# congelada a peso 300 (trazo mas fino que el 400 por defecto). El .ttf estatico
# esta bundled en brand/assets/fonts/Material_Icons/ y se regenera con
# scripts/make_icon_font.py. Sustituye a "Segoe Fluent Icons" (solo Windows).
#
# El nombre de familia lleva el peso a proposito: si se llamase "Material Symbols
# Outlined" a secas y alguien tuviera instalada la fuente oficial de Google,
# PowerPoint usaria esa (peso 400) en silencio. Asi, si falta, salen cajas.
FONT_ICON = "Material Symbols Outlined 300"

# Glyphs de icono (codepoints PUA de Material Symbols). Centralizados para
# reutilizarlos desde el contenido: T.ICON["cloud"], etc. Ver el fichero
# .codepoints junto al .ttf para el mapa nombre->codigo completo. OJO: los
# codepoints de Material Symbols NO coinciden con los de Material Icons; el mapa
# nombre-semantico -> nombre-de-Google vive en scripts/make_icon_font.py.
ICON = {
    "globe": "\uE80B", "cloud": "\uF15C", "server": "\uE875", "rack": "\uEB2F",
    "network": "\uE9F4", "mail": "\uE159", "lock": "\uE899", "cert": "\uEF76",
    "shield": "\uE9E0", "wrench": "\uF8CD", "gear": "\uE8B8", "monitor": "\uE30C",
    "cart": "\uE8CC", "mobile": "\uE7BA", "code": "\uE86F", "person": "\uF0D3",
    "people": "\uF233", "storage": "\uE1DB", "bolt": "\uEA0B", "sync": "\uE627",
    "pulse": "\uEAA2", "check": "\uF0BE", "phone": "\uF0D4",
    "quote": "\uE244", "star": "\uF09A", "idea": "\uE90F",
    "arrow": "\uE5C8", "location": "\uF1DB", "tick": "\uE668",
}

# Palabras clave de peso que, si aparecen en el nombre de la fuente, hacen que la
# libreria NO aplique negrita sintetica encima (evita dobles grosores).
_WEIGHT_TOKENS = ("Thin", "ExtraLight", "Light", "Medium", "SemiBold",
                  "ExtraBold", "Black", "Bold")

# --- Medidas del lienzo (16:9 panoramico) ---
SLIDE_W = Emu(12192000)   # 13.333 pulgadas
SLIDE_H = Emu(6858000)    # 7.5 pulgadas

# --- Recursos ---
_ASSETS = Path(__file__).resolve().parent / "assets"
LOGO_PATH = _ASSETS / "logo.png"
LOGO_WHITE_PATH = _ASSETS / "logo-white.png"   # version monocroma blanca (fondos oscuros)
IMG_DIR = _ASSETS / "img"   # biblioteca de imagenes del proyecto (portable)


def img(name):
    """Devuelve la ruta (str) a una imagen de la biblioteca del proyecto.

    Ej.: theme.img("naranjatec-web.jpg") o theme.img("avatars/avatar-canon.jpg").
    Lanza FileNotFoundError si no existe, para detectar erratas al construir.
    """
    p = IMG_DIR / name
    if not p.exists():
        raise FileNotFoundError("Imagen no encontrada en la biblioteca: %s" % p)
    return str(p)

# --- Eslogan corporativo ---
ESLOGAN = "Algo mas que informar, inspirar"

# Escala tipografica de referencia (en puntos)
SIZE_COVER_TITLE = Pt(46)
SIZE_SECTION = Pt(40)
SIZE_TITLE = Pt(30)
SIZE_SUBTITLE = Pt(18)
SIZE_BODY = Pt(16)
SIZE_SMALL = Pt(12)
SIZE_STAT = Pt(48)
