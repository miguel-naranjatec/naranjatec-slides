"""PLANTILLA - Deck institucional / de marca.

Presentacion general de quien es NaranjaTec: mision, valores, portfolio.
Sustituye los textos de ejemplo. Genera con: python build/build.py institucional
"""

import lib.slides as s

OUTFILE = "NaranjaTec-Institucional-Marca.pptx"
TITULO = "NaranjaTec - Institucional"


def build(prs):
    p = [0]

    def n():
        p[0] += 1
        return p[0]

    s.add_cover(
        prs,
        title="Quienes somos",
        subtitle="Creamos, cuidamos y optimizamos los activos online de las PYMEs.",
        eyebrow="NaranjaTec",
    )

    s.add_bullets(
        prs,
        "Nuestra historia",
        [
            ("+22 anos", "[Breve historia y origen de NaranjaTec]"),
            ("Nuestra mision", "Acompanar a las PYMEs en su digitalizacion."),
            ("Nuestra vision", "[Donde queremos estar]"),
        ],
        page=n(),
    )

    s.add_service_grid(
        prs,
        "Nuestros valores",
        [
            {"title": "Cercania", "desc": "[Que significa para nosotros]"},
            {"title": "Compromiso", "desc": "[Que significa para nosotros]"},
            {"title": "Excelencia", "desc": "[Que significa para nosotros]"},
        ],
        page=n(),
    )

    s.add_section(prs, "Que hacemos", number="")

    s.add_service_grid(
        prs,
        "Areas de servicio",
        [
            {"title": "Hosting", "desc": "Infraestructura fiable y segura."},
            {"title": "Desarrollo", "desc": "Webs, e-commerce y apps."},
            {"title": "Soporte", "desc": "Mantenimiento y gestion continua."},
        ],
        page=n(),
    )

    s.add_bullets(
        prs,
        "Portfolio",
        [
            ("[Proyecto 1]", "[Sector - resultado]"),
            ("[Proyecto 2]", "[Sector - resultado]"),
            ("[Proyecto 3]", "[Sector - resultado]"),
        ],
        page=n(),
    )

    s.add_cta(
        prs,
        headline="Algo mas que informar, inspirar",
        subtext="Hablemos.",
        contact_lines=["Web: www.naranjatec.com", "Email: [correo]", "Telefono: [telefono]"],
    )
    return prs
