"""Deck UNICO de test de disenos: una diapositiva de cada tipo disponible en
lib/slides.py (incluidos los layouts nuevos: declaracion, linea de tiempo,
comparativa y galerias). Sirve para iterar el diseno de cada layout.

Genera con: python build/build.py test
"""

import brand.theme as T
import lib.slides as s

OUTFILE = "NaranjaTec-Test-Disenos.pptx"
TITULO = "NaranjaTec - Test de disenos"

LOREM = ("Ed ut perspiciatis unde omnis iste natus error sit voluptatem "
         "accusantium doloremque laudantium, totam rem aperiam.")


def build(prs):
    p = [0]

    def n():
        p[0] += 1
        return p[0]

    # 1) PORTADA / HERO con imagen
    s.add_cover(
        prs,
        title="Tu partner tecnologico para *crecer online*",
        subtitle="Subtitulo con la frase de apoyo que resume la propuesta.",
        eyebrow="Hosting - Desarrollo - Soporte",
        image=T.img("naranjatec-web.jpg"),
    )

    # 2) AGENDA (tarjetas con icono)
    s.add_index(
        prs,
        "Que veremos hoy",
        [
            ("Quienes somos", "Mas de 22 anos"),
            ("El reto", "Digitalizar la PYME"),
            ("Nuestros servicios", "Todo en un sitio"),
            ("Trabajemos juntos", "Siguiente paso"),
        ],
        page=n(),
    )

    # 3) SEPARADOR DE SECCION con foto de fondo
    s.add_section(prs, "Separador de *seccion*", number="01",
                  image=T.img("ecco-office.jpg"))

    # 4) DECLARACION / CITA a sangre completa (NUEVO)
    s.add_statement(
        prs,
        "Algo mas que informar, *inspirar*: cuidamos tu presencia digital "
        "como si fuera la nuestra.",
        image=T.img("babidu-hand.jpg"),
        author="NaranjaTec",
        page=n(),
    )

    # 5) VINETAS con titulo y detalle
    s.add_bullets(
        prs,
        "Vinetas con titulo y detalle",
        [
            ("Primer punto", "Explicacion breve del primer punto.", T.ICON["cloud"]),
            ("Segundo punto", "Explicacion breve del segundo punto.", T.ICON["shield"]),
            ("Tercer punto", "Explicacion breve del tercer punto.", T.ICON["code"]),
            ("Cuarto punto", "Explicacion breve del cuarto punto.", T.ICON["wrench"]),
        ],
        image=T.img("accompany-meeting.jpg"),
        subtitle="Un subtitulo de apoyo en cursiva",
        page=n(),
        section="Ejemplo",
    )

    # 6) DOS COLUMNAS
    s.add_two_column(
        prs,
        "Dos columnas enfrentadas",
        left={"heading": "Lo que frena a las PYMEs", "icon": T.ICON["pulse"],
              "items": ["Webs lentas o caidas", "Soporte impersonal",
                        "Multiples proveedores", "Falta de tiempo"]},
        right={"heading": "Lo que necesitas", "icon": T.ICON["shield"],
               "items": ["Base tecnica solida", "Un unico interlocutor",
                         "Rapidez y seguridad", "Alguien que se ocupe"]},
        subtitle="Del reto a la solucion",
        page=n(),
        section="Ejemplo",
    )

    # 7) REJILLA DE SERVICIOS (6 tarjetas)
    s.add_service_grid(
        prs,
        "Rejilla de servicios",
        [
            {"title": "Hosting", "desc": "Alojamiento rapido y estable.", "icon": T.ICON["server"]},
            {"title": "Dominios", "desc": "Tu dominio ideal, gestionado.", "icon": T.ICON["globe"]},
            {"title": "Email", "desc": "Correo profesional con tu marca.", "icon": T.ICON["mail"]},
            {"title": "Seguridad", "desc": "SSL y proteccion antispam.", "icon": T.ICON["lock"]},
            {"title": "Desarrollo", "desc": "Webs y apps a medida.", "icon": T.ICON["code"]},
            {"title": "Soporte", "desc": "Mantenimiento y optimizacion.", "icon": T.ICON["wrench"]},
            {"title": "Cloud", "desc": "Infraestructura escalable.", "icon": T.ICON["cloud"]},
            {"title": "Backups", "desc": "Copias diarias automaticas.", "icon": T.ICON["sync"]},
            {"title": "Analitica", "desc": "Medicion y mejora continua.", "icon": T.ICON["pulse"]},
        ],
        subtitle="Todo lo que tu PYME necesita, en un mismo sitio",
        page=n(),
        section="Ejemplo",
    )

    # 8) PROCESO (pasos numerados 2x2)
    s.add_process(
        prs,
        "Proceso en cuatro pasos",
        [
            ("Escuchamos", "Entendemos tu negocio y tus objetivos."),
            ("Proponemos", "Disenamos la solucion adecuada."),
            ("Implementamos", "Ponemos todo en marcha con buenas practicas."),
            ("Acompanamos", "Cuidamos y optimizamos de forma continua."),
        ],
        page=n(),
        section="Ejemplo",
    )

    # 9) TEXTO + IMAGEN + dato (derecha)
    s.add_image_feature(
        prs,
        "Texto con imagen y dato",
        [
            "Bloque de texto a la izquierda que describe el servicio o el caso.",
            "Puede tener varios parrafos con detalle y contexto para el cliente.",
        ],
        image=T.img("ecco-working.jpg"),
        stat=("+350", "proyectos"),
        subtitle="Texto, imagen y un dato destacado",
        page=n(),
        section="Ejemplo",
    )

    # 10) TEXTO + IMAGEN (izquierda)
    s.add_image_feature(
        prs,
        "Imagen a la izquierda",
        [LOREM, "Segundo parrafo de apoyo con mas contexto del caso."],
        image=T.img("importaco-macbookpro.jpg"),
        side="left",
        subtitle="Imagen a un lado, texto al otro",
        page=n(),
        section="Ejemplo",
    )

    # 11) CIFRAS DESTACADAS
    s.add_stats(
        prs,
        [
            {"value": "+22", "label": "anos de experiencia"},
            {"value": "98%", "label": "clientes que renuevan"},
            {"value": "24/7", "label": "soporte y monitorizacion"},
        ],
        title="Cifras destacadas",
        subtitle="Los numeros que nos avalan",
        page=n(),
        section="Ejemplo",
    )

    # 11b) DESGLOSE DE PRESUPUESTO (NUEVO)
    s.add_pricing(
        prs,
        "Desglose de la *inversion*",
        [("Descubrimiento y diseno UX", 1300),
         ("Desarrollo a medida", 2950),
         ("Contenidos, QA y lanzamiento", 1280)],
        note="Calculado para un catalogo de unas 2.000 referencias. Un "
             "surtido mayor puede influir en el precio. Precios sin IVA.",
        subtitle="Todo lo que incluye la propuesta",
        page=n,
        section="INVERSION",
    )

    # 12) LINEA DE TIEMPO (NUEVO)
    s.add_timeline(
        prs,
        "Nuestra trayectoria",
        [
            {"year": "2003", "label": "Nacimiento", "icon": T.ICON["bolt"],
             "text": "Arrancamos como proveedor de hosting cercano para PYMEs, "
                     "con un trato directo y sin intermediarios."},
            {"year": "2014", "label": "Desarrollo web", "icon": T.ICON["code"],
             "text": "Ampliamos a diseno y desarrollo de webs y tiendas online a "
                     "medida de cada negocio."},
            {"year": "2025", "label": "Servicio integral", "icon": T.ICON["cloud"],
             "text": "Hosting, desarrollo y soporte bajo un unico proveedor de "
                     "confianza."},
        ],
        subtitle="Como hemos crecido, paso a paso",
        section="Historia",
    )

    # 13) TABLA COMPARATIVA (NUEVO)
    s.add_comparison(
        prs,
        "Por que elegirnos",
        ["Caracteristica", "NaranjaTec", "Proveedor A", "Proveedor B"],
        [
            {"label": "Soporte cercano", "marks": [True, False, False]},
            {"label": "Todo en un sitio", "marks": [True, False, True]},
            {"label": "Precio ajustado", "marks": [True, True, False]},
            {"label": "Sin permanencia", "marks": [True, False, False]},
            {"label": "Monitorizacion 24/7", "marks": [True, True, True]},
        ],
        subtitle="Comparanos con otros proveedores",
        page=n(),
        section="Comparativa",
    )

    # 14) GALERIA + LISTA (4 imagenes) (NUEVO)
    s.add_gallery_list(
        prs,
        "Galeria de cuatro imagenes",
        "Insert Awesome Sub-title Here",
        [
            ("Primer titular", "Descripcion breve del primer punto de la lista."),
            ("Segundo titular", "Descripcion breve del segundo punto de la lista."),
            ("Tercer titular", "Descripcion breve del tercer punto de la lista."),
            ("Cuarto titular", "Descripcion breve del cuarto punto de la lista."),
        ],
        [T.img("ecco-office.jpg"), T.img("canonbcn-imac.jpg"),
         T.img("springvale-home.jpg"), T.img("imporaco-reuniones.jpg")],
        page=n(),
    )

    # 15) GALERIA + LISTA (2 imagenes) (NUEVO)
    s.add_gallery_list(
        prs,
        "Galeria de dos imagenes",
        "Insert Awesome Sub-title Here",
        [
            ("Primer titular", "Descripcion breve del primer punto de la lista."),
            ("Segundo titular", "Descripcion breve del segundo punto de la lista."),
            ("Tercer titular", "Descripcion breve del tercer punto de la lista."),
            ("Cuarto titular", "Descripcion breve del cuarto punto de la lista."),
        ],
        [T.img("ecco-working.jpg"), T.img("credo-laptop.jpg")],
        page=n(),
    )

    # 16) TEXTO + GALERIA (3 imagenes verticales) (NUEVO)
    s.add_gallery_text(
        prs,
        "Texto con tres imagenes",
        "Header Info One",
        [LOREM, "Segundo parrafo con mas detalle y contexto para el cliente."],
        [T.img("pighen-mobile.jpg"), T.img("vielong-iphonex.jpg"),
         T.img("sinrodeos-iphone.jpg")],
        subtitle="Proyectos recientes",
        page=n(),
        section="Galeria",
    )

    # 17) MOSAICO DE 5 IMAGENES (NUEVO)
    s.add_gallery_mosaic(
        prs,
        "Mosaico de cinco imagenes",
        [T.img("naranjatec-web.jpg"), T.img("canonbcn-laptop.jpg"),
         T.img("springvale-portatil.jpg"), T.img("holanda-laptop.jpg"),
         T.img("ecco-night.jpg")],
        subtitle="Una muestra de nuestro trabajo",
        page=n(),
        section="Galeria",
    )

    # 18) BANDA DE FEATURES sobre imagen (NUEVO)
    s.add_feature_band(
        prs,
        "Modelo de servicio",
        [
            {"icon": T.ICON["globe"], "head": "Presencia", "text": "Tu web y dominio, siempre online."},
            {"icon": T.ICON["shield"], "head": "Seguridad", "text": "SSL, backups y monitorizacion 24/7."},
            {"icon": T.ICON["code"], "head": "Desarrollo", "text": "Webs y apps a medida de tu negocio."},
            {"icon": T.ICON["wrench"], "head": "Soporte", "text": "Mantenimiento cercano y sin call centers."},
        ],
        image=T.img("imporaco-reuniones.jpg"),
        intro="Todo lo que tu PYME necesita para crecer online, bajo un unico proveedor de confianza.",
        subtitle="Cuatro pilares para tu presencia digital",
        page=n(),
        section="Modelo",
    )

    # 19) MISION: features + imagen con pie oscuro (NUEVO)
    s.add_mission(
        prs,
        "Nuestra mision",
        [
            {"icon": T.ICON["people"], "head": "Cercania", "text": "Trato directo, sin intermediarios ni respuestas automaticas."},
            {"icon": T.ICON["bolt"], "head": "Agilidad", "text": "Resolvemos rapido para que tu negocio no se detenga."},
            {"icon": T.ICON["gear"], "head": "Integral", "text": "Hosting, desarrollo y soporte en un mismo sitio."},
            {"icon": T.ICON["check"], "head": "Compromiso", "text": "Cuidamos tu presencia digital como si fuera nuestra."},
        ],
        image=T.img("accompany-meeting.jpg"),
        caption_title="Algo mas que *informar*",
        caption_text="Acompanamos a las PYMEs en su digitalizacion desde hace mas de 22 anos.",
        page=n(),
        section="Mision",
    )

    # 20) REJILLA NUMERADA + declaracion resaltada (NUEVO)
    s.add_numbered_grid(
        prs,
        "Infraestructura tecnologica",
        [
            ("Cloud", "Servidores rapidos y escalables."),
            ("Seguridad", "SSL, WAF y copias diarias."),
            ("Rendimiento", "CDN y optimizacion continua."),
            ("Soporte", "Equipo tecnico propio."),
        ],
        highlight="La innovacion y la cercania son el nucleo de todo lo que hacemos.",
        page=n(),
        section="Tecnologia",
    )

    # HERO CON TARJETA sobre foto (NUEVO)
    s.add_hero_card(
        prs,
        "Pasion, cercania y *compromiso*",
        "Cuidamos tu presencia digital con un trato directo y un servicio "
        "integral, poniendo atencion en cada detalle.",
        cta="Ver servicios",
        image=T.img("imporaco-reuniones.jpg"),
        page=n(),
    )

    # 21) TARJETAS DE VALOR (imagen + tarjetas) (NUEVO)
    s.add_value_cards(
        prs,
        "Nuestros *valores*",
        image=T.img("importaco-macbookpro.jpg"),
        cards=[
            {"head": "Compromiso", "text": "Cuidamos cada proyecto como si fuera nuestro."},
            {"head": "Cercania", "text": "Trato directo, sin call centers ni respuestas automaticas."},
            {"value": "+350", "label": "proyectos entregados"},
        ],
        subtitle="Lo que nos mueve cada dia",
        page=n(),
        section="Valores",
    )

    # 22) RESUMEN (texto + imagenes + puntos) (NUEVO)
    s.add_overview(
        prs,
        "Resumen de servicios",
        "Todo lo que tu PYME necesita para crecer online",
        [LOREM, "Segundo parrafo con mas contexto y detalle del servicio."],
        [
            ("Hosting y dominios", "Alojamiento rapido y estable con tu dominio."),
            ("Desarrollo y soporte", "Webs a medida y mantenimiento continuo."),
        ],
        [T.img("ecco-office.jpg"), T.img("imporaco-reuniones.jpg")],
        subtitle="Una vision de conjunto",
        page=n(),
        section="Resumen",
    )

    # 23) PRODUCTO (titulo + cifra + filas con imagen) (NUEVO)
    s.add_product(
        prs,
        "Nuestro *producto*",
        "15M+",
        "Hosting y desarrollo web",
        [
            {"head": "Hosting gestionado", "text": "Servidores optimizados.",
             "image": T.img("ecco-dashboard.jpg"),
             "desc": "Alojamiento rapido, seguro y monitorizado 24/7 para tu web."},
            {"head": "Desarrollo a medida", "text": "Webs y tiendas online.",
             "image": T.img("springvale-portatil.jpg"),
             "desc": "Disenamos y desarrollamos la solucion que tu negocio necesita."},
            {"head": "Soporte cercano", "text": "Equipo tecnico propio.",
             "image": T.img("canonbcn-laptop.jpg"),
             "desc": "Mantenimiento, optimizacion y ayuda directa cuando la necesitas."},
        ],
        page=n(),
        section="Producto",
    )

    # 18) TESTIMONIO con avatar
    s.add_quote(
        prs,
        "Un texto de testimonio real de un cliente satisfecho que aporta confianza.",
        author="Nombre del cliente",
        role="Cargo - Empresa",
        avatar=T.img("avatars/avatar-canon.jpg"),
        image=T.img("accompany-meeting.jpg"),
        page=n(),
        section="Testimonio",
    )

    # 19) CIERRE / CTA
    s.add_cta(
        prs,
        headline="Hablemos de tu *proyecto*",
        subtext="Da el siguiente paso en tu digitalizacion.",
        contact=[
            (T.ICON["globe"], "www.naranjatec.com"),
            (T.ICON["mail"], "info@naranjatec.com"),
            (T.ICON["phone"], "+34 000 000 000"),
        ],
        image=T.img("oficina/naranjatec_4273.jpg"),
    )

    # 23b) EXTRAS: productos adicionales en tarjetas altas (NUEVO)
    s.add_extras(
        prs,
        "Ampliaciones *opcionales*",
        [
            {"price": 375, "name": "Busquedas guardadas",
             "desc": "Alertas por email de nuevas propiedades.",
             "icon": T.ICON["mail"], "image": T.img("ecco-working.jpg")},
            {"price": 150, "name": "Resenas de Google",
             "desc": "Integradas y actualizadas solas.",
             "icon": T.ICON["star"], "image": T.img("ecco-office.jpg")},
            {"price": 600, "name": "Panel de analitica",
             "desc": "Que buscan y donde abandonan.",
             "icon": T.ICON["pulse"], "image": T.img("ecco-night.jpg")},
            {"price": 900, "name": "Portal del cliente",
             "desc": "Acceso privado a documentacion.",
             "icon": T.ICON["lock"], "image": T.img("accompany-meeting.jpg")},
        ],
        subtitle="Se contratan aparte, cuando quieras",
        page=n(), section="EXTRAS",
    )

    # 23c) EXTRA DESTACADO: panel de color sobre foto (NUEVO)
    s.add_spotlight(
        prs,
        "Mantenimiento *gestionado*",
        [
            "Nos ocupamos de las actualizaciones, las copias y la seguridad, "
            "para que tu solo te ocupes de vender.",
            "Incluye monitorizacion, parches y un informe mensual.",
        ],
        image=T.img("ecco-night.jpg"),
        price=1200,
        page=n(), section="EXTRA",
    )

    # 23d) SOLUCION: dos fotos solapadas + puntos, uno destacado (NUEVO)
    s.add_solution(
        prs,
        "Nuestra *solucion*",
        [
            ("Rapida e indexable",
             "Paginas propias de zona que posicionan en Google.",
             T.ICON["bolt"]),
            ("Buscador propio", "Separa tu cartera del feed generico.",
             T.ICON["globe"]),
            ("Cero friccion", "Panel lateral con la referencia ya cargada.",
             T.ICON["idea"]),
            ("Confianza", "Testimonios donde se decide la compra.",
             T.ICON["shield"]),
        ],
        images=[T.img("imporaco-reuniones.jpg"), T.img("ecco-working.jpg")],
        subtitle="Donde se tapa cada fuga",
        highlight=1, page=n(), section="LA SOLUCION",
    )

    # 23e) MENSAJE DESTACADO a tres columnas (NUEVO)
    s.add_message(
        prs,
        "Fundador",
        "Un mensaje *personal*",
        image=T.img("oficina/naranjatec_4273.jpg"),
        lead="Llevamos 22 anos montando la tecnologia de las PYMEs que no "
             "quieren depender de nadie.",
        body=[
            "Cuando una web se percibe premium, la agencia se percibe premium. "
            "Por eso cuidamos la tipografia, el espacio y la fotografia tanto "
            "como el codigo que hay debajo.",
            "No entregamos una plantilla: entregamos un sistema que tu equipo "
            "puede mantener sin llamarnos.",
        ],
        author="Miguel Angel",
        role="Fundador de NaranjaTec",
        page=n(),
    )

    # 24) GRACIAS / CIERRE sobre foto (NUEVO)
    s.add_thanks(
        prs,
        "Gracias por *tu atencion*",
        [
            (T.ICON["globe"], "Web", "www.naranjatec.com"),
            (T.ICON["mail"], "Email", "info@naranjatec.com"),
            (T.ICON["phone"], "Telefono", "+34 000 000 000"),
        ],
        image=T.img("accompany-meeting.jpg"),
    )
    return prs
