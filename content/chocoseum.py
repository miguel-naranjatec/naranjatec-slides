# -*- coding: utf-8 -*-
"""Deck comercial: propuesta de nueva tienda online para Chocoseum.

Basado en el documento de propuesta (presentacion.md del proyecto Chocoseum), que
vive fuera de este repositorio. Tono aspiracional: se habla de la tienda que la
marca puede tener, no del software.

El eje del deck no es el catalogo de funcionalidades, sino el argumento de retorno
que el propio documento pone en el centro: sobre un trafico que ya se esta pagando,
mejorar la conversion es dinero que aparece sin gastar un euro mas en publicidad.

Genera con: python build/build.py chocoseum

Nota: el texto de contenido lleva acentos y ene (UTF-8, sin BOM) por ser un
entregable para cliente; el codigo y los comentarios se mantienen en ASCII.
"""

import brand.theme as T
import content.fijas as F
import lib.slides as s

OUTFILE = "Chocoseum-Propuesta-Tienda.pptx"
TITULO = "Chocoseum - Propuesta de nueva tienda online"


def build(prs):
    p = [0]

    def n():
        p[0] += 1
        return p[0]

    # 1) PORTADA
    s.add_cover(
        prs,
        title="La tienda que Chocoseum *merece*",
        subtitle="Quince años, 56 premios y 220.000 clientes. Una tienda a su altura.",
        eyebrow="NaranjaTec - Propuesta",
        image=T.img("pighen-store.jpg"),
    )

    # 2) INDICE
    s.add_index(
        prs,
        "Qué *veremos*",
        [
            ("El problema", "El tráfico llega, la venta no.", T.ICON["pulse"]),
            ("La solución", "Una tienda pensada para convertir.", T.ICON["idea"]),
            ("La propuesta", "Qué se construye, pieza a pieza.", T.ICON["storage"]),
            ("La inversión", "Lo que cuesta y lo que devuelve.", T.ICON["check"]),
        ],
        page=n(),
    )

    # ---------------------------------------------------------------- 01
    s.add_section(prs, "El *problema*", number="01",
                  image=T.img("abordo-tienda.jpg"))

    # 3) LA FRASE QUE DUELE. Es el corazon del documento: el ROI sobre trafico
    # que ya se paga. Va sobre foto, a sangre, sin nada que la acompane.
    s.add_statement(
        prs,
        "Cada visita que entra por un anuncio y se va sin comprar es *dinero "
        "gastado dos veces*: se pagó por traerla y no dejó nada.",
        image=T.img("babidu-store.jpg"),
        page=n(),
    )

    # 4) POR QUE LA TIENDA ACTUAL NO CONVIERTE (4 limitaciones de CCV Shop)
    s.add_bullets(
        prs,
        "El techo de una *plantilla*",
        [
            ("La velocidad no se controla",
             "Una tienda lenta pierde visitas antes de mostrarse, y Google y "
             "Meta encarecen el clic.", T.ICON["bolt"]),
            ("El proceso de compra es rígido",
             "No se puede quitar fricción del checkout, que es donde se "
             "abandona el carrito.", T.ICON["cart"]),
            ("No hay landings por campaña",
             "San Valentín y el regalo de empresa aterrizan en el mismo "
             "catálogo genérico.", T.ICON["monitor"]),
            ("La estructura para buscadores es débil",
             "Se compite peor en Google sin pagar, y se depende más de las "
             "campañas.", T.ICON["globe"]),
        ],
        image=T.img("choptime-desktop.jpg"),
        subtitle="Se trabaja dentro de lo que la plantilla permite",
        page=n(), section="El problema",
    )

    # 5) LO QUE LA MARCA YA TIENE. El documento lo dice: son argumentos que hoy
    # no trabajan a su favor.
    s.add_stats_feature(
        prs,
        "Todo para *vender*",
        [
            {"value": "15", "label": "años de recorrido artesanal",
             "icon": T.ICON["shield"]},
            {"value": "220.000", "label": "clientes que ya han comprado",
             "icon": T.ICON["people"]},
            {"value": "56", "label": "premios de chocolate",
             "icon": T.ICON["cert"]},
            {"value": "4,8", "label": "de valoración media sobre 5",
             "icon": T.ICON["star"]},
        ],
        image=T.img("babidu-macbook.jpg"),
        subtitle="Argumentos que hoy no trabajan a favor de la marca",
        page=n(), section="El problema",
    )

    # ---------------------------------------------------------------- 02
    s.add_section(prs, "La *solución*", number="02",
                  image=T.img("ecco-office.jpg"))

    # 6) EL DESARROLLO A MEDIDA
    s.add_image_feature(
        prs,
        "Una tienda hecha para *convertir*",
        [
            "Se construye una tienda nueva sobre WordPress y WooCommerce: "
            "control total sobre el diseño, la velocidad, el SEO y cada paso "
            "del proceso de compra.",
            "El objetivo no es una web más bonita. Es que cada euro invertido "
            "en campañas termine en más pedidos.",
        ],
        image=T.img("importaco-macbookpro.jpg"),
        stat=("5", "mercados listos desde el primer día"),
        subtitle="WordPress y WooCommerce, sin techo",
        page=n(), section="La solución",
    )

    # 7) PLANTILLA CERRADA CONTRA DESARROLLO PROPIO
    s.add_two_column(
        prs,
        "Lo que permite y lo que *necesitas*",
        left={
            "heading": "Hoy: una plantilla cerrada",
            "icon": T.ICON["lock"],
            "items": [
                "La velocidad la decide la plataforma",
                "Un checkout que no se puede afinar",
                "Un catálogo genérico para toda campaña",
                "Dependencia creciente de la publicidad",
            ],
        },
        right={
            "heading": "Mañana: una tienda propia",
            "icon": T.ICON["idea"],
            "items": [
                "Velocidad y SEO bajo tu control",
                "Cada paso de la compra, afinado",
                "Una landing por ocasión y campaña",
                "Tráfico que llega sin pagarlo",
            ],
        },
        subtitle="Del techo de la plantilla al suelo de tu negocio",
        page=n(), section="La solución",
    )

    # 8) QUIENES SOMOS (FIJA)
    F.mision(prs, page=n(), section="La solución")

    # 9) DONDE SE TAPA CADA FUGA. Son 5 fases y add_numbered_grid trunca a 4 en
    # silencio: perderiamos justo la fase de las senales de confianza.
    s.add_service_grid(
        prs,
        "Dónde se tapa cada *fuga*",
        [
            {"title": "Del anuncio al clic",
             "desc": "Una web rápida mejora la puntuación del anuncio y abarata "
                     "el clic.", "icon": T.ICON["arrow"]},
            {"title": "Del clic a la página",
             "desc": "Cada campaña aterriza en una landing hecha para esa "
                     "ocasión.", "icon": T.ICON["location"]},
            {"title": "De la página a la ficha",
             "desc": "Fichas claras, con opciones de regalo y una llamada a la "
                     "acción visible.", "icon": T.ICON["monitor"]},
            {"title": "De la ficha al carrito",
             "desc": "Los premios, los clientes y el 4,8 se muestran donde se "
                     "decide la compra.", "icon": T.ICON["star"]},
            {"title": "Del carrito al pago",
             "desc": "Un checkout directo, con envío, regalo y recogida ya "
                     "resueltos.", "icon": T.ICON["cart"]},
        ],
        subtitle="El recorrido de una venta, fase a fase",
        page=n(), section="La solución",
    )

    # ---------------------------------------------------------------- 03
    s.add_section(prs, "La *propuesta*", number="03",
                  image=T.img("pighen-new-lookbook.jpg"))

    # 10) LOS CUATRO PILARES
    s.add_solution(
        prs,
        "Lo que sostiene la *tienda*",
        [
            ("Bloques reutilizables",
             "Las páginas se montan combinando bloques maquetados una sola vez. "
             "Las campañas se crean desde el panel, sin depender de nadie.",
             T.ICON["storage"]),
            ("Dos caminos de compra",
             "Por producto y por ocasión. El segundo conecta al que busca un "
             "regalo con un escaparate hecho para ese momento.",
             T.ICON["idea"]),
            ("Regalo corporativo",
             "Un canal propio para el pedido grande de empresa: volumen, "
             "personalización y solicitud de presupuesto.",
             T.ICON["people"]),
            ("Cinco idiomas",
             "La estructura queda lista y traducible, para vender fuera sin "
             "rehacer la tienda.",
             T.ICON["globe"]),
        ],
        images=[T.img("pighen-mobile.jpg"), T.img("abordo-web.jpg")],
        subtitle="Cuatro decisiones que cambian el negocio",
        highlight=0,
        page=n(), section="La propuesta",
    )

    # 11) LO QUE RODEA A LA VENTA
    s.add_feature_band(
        prs,
        "El chocolate llega *bien*",
        [
            {"icon": T.ICON["location"], "head": "Envío refrigerado",
             "text": "Control de temperatura, entrega en 24h y recogida en "
                     "tienda."},
            {"icon": T.ICON["cart"], "head": "Cajas de regalo",
             "text": "Variaciones de tamaño y mezcla, listas para elegir."},
            {"icon": T.ICON["star"], "head": "Opciones de regalo",
             "text": "Mensaje, envoltorio y fecha de entrega en la compra."},
            {"icon": T.ICON["idea"], "head": "Museo y talleres",
             "text": "Una colección gestionable que refuerza la marca."},
        ],
        image=T.img("pighen-b2b-cart.jpg"),
        intro="La logística que la marca ya domina, explicada donde frena la "
              "venta: dentro de la ficha.",
        page=n(), section="La propuesta",
    )

    # 12) CATALOGO DE BLOQUES. 24 -> 2 diapositivas. Los elegidos salen de lo que
    # el documento nombra: mega-menu, buscador predictivo, catalogo con filtros,
    # ficha, carrito, checkout, mi cuenta, ocasiones, museo, FAQ, newsletter...
    # OJO: add_blocks_grid recibe el contador `n`, no `n()`.
    s.add_blocks_grid(
        prs,
        "Los bloques de tu *tienda*",
        [
            ("hero-banner", "Hero de portada", "Imagen, titular y una acción."),
            ("mega-menu", "Mega-menú", "Categorías y ocasiones a la vez."),
            ("search-featured", "Buscador predictivo",
             "Encuentra el producto al teclear."),
            ("category-grid", "Rejilla de categorías",
             "Bombones, trufas, veganos, halal."),
            ("product-carousel", "Carrusel de productos",
             "Destacados y ediciones limitadas."),
            ("benefits-band", "Banda de ventajas",
             "Envío refrigerado, 24h, recogida."),
            ("shop-catalog", "Catálogo con filtros",
             "Filtra por tipo, dieta y precio."),
            ("product-category", "Plantilla de categoría",
             "El escaparate de cada familia."),
            ("product-detail", "Ficha de producto",
             "Distintivos, regalo y confianza."),
            ("cart", "Carrito", "Con el envío ya resuelto."),
            ("checkout", "Checkout", "Directo, sin pasos de más."),
            ("my-account", "Mi cuenta", "Pedidos y datos del cliente."),
            ("promo-banner", "Landing de ocasión",
             "San Valentín, Navidad, empresa."),
            ("text-image", "Texto e imagen", "La historia artesanal."),
            ("text-image-alt", "Imagen y texto", "La variante alterna."),
            ("welcome-video", "Vídeo", "El obrador, en movimiento."),
            ("testimonials", "Testimonios", "Quien ya compró, lo cuenta."),
            ("google-reviews", "Valoraciones de Google",
             "El 4,8 donde se decide la compra."),
            ("faq-accordion", "Preguntas frecuentes",
             "Las dudas que frenan el pedido."),
            ("newsletter", "Newsletter", "La lista que no se alquila."),
            ("cta-banner", "Banner de acción",
             "El siguiente paso, siempre visible."),
            ("latest-news", "Últimas del blog", "Recetas, origen y marca."),
            ("cpt-showcase", "Experiencias del museo",
             "Talleres y visitas, gestionables."),
            ("footer-columns", "Pie completo", "Legales, envíos y contacto."),
        ],
        subtitle="Se maquetan una vez y se combinan para siempre",
        page=n, section="La propuesta",
    )

    # 13) TESTIMONIO (FIJA). Canon habla de autonomia: "mantener actualizada de
    # forma independiente". Es exactamente el argumento del sistema de bloques.
    F.testimonio(prs, page=n(), section="La propuesta",
                 temas=("autonomia", "diseno", "proceso"))

    # ---------------------------------------------------------------- 04
    s.add_section(prs, "La *inversión*", number="04",
                  image=T.img("oficina/naranjatec_4273.jpg"))

    # 14) EL PROYECTO EN CIFRAS. El deck habla en euros: no se muestran horas en
    # ningun sitio. Si aqui apareciesen las 43 horas junto a los 6.450 euros,
    # bastaria dividir para deducir la tarifa por hora.
    s.add_stats(
        prs,
        [
            {"value": "6.450 €", "label": "de inversión estimada"},
            {"value": "24", "label": "bloques reutilizables"},
            {"value": "5", "label": "idiomas listos"},
        ],
        title="El proyecto en cifras",
        subtitle="Lo que se construye",
        page=n(), section="La inversión",
    )

    # 15) DESGLOSE. Las cinco partidas del documento, convertidas de horas a
    # euros a la tarifa acordada: 5,5 + 13,5 + 12 + 2,5 + 9,5 = 43 horas. El
    # total lo suma add_pricing, asi que no puede desviarse de las filas.
    # OJO: add_pricing recibe el contador `n`, no `n()`.
    s.add_pricing(
        prs,
        "Desglose del *proyecto*",
        [
            ("Estructura y elementos comunes", 825),
            ("Tienda WooCommerce a medida", 2025),
            ("Plantillas de tienda", 1800),
            ("Contenido gestionable", 375),
            ("Bloques de contenido", 1425),
        ],
        note="Las ampliaciones opcionales se presupuestan aparte y pueden "
             "incorporarse en cualquier momento.",
        subtitle="Lo que incluye el desarrollo, partida a partida",
        page=n, section="La inversión",
    )

    # 16) AMPLIACIONES OPCIONALES: 2, 4 y 4 horas, a la misma tarifa.
    s.add_extras(
        prs,
        "Si quieres ir más *lejos*",
        [
            {"price": 300, "name": "Lista de deseos",
             "desc": "El cliente guarda lo que quiere y vuelve a por ello.",
             "icon": T.ICON["star"], "image": T.img("pighen-new-iphone.jpg")},
            {"price": 600, "name": "Club de suscripción",
             "desc": "Chocolate cada mes, con cobro recurrente.",
             "icon": T.ICON["sync"], "image": T.img("babidu-iphonex.jpg")},
            {"price": 600, "name": "Importar el catálogo",
             "desc": "Los productos actuales pasan a la tienda nueva.",
             "icon": T.ICON["storage"], "image": T.img("abordo-tienda.jpg")},
        ],
        subtitle="Ampliaciones opcionales",
        page=n(), section="La inversión",
    )

    # 17) PROXIMOS PASOS (FIJA)
    F.proximos_pasos(prs, page=n(), section="Siguiente")

    # 18) CIERRE
    s.add_cta(
        prs,
        "Hablemos de tu *tienda*",
        F.contacto_cta(),
        subtext="Quince años de chocolate merecen una tienda que los cuente.",
        image=T.img("pighen-new-mac.jpg"),
    )

    return prs
