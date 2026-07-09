# -*- coding: utf-8 -*-
"""Deck comercial real: propuesta de nueva web para Nereidas Real Estate.

Basado en el documento de propuesta (proyecto Nereidas). Usa los layouts de
lib/slides.py con la marca NaranjaTec. Las imagenes son de la biblioteca del
proyecto a modo de PLACEHOLDER (mockups de web / ambientes): conviene sustituir
por fotografia real de propiedades de Nereidas y capturas de la nueva web.

Genera con: python build/build.py nereidas

Nota: el texto de contenido lleva acentos y ene (UTF-8, sin BOM) por ser un
entregable para cliente; el codigo y los comentarios se mantienen en ASCII.
"""

import brand.theme as T
import lib.slides as s

OUTFILE = "Nereidas-Propuesta-Web.pptx"
TITULO = "Nereidas Real Estate - Propuesta de nueva web"


def build(prs):
    p = [0]

    def n():
        p[0] += 1
        return p[0]

    # 1) PORTADA
    s.add_cover(
        prs,
        title="Una web a la altura de tus *propiedades*",
        subtitle="Propuesta de nueva web a medida para Nereidas Real Estate.",
        eyebrow="NaranjaTec - Propuesta",
        image=T.img("valenciapremium-imac.jpg"),
    )

    # 2) INDICE
    s.add_index(
        prs,
        "Qué veremos",
        [
            ("El problema", "Una web que no convierte"),
            ("La solución", "Un desarrollo a medida"),
            ("Dónde ganamos", "Se tapa cada fuga"),
            ("El proyecto", "Alcance e inversión"),
        ],
        page=n(),
    )

    # 3) SECCION 01 - EL PROBLEMA
    s.add_section(prs, "El *problema*", number="01",
                  image=T.img("ecco-night.jpg"))

    # 4) DECLARACION: el problema en una frase
    s.add_statement(
        prs,
        "La web recibe visitas, pero no las convierte. El visitante entra, "
        "mira propiedades y se va *sin dejar rastro*.",
        image=T.img("sinrodeos-hand.jpg"),
        author="Nereidas Real Estate",
        page=n(),
    )

    # 5) POR QUE LA WEB ACTUAL NO VENDE (rejilla)
    s.add_service_grid(
        prs,
        "Por qué la web actual no vende",
        [
            {"title": "Indistinguible", "icon": T.ICON["people"],
             "desc": "El mismo plugin y feed que decenas de agencias de la "
                     "Costa del Sol."},
            {"title": "Poco profesional", "icon": T.ICON["star"],
             "desc": "Fotografía descuidada e interfaz de plantilla genérica."},
            {"title": "Lenta en móvil", "icon": T.ICON["bolt"],
             "desc": "45 sobre 100 en Google, justo donde llega el tráfico."},
            {"title": "Sin llamadas a la acción", "icon": T.ICON["arrow"],
             "desc": "Solo un 'Contact Us' en el menú; fichas con un pasivo "
                     "'Read More'."},
            {"title": "Formulario genérico", "icon": T.ICON["mail"],
             "desc": "No sabe qué propiedad mirabas; hay que reescribir la "
                     "referencia."},
            {"title": "Testimonios enterrados", "icon": T.ICON["quote"],
             "desc": "El activo de confianza, lejos de donde se decide la "
                     "compra."},
            {"title": "Sin SEO", "icon": T.ICON["globe"],
             "desc": "Sin títulos ni descripciones pensados para atraer el "
                     "clic."},
        ],
        subtitle="Los techos que pone la herramienta actual",
        page=n(),
        section="El problema",
    )

    # 6) SECCION 02 - LA SOLUCION
    s.add_section(prs, "La *solución*", number="02",
                  image=T.img("imporaco-reuniones.jpg"))

    # 7) LA DECISION: DESARROLLO A MEDIDA (texto + imagen + dato)
    s.add_image_feature(
        prs,
        "Un desarrollo nuevo, *a medida*",
        [
            "Una web nueva sobre WordPress, con bloques diseñados para esta "
            "marca. No una web más bonita: una web pensada de principio a fin "
            "para convertir.",
            "Integra directamente con Resales Online e importa las propiedades "
            "al propio WordPress: rápida, indexable y con control total del "
            "catálogo.",
        ],
        image=T.img("holanda-laptop.jpg"),
        stat=("90+", "objetivo de rendimiento"),
        side="right",
        subtitle="Cambiar de herramienta, no parchear",
        page=n(),
        section="La solución",
    )

    # 8) ANTES / DESPUES (dos columnas)
    s.add_two_column(
        prs,
        "De dónde partimos, a dónde llegamos",
        left={"heading": "Web actual", "icon": T.ICON["pulse"],
              "items": ["Indistinguible de la competencia",
                        "Lenta: 45 sobre 100 en móvil",
                        "Casi sin llamadas a la acción",
                        "Testimonios enterrados"]},
        right={"heading": "Web nueva", "icon": T.ICON["shield"],
               "items": ["Marca propia que se recuerda",
                         "Rápida: objetivo 90 o más",
                         "'Solicitar información' siempre visible",
                         "Prueba social donde se decide"]},
        subtitle="La web actual frente a la nueva",
        page=n(),
        section="La solución",
    )

    # 9) DECLARACION: el retorno de la inversion
    s.add_statement(
        prs,
        "Con el valor de *una sola comisión*, una única operación adicional "
        "amortiza el proyecto.",
        image=T.img("accompany-meeting.jpg"),
        author="La inversión con mejor retorno",
        page=n(),
    )

    # 10) DONDE SE TAPA CADA FUGA (proceso, recorrido del comprador)
    s.add_process(
        prs,
        "Dónde se tapa cada fuga",
        [
            ("De la búsqueda a la web",
             "Web rápida e indexable, con páginas de zona propias que "
             "posicionan mejor en Google."),
            ("De la home a la propiedad",
             "Buscador propio y escaparate de la cartera curada de Nereidas, "
             "separada del feed genérico."),
            ("De la propiedad al contacto",
             "Fichas claras y un 'Solicitar información' que abre un panel con "
             "la referencia ya cargada."),
            ("Del contacto a la confianza",
             "El trato personal de Karin y los testimonios reales, donde de "
             "verdad se decide la compra."),
        ],
        page=n(),
        section="Dónde ganamos",
    )

    # 11) EL VALOR DE CADA PARTE (rejilla)
    s.add_service_grid(
        prs,
        "El valor de cada parte",
        [
            {"title": "Bloques reutilizables", "icon": T.ICON["gear"],
             "desc": "Se maquetan una vez; creas y reorganizas páginas sin "
                     "depender de nadie."},
            {"title": "Resales Online", "icon": T.ICON["sync"],
             "desc": "Propiedades importadas y sincronizadas, con imágenes "
                     "optimizadas en local."},
            {"title": "Cartera propia", "icon": T.ICON["star"],
             "desc": "Los inmuebles de la agencia, destacados como la selección "
                     "exclusiva de Karin."},
            {"title": "Buscador y zonas", "icon": T.ICON["globe"],
             "desc": "Filtros a medida y páginas de zona con contenido único "
                     "que posicionan."},
            {"title": "Fichas que convierten", "icon": T.ICON["monitor"],
             "desc": "Cabecera elegante, características en iconos, galería "
                     "amplia y CTA a mano."},
            {"title": "Contacto sin fricción", "icon": T.ICON["bolt"],
             "desc": "Panel lateral con la referencia precargada, botón "
                     "flotante y WhatsApp directo."},
            {"title": "Confianza", "icon": T.ICON["people"],
             "desc": "Storytelling de Karin y testimonios con datos "
                     "estructurados para Google."},
            {"title": "Cuatro idiomas", "icon": T.ICON["location"],
             "desc": "Inglés, neerlandés, alemán y español, sin mezclas de "
                     "idiomas."},
        ],
        subtitle="Qué incluye la web nueva y por qué suma",
        page=n(),
        section="Dónde ganamos",
    )

    # 12) SECCION 03 - EL PROYECTO
    s.add_section(prs, "El *proyecto*", number="03",
                  image=T.img("ecco-office.jpg"))

    # 13) EL PROYECTO EN CIFRAS
    # El deck habla en euros: no se muestran horas en ningún sitio. Si aquí
    # apareciesen las 34,5h junto a los 5.175 € del desglose, bastaría dividir
    # para deducir la tarifa por hora.
    s.add_stats(
        prs,
        [
            {"value": "5.175 €", "label": "de inversión estimada"},
            {"value": "20", "label": "bloques reutilizables"},
            {"value": "4", "label": "idiomas listos"},
        ],
        title="El proyecto en cifras",
        subtitle="Alcance del desarrollo",
        page=n(),
        section="El proyecto",
    )

    # 14) DESGLOSE DEL PROYECTO
    # Las cinco partidas del documento de propuesta, convertidas de horas a
    # euros (150 €/hora). El deck habla en euros: las horas no se muestran.
    # El total lo suma add_pricing, asi que no puede desviarse de las filas.
    # OJO: add_pricing recibe el contador `n`, no `n()`.
    s.add_pricing(
        prs,
        "Desglose del *proyecto*",
        [
            ("Estructura y elementos comunes", 1200),
            ("Propiedades y contenido gestionable", 750),
            ("Integración con Resales Online", 900),
            ("Buscador de propiedades", 450),
            ("Bloques de contenido", 1875),
        ],
        note="Las ampliaciones opcionales (búsquedas guardadas y alertas, "
             "reseñas de Google) se presupuestan aparte.",
        subtitle="Lo que incluye el desarrollo, partida a partida",
        page=n,
        section="El proyecto",
    )

    # 15) AMPLIACIONES OPCIONALES
    # Las dos del documento de propuesta: +2,5h y +1h, a 150 €/hora.
    # Imagenes PLACEHOLDER: sustituir por capturas reales de la web nueva.
    s.add_extras(
        prs,
        "Ampliaciones *opcionales*",
        [
            {"price": 375, "name": "Búsquedas guardadas",
             "desc": "El comprador guarda su búsqueda y recibe por email las "
                     "propiedades nuevas que encajan.",
             "icon": T.ICON["mail"], "image": T.img("ecco-working.jpg")},
            {"price": 150, "name": "Reseñas de Google",
             "desc": "Las reseñas reales de la agencia, integradas en la web y "
                     "actualizadas solas.",
             "icon": T.ICON["star"], "image": T.img("accompany-meeting.jpg")},
        ],
        subtitle="Se contratan cuando quieras, sobre la web ya en marcha",
        page=n(),
        section="El proyecto",
    )

    # 16) CIERRE / CTA
    s.add_cta(
        prs,
        headline="Demos el *siguiente paso*",
        subtext="Una web a la altura de Nereidas Real Estate.",
        contact=[
            (T.ICON["globe"], "www.naranjatec.com"),
            (T.ICON["mail"], "info@naranjatec.com"),
            (T.ICON["phone"], "+34 000 000 000"),
        ],
        image=T.img("oficina/naranjatec_4273.jpg"),
    )
    return prs
