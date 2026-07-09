"""PLANTILLA - Deck interno / corporativo.

Util para onboarding, resultados de equipo, formacion o reuniones internas.
Sustituye los textos de ejemplo. Genera con: python build/build.py interna
"""

import lib.slides as s

OUTFILE = "NaranjaTec-Interna-Corporativa.pptx"
TITULO = "NaranjaTec - Uso interno"


def build(prs):
    p = [0]

    def n():
        p[0] += 1
        return p[0]

    s.add_cover(
        prs,
        title="[Titulo de la reunion / tema]",
        subtitle="[Fecha - Equipo - Objetivo de la sesion]",
        eyebrow="Interno",
    )

    s.add_bullets(
        prs,
        "Agenda",
        [
            ("1. [Punto 1]", "[Detalle]"),
            ("2. [Punto 2]", "[Detalle]"),
            ("3. [Punto 3]", "[Detalle]"),
            ("4. [Punto 4]", "[Detalle]"),
        ],
        page=n(),
    )

    s.add_stats(
        prs,
        [
            {"value": "[dato]", "label": "[KPI 1]"},
            {"value": "[dato]", "label": "[KPI 2]"},
            {"value": "[dato]", "label": "[KPI 3]"},
        ],
        title="Resultados del periodo",
        page=n(),
    )

    s.add_two_column(
        prs,
        "Lo que va bien / lo que mejoramos",
        left={"heading": "Va bien", "items": ["[Logro 1]", "[Logro 2]", "[Logro 3]"]},
        right={"heading": "A mejorar", "items": ["[Reto 1]", "[Reto 2]", "[Reto 3]"]},
        page=n(),
    )

    s.add_section(prs, "Proximos pasos", number="")

    s.add_bullets(
        prs,
        "Acciones y responsables",
        [
            ("[Accion 1]", "Responsable: [nombre] - Fecha: [fecha]"),
            ("[Accion 2]", "Responsable: [nombre] - Fecha: [fecha]"),
            ("[Accion 3]", "Responsable: [nombre] - Fecha: [fecha]"),
        ],
        page=n(),
    )

    s.add_cta(
        prs,
        headline="Gracias",
        subtext="[Cierre o mensaje al equipo]",
        contact_lines=["[Contacto interno / siguiente reunion]"],
    )
    return prs
