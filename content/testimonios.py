# -*- coding: utf-8 -*-
"""Testimonios reales de clientes de NaranjaTec.

Un testimonio no se elige al azar: se elige el que REFUERZA el argumento del deck.
Por eso cada uno lleva `temas`. En una propuesta de hosting critico habla Pig&Hen;
en una donde el cliente teme depender del proveedor, habla Canon; si lo que pesa
son los plazos, Importaco.

    python content/testimonios.py --list        # ver el catalogo y sus temas

Uso desde un deck:

    import content.testimonios as TT
    TT.quote(prs, "importaco", page=n(), section="Confianza")
    TT.por_tema("hosting")                      # -> ["pig-hen", "selva-digital"]

Sobre la literalidad: las citas van palabra por palabra, con su puntuacion, como
las escribieron sus autores. Solo se normalizan tres cosas: el nombre de la marca
("NaranjaTec"; en el original de Valencia Guias ponia "Naracjatec"), las tildes
omitidas al teclear, y los cargos, a los que se les quita la empresa porque ya va
al lado. Ni una palabra mas ni una menos.

Cuando una cita es demasiado larga para `add_quote`, se guarda tambien un
`extracto`, que es un subconjunto LITERAL del original con elipsis: nunca se pone
en boca de un cliente algo que no dijo. Hay un test que lo comprueba.

El texto lleva acentos reales (es un entregable); el codigo y los comentarios,
ASCII puro.
"""

import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import brand.theme as T
import lib.slides as s


# `avatar` e `image` son rutas dentro de brand/assets/img/, o None si no tenemos.
# `extracto` es None cuando la cita entera ya cabe holgada en la diapositiva.

TESTIMONIOS = [
    {
        "slug": "pig-hen",
        "cliente": "Pig & Hen",
        "autor": "Thomas van der Kallen",
        "cargo": "Co-propietario",
        "temas": ("hosting", "soporte", "ecommerce", "criticidad"),
        "avatar": "avatars/avatar-pighen.jpg",
        "image": "pighen-mac.jpg",
        "texto": "NaranjaTec provee Pig&Hen de servicios esenciales de hospedaje "
                 "y web que son críticos para nuestro negocio online. Es un "
                 "equipo de profesionales y apasionados que siempre están al "
                 "quite para ofrecernos las mejores soluciones y servicio.",
        "extracto": None,
    },
    {
        "slug": "canon",
        "cliente": "Canon",
        "autor": "Leon Bouma",
        "cargo": "CEO y fundador",
        "temas": ("autonomia", "precio", "diseno", "proceso"),
        "avatar": "avatars/avatar-canon.jpg",
        "image": "canonbcn-imac.jpg",
        "texto": "Buscábamos una web ágil de gestionar que luego podíamos "
                 "mantener actualizada de forma independiente. Estamos muy "
                 "satisfechos sobre precio/calidad, diseño y el proceso. "
                 "¡Empresa 100% recomendable!",
        "extracto": "Buscábamos una web ágil de gestionar que luego podíamos "
                    "mantener actualizada de forma independiente. [...] "
                    "¡Empresa 100% recomendable!",
    },
    {
        "slug": "abordo",
        "cliente": "Abordo",
        "autor": "Antonio Herrero",
        "cargo": "Marketing manager",
        "temas": ("escucha", "catalogo", "ecommerce", "mantenimiento"),
        "avatar": None,
        "image": "abordo-web.jpg",
        "texto": "Su equipo se ha esforzado en cada momento para entender lo que "
                 "queríamos ofreciéndonos soluciones prácticas a nuestras "
                 "peticiones. El resultado ha sido una web atractiva y funcional "
                 "y un catálogo de productos online de fácil actualización y "
                 "mantenimiento.",
        "extracto": None,
    },
    {
        "slug": "selva-digital",
        "cliente": "Selva Digital",
        "autor": "Noah Winkelman",
        "cargo": "CEO y fundador",
        "temas": ("hosting", "soporte", "calidad", "internacional"),
        "avatar": None,
        "image": "accompany-website.jpg",
        "texto": "Selva Digital tiene clientes en toda Europa y, por lo tanto, es "
                 "importante tener un proveedor de alta calidad para los "
                 "servicios de alojamiento. ¡Qué suerte que hemos encontrado este "
                 "proveedor en NaranjaTec! Con un equipo de soporte incomparable "
                 "y servicios de alta calidad, es un placer trabajar con "
                 "NaranjaTec.",
        "extracto": "Es importante tener un proveedor de alta calidad para los "
                    "servicios de alojamiento. [...] Con un equipo de soporte "
                    "incomparable y servicios de alta calidad, es un placer "
                    "trabajar con NaranjaTec.",
    },
    {
        "slug": "sin-rodeos",
        "cliente": "Sin Rodeos",
        "autor": "Ronald Verstappen",
        "cargo": "Fundador",
        "temas": ("proceso", "conocimiento", "idiomas", "comunicacion"),
        "avatar": "avatars/avatar-sinrodeos.jpg",
        "image": "sinrodeos-desktop-nl.jpg",
        "texto": "Ningún proceso ha sido tan impecable como con NaranjaTec. Este "
                 "equipo tiene el conocimiento y las habilidades en casa, y "
                 "permite conectarse y comunicarse fácilmente, ¡incluso en varios "
                 "idiomas!",
        "extracto": None,
    },
    {
        "slug": "valencia-guias",
        "cliente": "Valencia Guías",
        "autor": "Ana Merelo",
        "cargo": "Socio-fundador",
        "temas": ("cercania", "plazos", "compromiso", "disponibilidad"),
        "avatar": None,
        "image": "accompany-meeting.jpg",
        "texto": "Hemos elegido NaranjaTec por la cercanía y disponibilidad, "
                 "escuchan, se adaptan y hacen de lo digital algo muy tangible "
                 "gracias a esa manera fácil de hacer las cosas. Es un proveedor "
                 "que cumple plazos y compromisos. Sin duda para nosotros muy "
                 "recomendable para cualquier empresa.",
        "extracto": "Hemos elegido NaranjaTec por la cercanía y disponibilidad, "
                    "escuchan, se adaptan y hacen de lo digital algo muy "
                    "tangible [...] Es un proveedor que cumple plazos y "
                    "compromisos.",
    },
    {
        "slug": "bendorfy",
        "cliente": "Bendorfy",
        "autor": "Francisco J. C. Aguilar",
        "cargo": "Cofundador",
        "temas": ("estabilidad", "robustez", "profesionalidad"),
        "avatar": None,
        "image": "ecco-office.jpg",
        "texto": "Grandes profesionales, y grandes aliados para dar estabilidad "
                 "con robustez a nuestro negocio.",
        "extracto": None,
    },
    {
        "slug": "importaco",
        "cliente": "Importaco",
        "autor": "Rosa Medina",
        "cargo": "Técnico de relaciones externas y RSC",
        "temas": ("plazos", "incidencias", "profesionalidad", "confianza"),
        "avatar": None,
        "image": "importaco-macbookpro.jpg",
        "texto": "Hemos trabajado con NaranjaTec en varios proyectos y la "
                 "experiencia ha sido muy positiva. Destacan por su gran "
                 "profesionalidad y por el cumplimiento riguroso de los plazos, "
                 "algo clave en este tipo de trabajos. Además, valoramos "
                 "especialmente su rapidez en la resolución de incidencias y su "
                 "disposición constante a ayudar y aportar soluciones, lo que "
                 "facilita mucho el día a día y genera mucha confianza. Sin duda, "
                 "un equipo fiable y comprometido. Muy recomendables.",
        "extracto": "Destacan por su gran profesionalidad y por el cumplimiento "
                    "riguroso de los plazos [...] valoramos especialmente su "
                    "rapidez en la resolución de incidencias y su disposición "
                    "constante a ayudar y aportar soluciones [...] Sin duda, un "
                    "equipo fiable y comprometido.",
    },
]

