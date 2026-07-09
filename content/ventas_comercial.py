"""Contenido del deck comercial / de ventas de NaranjaTec.

BORRADOR redactado a partir de naranjatec.com y de buenas practicas de venta,
usando la biblioteca de imagenes del proyecto (brand/assets/img). Revisa y ajusta
los textos: cambiar el contenido no requiere tocar lib/slides.py. Los apartados
marcados con [REVISAR] necesitan datos reales (casos, metricas, testimonios,
contacto).
"""

import brand.theme as T
import lib.slides as s

OUTFILE = "NaranjaTec-Ventas-Comercial.pptx"
TITULO = "NaranjaTec - Presentacion comercial"


def build(prs):
    page = [0]

    def n():
        page[0] += 1
        return page[0]

    # 1. PORTADA / HERO
    s.add_cover(
        prs,
        title="Tu partner tecnologico para *crecer online*",
        subtitle="Hosting, desarrollo web y soporte para PYMEs. Mas de 22 anos "
                 "cuidando de tu presencia digital.",
        eyebrow="Hosting - Desarrollo - Soporte",
        image=T.img("naranjatec-web.jpg"),
        cta="www.naranjatec.com",
    )

    # 2. INDICE
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

    # 3. SECCION 01
    s.add_section(prs, "Quienes somos", number="01",
                  image=T.img("imporaco-reuniones.jpg"))

    # 4. QUIENES SOMOS (texto + imagen + dato)
    s.add_image_feature(
        prs,
        "Mas de 22 anos cuidando tu presencia online",
        [
            "Acompanamos a las PYMEs en su digitalizacion con un servicio cercano "
            "y personalizado, sin call centers ni respuestas automaticas.",
            "Hosting, desarrollo y soporte bajo un unico proveedor de confianza: "
            "todo en un mismo sitio.",
        ],
        image=T.img("accompany-meeting.jpg"),
        stat=("+22", "anos"),
        side="right",
        page=n(),
        section="Quienes somos",
    )

    # 5. SECCION 02
    s.add_section(prs, "El reto de *digitalizar* tu negocio", number="02",
                  image=T.img("ecco-working.jpg"))

    # 6. EL RETO (dos columnas)
    s.add_two_column(
        prs,
        "Estar online no es suficiente",
        left={
            "heading": "Lo que frena a muchas PYMEs",
            "items": [
                "Webs lentas o caidas que cuestan clientes",
                "Proveedores lejanos y soporte impersonal",
                "Multiples facturas y proveedores dispersos",
                "Falta de tiempo y conocimiento tecnico",
            ],
        },
        right={
            "heading": "Lo que necesitas de verdad",
            "items": [
                "Una base tecnica solida y fiable",
                "Un unico interlocutor que te entienda",
                "Rapidez, seguridad y tranquilidad",
                "Alguien que se ocupe por ti",
            ],
        },
        page=n(),
        section="El reto",
    )

    # 7. PROPUESTA DE VALOR (vinetas)
    s.add_bullets(
        prs,
        "Nuestra propuesta de valor",
        [
            ("Creamos", "Disenamos y desarrollamos tu web o tienda a medida."),
            ("Cuidamos", "Alojamos, protegemos y mantenemos tus activos online."),
            ("Optimizamos", "Mejoramos rendimiento, seguridad y resultados en el tiempo."),
        ],
        page=n(),
        section="El reto",
    )

    # 8. SECCION 03
    s.add_section(prs, "Nuestros servicios", number="03",
                  image=T.img("ecco-office.jpg"))

    # 9. Servicios: Hosting e infraestructura
    s.add_service_grid(
        prs,
        "Hosting e infraestructura",
        [
            {"title": "Dominios", "desc": "Registro y gestion de tu dominio ideal.", "icon": T.ICON["globe"]},
            {"title": "Hosting Linux", "desc": "Alojamiento rapido y estable para tu web.", "icon": T.ICON["server"]},
            {"title": "VPS", "desc": "Servidores virtuales escalables a tu medida.", "icon": T.ICON["network"]},
            {"title": "Servidores dedicados", "desc": "Maxima potencia y control exclusivo.", "icon": T.ICON["rack"]},
            {"title": "Email profesional", "desc": "Correo con tu dominio y antispam.", "icon": T.ICON["mail"]},
            {"title": "Certificados SSL", "desc": "Seguridad y confianza para tus visitantes.", "icon": T.ICON["lock"]},
        ],
        page=n(),
        section="Servicios",
    )

    # 10. Servicios: Desarrollo y diseno
    s.add_service_grid(
        prs,
        "Desarrollo y diseno",
        [
            {"title": "Diseno web", "desc": "Webs corporativas modernas y responsive.", "icon": T.ICON["monitor"]},
            {"title": "Tiendas online", "desc": "E-commerce listo para vender.", "icon": T.ICON["cart"]},
            {"title": "Apps moviles", "desc": "Aplicaciones a medida para tu negocio.", "icon": T.ICON["mobile"]},
        ],
        page=n(),
        section="Servicios",
    )

    # 11. Servicios: Soporte y gestion
    s.add_service_grid(
        prs,
        "Soporte y gestion",
        [
            {"title": "Mantenimiento WordPress", "desc": "Actualizaciones y copias de seguridad.", "icon": T.ICON["wrench"]},
            {"title": "Private Cloud", "desc": "Tu nube privada, segura y flexible.", "icon": T.ICON["cloud"]},
            {"title": "AntiSpam", "desc": "Proteccion frente a correo no deseado.", "icon": T.ICON["shield"]},
            {"title": "Portal de cliente", "desc": "Gestiona tus servicios en un clic.", "icon": T.ICON["person"]},
        ],
        page=n(),
        section="Servicios",
    )

    # 12. SECCION 04
    s.add_section(prs, "Proyectos y metodo", number="04",
                  image=T.img("ecco-night.jpg"))

    # 13. Caso de portfolio 1 (imagen derecha)
    s.add_image_feature(
        prs,
        "Tiendas online que venden",
        [
            "Disenamos e-commerce a medida, rapidos y faciles de gestionar, "
            "pensados para convertir visitas en ventas.",
            "[REVISAR] Anade aqui el resultado del caso (ventas, trafico, etc.).",
        ],
        image=T.img("pighen-new-mac.jpg"),
        side="right",
        page=n(),
        section="Proyectos",
    )

    # 14. Caso de portfolio 2 (imagen izquierda)
    s.add_image_feature(
        prs,
        "Webs corporativas que inspiran",
        [
            "Creamos sitios corporativos modernos y responsive que transmiten "
            "confianza y reflejan la marca de cada cliente.",
            "[REVISAR] Anade aqui el resultado del caso (leads, imagen, etc.).",
        ],
        image=T.img("credo-laptop.jpg"),
        side="left",
        page=n(),
        section="Proyectos",
    )

    # 15. Como trabajamos (proceso)
    s.add_process(
        prs,
        "Como trabajamos contigo",
        [
            ("Escuchamos", "Entendemos tu negocio, tus objetivos y tu punto de partida."),
            ("Proponemos", "Disenamos la solucion adecuada, sin humo ni sobrecostes."),
            ("Implementamos", "Ponemos todo en marcha con rapidez y buenas practicas."),
            ("Acompanamos", "Te cuidamos y optimizamos de forma continua."),
        ],
        page=n(),
        section="Metodo",
    )

    # 16. Por que NaranjaTec (cifras)
    s.add_stats(
        prs,
        [
            {"value": "+22", "label": "anos de experiencia"},
            {"value": "360", "label": "servicio integral: web, hosting y soporte"},
            {"value": "1", "label": "unico interlocutor para todo"},
        ],
        title="Por que elegir NaranjaTec",
        page=n(),
        section="Ventajas",
    )

    # 17. Testimonio [REVISAR: sustituir por testimonio y cliente reales]
    s.add_quote(
        prs,
        "[REVISAR] Frase real de un cliente satisfecho que aporte confianza y "
        "resuma el valor que le aportamos.",
        author="[REVISAR] Nombre del cliente",
        role="[REVISAR] Cargo - Empresa",
        page=n(),
        section="Testimonio",
    )

    # 18. Cierre / CTA [REVISAR: datos de contacto reales]
    s.add_cta(
        prs,
        headline="Hablemos de tu *proyecto*",
        subtext="Da el siguiente paso en tu digitalizacion.",
        contact_lines=[
            "Web: www.naranjatec.com",
            "Email: [REVISAR] info@naranjatec.com",
            "Telefono: [REVISAR] +34 000 000 000",
        ],
    )

    return prs
