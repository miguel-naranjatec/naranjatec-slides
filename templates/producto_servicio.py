"""PLANTILLA - Deck de producto / servicio.

Copia este guion y sustituye los textos de ejemplo por el servicio concreto que
quieras presentar (p.ej. Hosting Linux, Tiendas online, Private Cloud...).
Genera con:  python build/build.py producto
"""

import lib.slides as s

OUTFILE = "NaranjaTec-Producto-Servicio.pptx"
TITULO = "NaranjaTec - Producto / Servicio"


def build(prs):
    p = [0]

    def n():
        p[0] += 1
        return p[0]

    s.add_cover(
        prs,
        title="[Nombre del servicio]",
        subtitle="[Una frase que resuma el beneficio principal para el cliente]",
        eyebrow="NaranjaTec",
    )

    s.add_bullets(
        prs,
        "Que es y para quien",
        [
            ("[Que es]", "[Descripcion en una linea]"),
            ("[Para quien]", "[Perfil de cliente ideal]"),
            ("[Que problema resuelve]", "[El dolor que elimina]"),
        ],
        page=n(),
    )

    s.add_two_column(
        prs,
        "Antes y despues",
        left={"heading": "Sin este servicio", "items": ["[Problema 1]", "[Problema 2]", "[Problema 3]"]},
        right={"heading": "Con NaranjaTec", "items": ["[Beneficio 1]", "[Beneficio 2]", "[Beneficio 3]"]},
        page=n(),
    )

    s.add_service_grid(
        prs,
        "Caracteristicas principales",
        [
            {"title": "[Caracteristica 1]", "desc": "[Detalle]"},
            {"title": "[Caracteristica 2]", "desc": "[Detalle]"},
            {"title": "[Caracteristica 3]", "desc": "[Detalle]"},
            {"title": "[Caracteristica 4]", "desc": "[Detalle]"},
            {"title": "[Caracteristica 5]", "desc": "[Detalle]"},
            {"title": "[Caracteristica 6]", "desc": "[Detalle]"},
        ],
        page=n(),
    )

    s.add_stats(
        prs,
        [
            {"value": "[dato]", "label": "[metrica clave]"},
            {"value": "[dato]", "label": "[metrica clave]"},
            {"value": "[dato]", "label": "[metrica clave]"},
        ],
        title="En cifras",
        page=n(),
    )

    s.add_cta(
        prs,
        headline="Empieza hoy con [servicio]",
        subtext="[Oferta o llamada a la accion]",
        contact_lines=["Web: www.naranjatec.com", "Email: [correo]", "Telefono: [telefono]"],
    )
    return prs
