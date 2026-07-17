# -*- coding: utf-8 -*-
"""Diapositivas FIJAS: contenido de NaranjaTec, no del cliente.

Un deck de propuesta mezcla dos cosas. Lo que sale del documento del cliente (su
problema, su alcance, su presupuesto) y lo que ponemos nosotros siempre igual:
como trabajamos, quienes somos, que pasa despues de firmar. Lo segundo vive aqui,
escrito una vez, y se activa deck a deck.

El skill `propuesta-a-deck` lee este registro y PREGUNTA cuales incluir antes de
generar nada. Anadir una fija nueva es anadir una entrada a `FIJAS`: ni el skill
ni los decks existentes se tocan.

    python content/fijas.py --list      # ver el registro

Uso desde un deck:

    import content.fijas as F
    F.proximos_pasos(prs, page=n(), section="Siguiente")

El texto lleva acentos reales (es un entregable); el codigo y los comentarios,
ASCII puro.
"""

import sys
from pathlib import Path

if __name__ == "__main__":                      # ejecutable suelto: python content/fijas.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import brand.theme as T
import content.testimonios as TT
import lib.slides as s


# --- Testimonio ------------------------------------------------------------
# La fija elige la voz que sostiene el argumento del deck. Sin pistas, habla
# Importaco: profesionalidad, plazos, incidencias y confianza sirven en casi
# cualquier propuesta.

TESTIMONIO_DEFECTO = "importaco"


def testimonio(prs, page=None, section="", slug=None, temas=(), corto=True):
    """Un testimonio real de `content/testimonios.py`. Pasa `temas` (los del
    argumento del deck: "hosting", "plazos", "autonomia"...) y elige el cliente
    que mejor los defiende; o fuerza uno con `slug`."""
    if slug is None:
        candidatos = TT.por_tema(*temas) if temas else []
        slug = candidatos[0] if candidatos else TESTIMONIO_DEFECTO
    return TT.quote(prs, slug, page=page, section=section, corto=corto)


# --- Proximos pasos --------------------------------------------------------
# Los cinco pasos del proceso de NaranjaTec, de la firma al lanzamiento.
# `add_next_steps` admite de 3 a 5: anadir uno obliga a quitar otro.

PASOS = [
    ("Aprobación del presupuesto",
     "Das el visto bueno a la propuesta y reservamos las fechas.",
     T.ICON["check"]),
    ("Aportación de materiales",
     "Nos pasas textos, logotipos e imágenes.",
     T.ICON["storage"]),
    ("Diseño",
     "Definimos estructura y aspecto, y lo validas antes de programar.",
     T.ICON["idea"]),
    ("Programación",
     "Construimos la web a medida y la probamos.",
     T.ICON["code"]),
    ("Lanzamiento",
     "Publicamos, formamos a tu equipo y quedamos de soporte.",
     T.ICON["bolt"]),
]


def proximos_pasos(prs, page=None, section="", pasos=None,
                   title="Próximos *pasos*",
                   subtitle="De la firma al lanzamiento"):
    """Que ocurre despues de decir que si. `pasos` sustituye a los de serie:
    la descripcion se puede adaptar al proyecto, y cabe anadir una fase (una
    migracion, una formacion) siempre que se quite otra (el maximo son 5)."""
    return s.add_next_steps(prs, title, pasos or PASOS, subtitle=subtitle,
                            page=page, section=section)


# --- Nuestra mision --------------------------------------------------------
# Aqui vive el discurso comercial de la casa: este es el copy bueno, el que se
# reutiliza en las propuestas. `add_mission` pinta 4 features como maximo.

MISION = [
    {"icon": T.ICON["people"], "head": "Un único interlocutor",
     "text": "Hosting, desarrollo y soporte bajo un mismo techo. Sin "
             "proveedores dispersos ni facturas sueltas."},
    {"icon": T.ICON["shield"], "head": "Más de 22 años",
     "text": "Cuidando la presencia online de PYMEs, sobre una base técnica "
             "sólida y fiable."},
    {"icon": T.ICON["person"], "head": "Servicio cercano",
     "text": "Personas que entienden tu negocio. Ni call centers ni "
             "respuestas automáticas."},
    {"icon": T.ICON["check"], "head": "Sin humo ni sobrecostes",
     "text": "Diseñamos la solución adecuada y te explicamos por qué es esa."},
]

MISION_CAPTION = ("Acompañamos a las PYMEs en su digitalización",
                  "Entendemos tu negocio, tus objetivos y tu punto de partida.")


def mision(prs, page=None, section="", features=None, image=None,
           title="Nuestra *misión*", caption=None):
    """Quienes somos. `features` se adapta a lo que se ofrece en cada deck: en
    una propuesta de e-commerce pesa mas la tienda que el hosting. `title`,
    `features` y `caption` son los puntos por donde se TRADUCE la fija cuando el
    deck no va en espanol."""
    cap = caption or MISION_CAPTION
    return s.add_mission(prs, title, features or MISION,
                         image or T.img("oficina/naranjatec_4273.jpg"),
                         cap[0], cap[1], page=page, section=section)


