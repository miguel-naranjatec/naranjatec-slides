"""Genera la biblioteca de esquemas de bloques de pagina como SVG.

Por que un generador y no 60 ficheros a mano: los esquemas solo sirven si TODOS
hablan el mismo idioma visual (mismo grosor de trazo, mismos grises, misma caja
de imagen). Componiendolos con un juego de primitivas eso queda garantizado, y
el resultado siguen siendo .svg de verdad, reutilizables fuera de este repo
(web, Figma, documentacion).

Uso:
    python scripts/gen_blocks.py            # escribe brand/assets/blocks/*.svg
    python scripts/make_blocks.py           # y luego los rasteriza a PNG

Lienzo: viewBox 320x180 (16:9), sin fondo. Los esquemas se leen a 2 cm de ancho,
asi que no llevan texto: solo barras que sugieren texto.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "brand" / "assets" / "blocks"

W, H = 320, 180
NAVY = "#0B3D66"     # trazo principal (azul profundo de marca)
GOLD = "#FFCD33"     # acento: el elemento activo / la llamada a la accion
MUTE = "#C3CEDA"     # barras que sugieren texto
LIGHT = "#E9EEF3"    # rellenos suaves


# --- Primitivas -----------------------------------------------------------

def box(x, y, w, h, r=6, fill="none", stroke=NAVY, sw=3):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"/>' % (x, y, w, h, r, fill, stroke, sw))


def solid(x, y, w, h, r=3, fill=MUTE):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>'
            % (x, y, w, h, r, fill))


def frame():
    return box(6, 6, W - 12, H - 12, r=10, sw=3)


def imgbox(x, y, w, h, r=6):
    """Caja de imagen: marco + aspa, el simbolo universal de 'aqui va una foto'."""
    return (box(x, y, w, h, r=r, fill=LIGHT) +
            '<path d="M%g %g L%g %g M%g %g L%g %g" stroke="%s" stroke-width="2.5" '
            'opacity="0.55"/>' % (x, y, x + w, y + h, x + w, y, x, y + h, NAVY))


def play(cx, cy, r=13):
    return ('<circle cx="%g" cy="%g" r="%g" fill="%s"/>'
            '<path d="M%g %g L%g %g L%g %g Z" fill="%s"/>'
            % (cx, cy, r, NAVY, cx - r * 0.28, cy - r * 0.42,
               cx + r * 0.45, cy, cx - r * 0.28, cy + r * 0.42, "#FFFFFF"))


def lines(x, y, w, n=3, gap=11, h=6, last=0.6):
    out = []
    for i in range(n):
        ww = w * last if i == n - 1 else w
        out.append(solid(x, y + i * gap, ww, h))
    return "".join(out)


def title_line(x, y, w, h=10):
    return solid(x, y, w, h, r=4, fill=NAVY)


def btn(x, y, w=56, h=18):
    return solid(x, y, w, h, r=9, fill=GOLD)


def dots(cx, cy, n=3, active=0, r=5, gap=16):
    out = []
    x0 = cx - (n - 1) * gap / 2.0
    for i in range(n):
        c = GOLD if i == active else NAVY
        out.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>'
                   % (x0 + i * gap, cy, r, c))
    return "".join(out)


def circle(cx, cy, r, fill=NAVY):
    return '<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (cx, cy, r, fill)


def ring(cx, cy, r, sw=3):
    return ('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" '
            'stroke-width="%g"/>' % (cx, cy, r, NAVY, sw))


def grid(x, y, w, h, cols, rows, gap=8, img=False):
    out = []
    cw = (w - (cols - 1) * gap) / cols
    ch = (h - (rows - 1) * gap) / rows
    for r in range(rows):
        for c in range(cols):
            cx = x + c * (cw + gap)
            cy = y + r * (ch + gap)
            out.append(imgbox(cx, cy, cw, ch) if img else box(cx, cy, cw, ch, sw=2.5))
    return "".join(out)


def arrows(y, r=9):
    return (ring(20, y, r, sw=2.5) + ring(W - 20, y, r, sw=2.5))


def star(cx, cy, r=8, fill=GOLD):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


def plus(cx, cy, s=6):
    return ('<path d="M%g %g H%g M%g %g V%g" stroke="%s" stroke-width="2.5" '
            'stroke-linecap="round"/>' % (cx - s, cy, cx + s, cx, cy - s, cy + s, NAVY))


# --- Composicion de cada bloque -------------------------------------------
# clave = nombre del fichero (slug). Valor = funcion que devuelve el dibujo.

def _hero():
    return (frame() + imgbox(20, 24, 130, 132) + title_line(166, 46, 118) +
            lines(166, 70, 118, 3) + btn(166, 116))


def _hero_fullscreen():
    return (imgbox(6, 6, W - 12, H - 12, r=10) +
            solid(80, 62, 160, 12, r=5, fill=NAVY) + lines(96, 88, 128, 2) +
            btn(132, 122))


def _carousel_featured():
    return frame() + imgbox(20, 22, W - 40, 108) + dots(W / 2, 152, 3, 0)


def _page_header():
    return (frame() + solid(20, 34, 60, 6) + title_line(20, 56, 150, 12) +
            lines(20, 84, 190, 1) + solid(20, 120, W - 40, 1.5, r=0, fill=MUTE))


def _welcome_video():
    return frame() + imgbox(20, 24, W - 40, 132) + play(W / 2, 90, 18)


def _title():
    return frame() + title_line(60, 78, 200, 14)


def _text():
    return frame() + lines(30, 52, 260, 6, gap=15)


def _text_image():
    return frame() + lines(20, 50, 130, 5, gap=14) + imgbox(170, 30, 130, 120)


def _text_image_alt():
    return frame() + imgbox(20, 30, 130, 120) + lines(170, 50, 130, 5, gap=14)


def _article_body():
    return (frame() + title_line(20, 26, 150, 11) + lines(20, 52, 280, 4, gap=13) +
            imgbox(20, 108, 130, 52) + lines(166, 110, 130, 3, gap=13))


def _seo_text():
    return frame() + lines(24, 34, 272, 8, gap=15, h=5)


def _pull_quote():
    return (frame() + solid(26, 50, 8, 80, r=4, fill=GOLD) +
            lines(52, 58, 220, 3, gap=18, h=8) + solid(52, 128, 90, 6))


def _full_width_band():
    return (frame() + solid(6, 52, W - 12, 76, r=0, fill=NAVY) +
            solid(70, 74, 180, 10, r=4, fill="#FFFFFF") +
            solid(102, 96, 116, 6, r=3, fill="#8FA9BF"))


def _spacer():
    return (frame() + '<path d="M40 90 H280" stroke="%s" stroke-width="3" '
            'stroke-dasharray="10 10" stroke-linecap="round"/>' % MUTE)


def _kpis():
    out = [frame()]
    for i in range(3):
        x = 30 + i * 90
        out.append(title_line(x, 62, 54, 16))
        out.append(solid(x, 90, 54, 6))
    return "".join(out)


def _why_us():
    out = [frame()]
    for i in range(3):
        x = 34 + i * 88
        out.append(ring(x + 26, 62, 15))
        out.append(solid(x, 92, 52, 7, fill=NAVY))
        out.append(lines(x, 110, 52, 2, gap=11, h=5))
    return "".join(out)


def _benefits_band():
    out = [frame(), solid(6, 56, W - 12, 68, r=0, fill=LIGHT)]
    for i in range(4):
        x = 30 + i * 70
        out.append(circle(x + 12, 78, 9))
        out.append(solid(x, 98, 44, 6))
    return "".join(out)


def _features_icons():
    out = [frame()]
    for r in range(2):
        for c in range(2):
            x, y = 30 + c * 140, 42 + r * 62
            out.append(ring(x + 12, y + 12, 12))
            out.append(solid(x + 34, y + 4, 86, 7, fill=NAVY))
            out.append(solid(x + 34, y + 18, 60, 5))
    return "".join(out)


def _timeline():
    out = [frame(), '<path d="M30 92 H290" stroke="%s" stroke-width="3"/>' % MUTE]
    for i in range(4):
        x = 42 + i * 78
        out.append(circle(x, 92, 8, GOLD if i == 0 else NAVY))
        out.append(solid(x - 22, 112, 44, 6))
    return "".join(out)


def _testimonials():
    return (frame() + box(30, 34, 260, 92, r=10, fill=LIGHT) +
            circle(58, 62, 13) + solid(82, 52, 90, 7, fill=NAVY) +
            lines(56, 84, 208, 2, gap=12) + dots(W / 2, 148, 3, 1))


def _google_reviews():
    out = [frame()]
    for i in range(5):
        out.append(star(70 + i * 36, 62, 11))
    out.append(lines(70, 92, 180, 2, gap=13))
    out.append(solid(70, 128, 80, 6))
    return "".join(out)


def _logo_carousel():
    out = [frame(), arrows(90)]
    for i in range(4):
        out.append(box(46 + i * 58, 70, 46, 40, r=6, fill=LIGHT, sw=2.5))
    return "".join(out)


def _certifications():
    out = [frame()]
    for i in range(4):
        cx = 62 + i * 66
        out.append(ring(cx, 84, 22))
        out.append(circle(cx, 84, 8, GOLD if i == 0 else MUTE))
    return "".join(out)


def _team_showcase():
    out = [frame()]
    for i in range(3):
        x = 46 + i * 80
        out.append(imgbox(x, 32, 56, 62))
        out.append(solid(x, 104, 56, 7, fill=NAVY))
        out.append(solid(x + 8, 118, 40, 5))
    return "".join(out)


def _case_studies():
    out = [frame()]
    for i in range(2):
        x = 26 + i * 140
        out.append(imgbox(x, 28, 128, 68))
        out.append(solid(x, 106, 100, 7, fill=NAVY))
        out.append(lines(x, 122, 128, 2, gap=11, h=5))
    return "".join(out)


def _solution_selector():
    out = [frame(), solid(60, 40, 200, 8, r=4, fill=NAVY)]
    for i in range(3):
        x = 30 + i * 90
        out.append(box(x, 68, 74, 46, r=8, fill=LIGHT if i != 1 else "none",
                       stroke=GOLD if i == 1 else NAVY))
        out.append(solid(x + 14, 88, 46, 6))
    out.append(btn(132, 130))
    return "".join(out)


def _cpt_showcase():
    out = [frame()]
    for i in range(3):
        x = 26 + i * 92
        out.append(imgbox(x, 30, 80, 62))
        out.append(solid(x, 102, 60, 7, fill=NAVY))
        out.append(solid(x, 116, 80, 5))
    return "".join(out)


def _cpt_list():
    out = [frame(), box(20, 26, 66, 128, r=8, fill=LIGHT, sw=2.5)]
    for i in range(4):
        out.append(solid(30, 40 + i * 22, 46, 7))
    for i in range(3):
        y = 30 + i * 40
        out.append(imgbox(100, y, 44, 32))
        out.append(solid(154, y + 4, 100, 7, fill=NAVY))
        out.append(solid(154, y + 18, 70, 5))
    out.append(dots(200, 158, 3, 0, r=4, gap=14))
    return "".join(out)


def _cpt_detail():
    return (frame() + imgbox(20, 26, 128, 128) + title_line(164, 34, 120) +
            lines(164, 58, 130, 3) + solid(164, 104, 60, 10, r=4, fill=NAVY) +
            btn(164, 126))


def _spec_sheet():
    out = [frame(), solid(20, 26, W - 40, 10, r=4, fill=NAVY)]
    for i in range(5):
        y = 50 + i * 22
        out.append(solid(20, y, 110, 6))
        out.append(solid(150, y, 150, 6, fill=LIGHT))
    return "".join(out)


def _card_grid():
    return frame() + grid(20, 26, W - 40, 128, 3, 2)


def _category_grid():
    out = [frame()]
    for r in range(2):
        for c in range(2):
            x, y = 24 + c * 144, 26 + r * 66
            out.append(imgbox(x, y, 128, 52))
            out.append(solid(x, y + 56, 70, 6))
    return "".join(out)


def _related_items():
    out = [frame(), solid(20, 26, 110, 8, r=4, fill=NAVY), arrows(100)]
    for i in range(3):
        x = 40 + i * 84
        out.append(imgbox(x, 50, 70, 60))
        out.append(solid(x, 118, 52, 6))
    return "".join(out)


def _shop_catalog():
    return (frame() + box(20, 26, 60, 128, r=8, fill=LIGHT, sw=2.5) +
            lines(28, 40, 44, 4, gap=18, h=6) + grid(94, 26, 206, 128, 3, 2, img=True))


def _product_category():
    return (frame() + imgbox(20, 22, W - 40, 44) + grid(20, 76, W - 40, 78, 3, 1, img=True))


def _product_detail():
    return (frame() + imgbox(20, 26, 120, 128) + lines(156, 34, 130, 2, gap=13) +
            title_line(156, 70, 70, 14) + btn(156, 100, 80, 20) +
            lines(156, 132, 130, 1, h=5))


def _product_carousel():
    out = [frame(), arrows(94)]
    for i in range(3):
        x = 42 + i * 82
        out.append(imgbox(x, 40, 68, 66))
        out.append(solid(x, 114, 44, 6))
        out.append(solid(x, 126, 30, 6, fill=NAVY))
    return "".join(out)


def _search_featured():
    return (frame() + box(30, 72, 200, 34, r=17, sw=3) + circle(52, 89, 6, MUTE) +
            solid(68, 86, 120, 6) + btn(240, 74, 50, 30))


def _cart():
    out = [frame()]
    for i in range(3):
        y = 30 + i * 34
        out.append(imgbox(20, y, 40, 28))
        out.append(solid(70, y + 4, 100, 6))
        out.append(solid(70, y + 16, 60, 5))
        out.append(solid(190, y + 10, 30, 6, fill=NAVY))
    out.append(box(238, 30, 62, 96, r=8, fill=LIGHT, sw=2.5))
    out.append(solid(248, 44, 42, 6))
    out.append(btn(248, 96, 42, 18))
    return "".join(out)


def _checkout():
    out = [frame()]
    for i in range(4):
        out.append(box(20, 28 + i * 30, 170, 22, r=5, sw=2.5))
    out.append(box(206, 28, 94, 96, r=8, fill=LIGHT, sw=2.5))
    out.append(lines(216, 42, 74, 3, gap=14, h=5))
    out.append(btn(206, 132, 94, 20))
    return "".join(out)


def _my_account():
    out = [frame(), box(20, 26, 76, 128, r=8, fill=LIGHT, sw=2.5)]
    for i in range(4):
        out.append(solid(30, 42 + i * 24, 56, 7))
    out.append(circle(140, 52, 16))
    out.append(solid(166, 46, 90, 7, fill=NAVY))
    out.append(lines(112, 88, 188, 3, gap=16))
    return "".join(out)


def _gallery_grid():
    return frame() + grid(20, 26, W - 40, 128, 3, 2, img=True)


def _gallery_carousel():
    return frame() + imgbox(46, 30, 228, 104) + arrows(82) + dots(W / 2, 152, 4, 1)


def _video_gallery():
    out = [frame()]
    for i in range(3):
        x = 26 + i * 92
        out.append(imgbox(x, 44, 80, 62))
        out.append(play(x + 40, 75, 12))
    return "".join(out)


def _video_fullwidth():
    return imgbox(6, 6, W - 12, H - 12, r=10) + play(W / 2, H / 2, 22)


def _video_text():
    return (frame() + imgbox(20, 34, 150, 112) + play(95, 90, 16) +
            lines(188, 52, 108, 4, gap=15))


def _image_compare():
    return (frame() + imgbox(20, 26, 128, 128) + imgbox(172, 26, 128, 128) +
            '<path d="M160 26 V154" stroke="%s" stroke-width="3"/>' % NAVY +
            circle(160, 90, 11, GOLD))


def _latest_news():
    out = [frame()]
    for i in range(3):
        x = 26 + i * 92
        out.append(imgbox(x, 26, 80, 54))
        out.append(solid(x, 88, 40, 5, fill=GOLD))
        out.append(solid(x, 100, 80, 7, fill=NAVY))
        out.append(lines(x, 114, 80, 2, gap=11, h=5))
    return "".join(out)


def _news_list():
    out = [frame()]
    for i in range(3):
        y = 28 + i * 42
        out.append(imgbox(20, y, 56, 34))
        out.append(solid(88, y + 2, 40, 5, fill=GOLD))
        out.append(solid(88, y + 14, 180, 7, fill=NAVY))
        out.append(solid(88, y + 26, 130, 5))
    return "".join(out)


def _cta_banner():
    return (frame() + solid(6, 58, W - 12, 64, r=0, fill=NAVY) +
            solid(30, 76, 140, 10, r=4, fill="#FFFFFF") +
            solid(30, 94, 100, 6, r=3, fill="#8FA9BF") + btn(216, 78, 70, 24))


def _cta_featured():
    return (imgbox(6, 6, W - 12, H - 12, r=10) + box(24, 34, 150, 112, r=10,
            fill="#FFFFFF", sw=0) + title_line(40, 52, 110) +
            lines(40, 76, 118, 2, gap=13) + btn(40, 110))


def _call_to_action():
    return (frame() + title_line(80, 56, 160, 12) + lines(90, 80, 140, 1) +
            btn(132, 108, 56, 22))


def _promo_banner():
    return (frame() + box(20, 50, W - 40, 80, r=10, fill=LIGHT) +
            solid(36, 66, 44, 16, r=8, fill=GOLD) + solid(36, 92, 150, 8, fill=NAVY) +
            btn(224, 78, 60, 24))


def _popup_form():
    return (frame() + '<rect x="6" y="6" width="%g" height="%g" rx="10" '
            'fill="%s" opacity="0.55"/>' % (W - 12, H - 12, NAVY) +
            box(76, 34, 168, 112, r=10, fill="#FFFFFF", sw=0) +
            solid(92, 50, 100, 8, fill=NAVY) +
            box(92, 70, 136, 18, r=5, sw=2) + box(92, 94, 136, 18, r=5, sw=2) +
            btn(92, 118, 60, 18))


def _dynamic_form():
    out = [frame()]
    for i in range(3):
        out.append(box(30, 32 + i * 30, 260, 22, r=5, sw=2.5))
    out.append(box(30, 122, 124, 22, r=5, sw=2.5))
    out.append(btn(178, 122, 112, 22))
    return "".join(out)


def _contact_methods():
    out = [frame()]
    for i in range(3):
        x = 34 + i * 88
        out.append(ring(x + 26, 66, 16))
        out.append(solid(x, 96, 52, 7, fill=NAVY))
        out.append(solid(x + 6, 110, 40, 5))
    return "".join(out)


def _map():
    return (frame() + box(20, 26, W - 40, 128, r=8, fill=LIGHT, sw=2.5) +
            '<path d="M20 110 L110 70 L190 120 L280 62" stroke="%s" '
            'stroke-width="2.5" fill="none" opacity="0.5"/>' % NAVY +
            circle(160, 84, 12, GOLD) + circle(160, 84, 5, NAVY))


def _newsletter():
    return (frame() + solid(60, 52, 200, 9, r=4, fill=NAVY) +
            box(40, 84, 170, 30, r=15, sw=3) + solid(58, 95, 96, 7) +
            btn(220, 86, 60, 26))


def _app_download():
    return (frame() + box(30, 26, 74, 128, r=10, sw=3) + circle(67, 142, 4, MUTE) +
            solid(42, 40, 50, 84, r=4, fill=LIGHT) +
            box(130, 54, 160, 32, r=8, fill=LIGHT, sw=2.5) +
            box(130, 96, 160, 32, r=8, fill=LIGHT, sw=2.5))


def _tabs_accordion():
    out = [frame(), solid(20, 28, 84, 20, r=5, fill=NAVY)]
    for i in range(2):
        out.append(box(112 + i * 90, 28, 84, 20, r=5, sw=2.5))
    out.append(box(20, 60, W - 40, 94, r=8, fill=LIGHT, sw=2.5))
    out.append(lines(34, 78, 250, 4, gap=16))
    return "".join(out)


def _faq_accordion():
    out = [frame()]
    for i in range(4):
        y = 28 + i * 32
        out.append(box(20, y, W - 40, 24, r=6, sw=2.5,
                       fill=LIGHT if i == 0 else "none"))
        out.append(solid(34, y + 9, 150, 6))
        out.append(plus(276, y + 12))
    return "".join(out)


def _steps_process():
    out = [frame(), '<path d="M46 78 H274" stroke="%s" stroke-width="3"/>' % MUTE]
    for i in range(4):
        x = 46 + i * 76
        out.append(circle(x, 78, 14, GOLD if i == 0 else NAVY))
        out.append(solid(x - 24, 106, 48, 6))
        out.append(solid(x - 16, 120, 32, 5))
    return "".join(out)


def _downloads():
    out = [frame()]
    for i in range(3):
        y = 34 + i * 40
        out.append(box(20, y, W - 40, 30, r=6, sw=2.5))
        out.append(solid(34, y + 8, 16, 14, r=3, fill=NAVY))
        out.append(solid(60, y + 12, 140, 6))
        out.append(circle(280, y + 15, 8, GOLD))
    return "".join(out)


def _pricing_plans():
    out = [frame()]
    for i in range(3):
        x = 24 + i * 92
        dest = (i == 1)
        out.append(box(x, 24, 80, 132, r=8, sw=3,
                       stroke=GOLD if dest else NAVY,
                       fill=LIGHT if dest else "none"))
        out.append(solid(x + 14, 38, 52, 6))
        out.append(title_line(x + 18, 54, 44, 14))
        out.append(lines(x + 14, 82, 52, 3, gap=12, h=5))
        out.append(btn(x + 14, 126, 52, 16))
    return "".join(out)


BLOCKS = {
    # Portada y cabeceras
    "hero-banner": _hero,
    "hero-fullscreen": _hero_fullscreen,
    "carousel-featured": _carousel_featured,
    "page-header": _page_header,
    "welcome-video": _welcome_video,
    # Contenido base
    "title": _title,
    "text": _text,
    "text-image": _text_image,
    "text-image-alt": _text_image_alt,
    "article-body": _article_body,
    "seo-text": _seo_text,
    "pull-quote": _pull_quote,
    "full-width-band": _full_width_band,
    "spacer": _spacer,
    # Confianza y marca
    "kpis": _kpis,
    "why-us": _why_us,
    "benefits-band": _benefits_band,
    "features-icons": _features_icons,
    "timeline": _timeline,
    "testimonials": _testimonials,
    "google-reviews": _google_reviews,
    "logo-carousel": _logo_carousel,
    "certifications": _certifications,
    "team-showcase": _team_showcase,
    "case-studies": _case_studies,
    # Contenidos gestionables (CPT)
    "solution-selector": _solution_selector,
    "cpt-showcase": _cpt_showcase,
    "cpt-list": _cpt_list,
    "cpt-detail": _cpt_detail,
    "spec-sheet": _spec_sheet,
    "card-grid": _card_grid,
    "category-grid": _category_grid,
    "related-items": _related_items,
    # Tienda (WooCommerce)
    "shop-catalog": _shop_catalog,
    "product-category": _product_category,
    "product-detail": _product_detail,
    "product-carousel": _product_carousel,
    "search-featured": _search_featured,
    "cart": _cart,
    "checkout": _checkout,
    "my-account": _my_account,
    # Multimedia
    "gallery-grid": _gallery_grid,
    "gallery-carousel": _gallery_carousel,
    "video-gallery": _video_gallery,
    "video-fullwidth": _video_fullwidth,
    "video-text": _video_text,
    "image-compare": _image_compare,
    # Blog
    "latest-news": _latest_news,
    "news-list": _news_list,
    # Conversion y contacto
    "cta-banner": _cta_banner,
    "cta-featured": _cta_featured,
    "call-to-action": _call_to_action,
    "promo-banner": _promo_banner,
    "popup-form": _popup_form,
    "dynamic-form": _dynamic_form,
    "contact-methods": _contact_methods,
    "map": _map,
    "newsletter": _newsletter,
    "app-download": _app_download,
    # Organizacion de la informacion
    "tabs-accordion": _tabs_accordion,
    "faq-accordion": _faq_accordion,
    "steps-process": _steps_process,
    "downloads": _downloads,
    "pricing-plans": _pricing_plans,
}

CABECERA = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
    'height="%d" role="img" aria-label="%s">\n'
    '  <!-- Generado por scripts/gen_blocks.py. No editar a mano. -->\n  '
)


def main(argv):
    DST.mkdir(parents=True, exist_ok=True)
    for slug, dibujar in sorted(BLOCKS.items()):
        svg = (CABECERA % (W, H, W, H, slug)) + dibujar() + "\n</svg>\n"
        (DST / (slug + ".svg")).write_text(svg, encoding="utf-8", newline="\n")
    print("Escritos %d SVG en %s" % (len(BLOCKS), DST.relative_to(ROOT)))
    print("Ahora: python scripts/make_blocks.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