POR_SLUG = {t["slug"]: t for t in TESTIMONIOS}


def por_tema(*temas):
    """Slugs de los testimonios que hablan de alguno de esos temas, del que mas
    temas comparte al que menos. Sirve para elegir el que sostiene el argumento
    del deck, no el primero de la lista.

    A igualdad de afinidad manda el orden del catalogo, no el alfabetico: si no,
    `selva-digital` adelantaria a `pig-hen` por la letra."""
    pedidos = set(temas)
    con_peso = [(len(pedidos & set(t["temas"])), i, t["slug"])
                for i, t in enumerate(TESTIMONIOS)]
    con_peso.sort(key=lambda x: (-x[0], x[1]))
    return [slug for peso, _, slug in con_peso if peso]


def texto(slug, corto=True):
    """La cita. `corto` usa el extracto literal cuando existe."""
    t = POR_SLUG[slug]
    return t["extracto"] if (corto and t["extracto"]) else t["texto"]


def quote(prs, slug, page=None, section="", corto=True, image=None, stars=5):
    """Pinta el testimonio con `add_quote`. La foto de fondo y el avatar salen
    del propio testimonio; `image` los sobrescribe."""
    t = POR_SLUG[slug]
    img = image or (T.img(t["image"]) if t["image"] else None)
    return s.add_quote(
        prs, texto(slug, corto), author=t["autor"],
        role="%s - %s" % (t["cargo"], t["cliente"]),
        avatar=T.img(t["avatar"]) if t["avatar"] else None,
        stars=stars, image=img, page=page, section=section)


def listar():
    for t in TESTIMONIOS:
        marca = "corto+integro" if t["extracto"] else "integro"
        print("%-16s %-16s %s" % (t["slug"], t["cliente"], marca))
        print("%-16s   temas: %s" % ("", ", ".join(t["temas"])))
    print("\n%d testimonios." % len(TESTIMONIOS))
    return 0


if __name__ == "__main__":
    raise SystemExit(listar())