# --- Complementos: hosting, soporte y llave en mano ------------------------
# Van en casi todas las propuestas. Los importes son los de casa; se sobreescriben
# pasando otras listas. El equivalente anual NO se escribe aqui: lo calcula
# `add_addons` multiplicando por 12, para que no pueda contradecir al mensual.

LLAVE_EN_MANO = {
    "name": "Llave en mano",
    "desc": "Entrega de la web lista para publicar: contenidos, configuración y "
            "puesta en marcha por NaranjaTec.",
    "price": 750,
    "icon": T.ICON["lock"],
}

RECURRENTES = [
    {"name": "Hosting · WordPress optimizado",
     "desc": "Alojamiento gestionado y optimizado para WordPress.",
     "price": 35, "icon": T.ICON["server"]},
    {"name": "Soporte y mantenimiento",
     "desc": "Actualizaciones, copias de seguridad y soporte continuo del sitio.",
     "price": 35, "icon": T.ICON["wrench"]},
]

NOTA_COMPLEMENTOS = ("Opciones no incluidas en el total del presupuesto. "
                     "Todos los precios son sin IVA.")


def complementos(prs, page=None, section="", recurrentes=None, unicos=None,
                 title="Complementos a tu *medida*",
                 subtitle="Opciones y servicios", note=None):
    """Pagos unicos (llave en mano) a la izquierda y servicios recurrentes
    (hosting, soporte) a la derecha. `unicos=[]` quita la columna izquierda."""
    return s.add_addons(
        prs, title,
        recurrentes if recurrentes is not None else RECURRENTES,
        unicos=unicos if unicos is not None else [LLAVE_EN_MANO],
        subtitle=subtitle,
        note=note if note is not None else NOTA_COMPLEMENTOS,
        label_unico="Pago único",
        label_recurrente="Servicios recurrentes · Pago anual",
        anual_texto="Facturación anual (%s/año).",
        page=page, section=section)


# --- Contacto --------------------------------------------------------------
# El cierre de un deck necesita a quien escribir. Se PREGUNTA a que contacto va
# dirigido; si no se dice nada, estos son los de casa. Nunca se inventa uno.

EMAIL = "rick@naranjatec.com"
TELEFONO = "627 41 41 36"
WEB = "www.naranjatec.com"


def contacto_cta(email=None, telefono=None, web=None):
    """Para `add_cta`, que espera 2-tuplas (icono, valor)."""
    return [
        (T.ICON["mail"], email or EMAIL),
        (T.ICON["phone"], telefono or TELEFONO),
        (T.ICON["globe"], web or WEB),
    ]


def contacto_thanks(email=None, telefono=None, web=None):
    """Para `add_thanks`, que espera 3-tuplas (icono, etiqueta, valor)."""
    return [
        (T.ICON["mail"], "Email", email or EMAIL),
        (T.ICON["phone"], "Teléfono", telefono or TELEFONO),
        (T.ICON["globe"], "Web", web or WEB),
    ]


# --- El registro -----------------------------------------------------------
# `acto` dice en que punto del arco (problema -> solucion -> propuesta ->
# presupuesto -> proximos pasos) encaja la fija. `defecto` es si viene marcada
# en la pregunta que hace el skill.

FIJAS = [
    {
        "slug": "mision",
        "nombre": "Nuestra mision",
        "desc": "Quienes somos: un interlocutor, 22 anos, servicio cercano.",
        "acto": "solucion",
        "defecto": True,
        "fn": mision,
    },
    {
        "slug": "testimonio",
        "nombre": "Testimonio de cliente",
        "desc": "Una voz real que sostiene el argumento (elige por temas).",
        "acto": "propuesta",
        "defecto": True,
        "fn": testimonio,
    },
    {
        "slug": "complementos",
        "nombre": "Complementos (hosting, soporte, llave en mano)",
        "desc": "Pago unico y servicios recurrentes, fuera del presupuesto.",
        "acto": "presupuesto",
        "defecto": True,
        "fn": complementos,
    },
    {
        "slug": "proximos-pasos",
        "nombre": "Proximos pasos",
        "desc": "De la aprobacion del presupuesto al lanzamiento.",
        "acto": "proximos pasos",
        "defecto": True,
        "fn": proximos_pasos,
    },
]


def listar():
    # Los metadatos del registro van en ASCII: se leen en una consola, no en el
    # deck. El copy con acentos es el de PASOS y MISION.
    for f in FIJAS:
        print("%-16s %s%s" % (f["slug"], f["nombre"],
                              "  [por defecto]" if f["defecto"] else ""))
        print("%-16s   %s" % ("", f["desc"]))
        print("%-16s   acto: %s" % ("", f["acto"]))
    print("\n%d diapositivas fijas." % len(FIJAS))
    return 0


if __name__ == "__main__":
    # No hay mas modos: este modulo solo se ejecuta para mirar el registro.
    raise SystemExit(listar())
