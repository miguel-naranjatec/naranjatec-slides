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

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "brand" / "assets" / "blocks"

W, H = 320, 180
NAVY = "#0B3D66"     # trazo principal (azul profundo de marca)
GOLD = "#FFCD33"     # acento: el elemento activo / la llamada a la accion
MUTE = "#C3CEDA"     # barras que sugieren texto
LIGHT = "#E9EEF3"    # rellenos suaves
SOFT = "#8FA9BF"     # texto sugerido SOBRE navy
WHITE = "#FFFFFF"


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
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


def plus(cx, cy, s=6):
    return ('<path d="M%g %g H%g M%g %g V%g" stroke="%s" stroke-width="2.5" '
            'stroke-linecap="round"/>' % (cx - s, cy, cx + s, cx, cy - s, cy + s, NAVY))


def dashed(x1, y1, x2, y2, color=MUTE, sw=2, dash="2 5"):
    return ('<path d="M%g %g L%g %g" stroke="%s" stroke-width="%g" '
            'stroke-dasharray="%s" stroke-linecap="round"/>'
            % (x1, y1, x2, y2, color, sw, dash))


def check(cx, cy, s=5, color=NAVY):
    return ('<path d="M%g %g L%g %g L%g %g" stroke="%s" stroke-width="2.5" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            % (cx - s, cy, cx - s * 0.15, cy + s * 0.8, cx + s, cy - s * 0.9, color))


def checkbox(x, y, on=False, s=13):
    out = [box(x, y, s, s, r=3, sw=2.5, fill=GOLD if on else "none")]
    if on:
        out.append(check(x + s / 2.0, y + s / 2.0, 3.4))
    return "".join(out)


def radio(cx, cy, on=False, r=6):
    out = [ring(cx, cy, r, sw=2.5)]
    if on:
        out.append(circle(cx, cy, r * 0.52, GOLD))
    return "".join(out)


def bar(x, base, w, h, fill=NAVY):
    """Barra de grafico anclada a su base (crece hacia arriba)."""
    return solid(x, base - h, w, h, r=2, fill=fill)


def donut(cx, cy, r, frac, sw=9, fill=GOLD):
    """Anillo gris con un arco de acento que cubre `frac` de la vuelta."""
    frac = max(0.02, min(frac, 0.999))
    a0 = -math.pi / 2
    a1 = a0 + 2 * math.pi * frac
    laf = 1 if frac > 0.5 else 0
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return ('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" '
            'stroke-width="%g"/>'
            '<path d="M%.1f %.1f A%g %g 0 %d 1 %.1f %.1f" fill="none" '
            'stroke="%s" stroke-width="%g" stroke-linecap="round"/>'
            % (cx, cy, r, LIGHT, sw, x0, y0, r, r, laf, x1, y1, fill, sw))


def slider(x, y, w, frac):
    return (solid(x, y - 2, w, 4, r=2, fill=LIGHT) +
            solid(x, y - 2, w * frac, 4, r=2, fill=NAVY) +
            circle(x + w * frac, y, 7, GOLD) + ring(x + w * frac, y, 7, sw=2.5))


def avatar(cx, cy, r=9):
    return circle(cx, cy, r, NAVY)


def chip(x, y, w, h=14, fill=LIGHT):
    return solid(x, y, w, h, r=h / 2.0, fill=fill)


def cal_grid(x, y, w, h, cols=7, rows=5, gap=5, active=(2, 3)):
    """Rejilla de dias de un mes. `active` es la celda (fila, columna) en dorado."""
    out = []
    cw = (w - (cols - 1) * gap) / cols
    ch = (h - (rows - 1) * gap) / rows
    for r in range(rows):
        for c in range(cols):
            fill = GOLD if (r, c) == active else LIGHT
            out.append(solid(x + c * (cw + gap), y + r * (ch + gap), cw, ch,
                             r=3, fill=fill))
    return "".join(out)


def wave(x, y, w, n=30, h=36):
    """Onda de audio: barras simetricas de altura variable pero determinista."""
    out = []
    bw = w / (n * 1.8)
    step = w / float(n)
    for i in range(n):
        a = abs(math.sin(i * 0.7)) * 0.75 + abs(math.sin(i * 0.23)) * 0.25
        hh = max(3.0, h * a)
        out.append(solid(x + i * step, y - hh / 2.0, bw, hh, r=bw / 2.0,
                         fill=NAVY if i < n * 0.45 else MUTE))
    return "".join(out)


def pin(cx, cy, r=7, fill=GOLD):
    return ('<path d="M%g %g L%g %g L%g %g Z" fill="%s"/>'
            % (cx - r * 0.6, cy + r * 0.55, cx + r * 0.6, cy + r * 0.55,
               cx, cy + r * 1.9, fill) +
            circle(cx, cy, r, fill) + circle(cx, cy, r * 0.36, NAVY))


def chevron(cx, cy, dirn="r", s=5, color=NAVY):
    if dirn in ("r", "l"):
        d = 1 if dirn == "r" else -1
        pts = ((cx - s * 0.5 * d, cy - s), (cx + s * 0.5 * d, cy),
               (cx - s * 0.5 * d, cy + s))
    else:
        d = 1 if dirn == "d" else -1
        pts = ((cx - s, cy - s * 0.5 * d), (cx, cy + s * 0.5 * d),
               (cx + s, cy - s * 0.5 * d))
    return ('<path d="M%g %g L%g %g L%g %g" stroke="%s" stroke-width="2.5" '
            'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            % (pts[0][0], pts[0][1], pts[1][0], pts[1][1],
               pts[2][0], pts[2][1], color))


def clipped(inner, uid="c"):
    """Recorta el dibujo al marco. Lo necesitan los bloques que sangran por el
    borde a proposito (cinta, scroll horizontal, pantalla partida)."""
    return ('<defs><clipPath id="%s"><rect x="6" y="6" width="%g" height="%g" '
            'rx="10"/></clipPath></defs><g clip-path="url(#%s)">%s</g>'
            % (uid, W - 12, H - 12, uid, inner))


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


# --- v2: navegacion y chrome ----------------------------------------------

def _nav_bar():
    out = [frame(), solid(20, 22, 42, 16, r=4, fill=NAVY)]
    for i in range(4):
        out.append(solid(84 + i * 38, 27, 28, 6))
    out.append(btn(250, 21, 50, 18))
    out.append(solid(6, 52, W - 12, 1.5, r=0, fill=MUTE))
    out.append(solid(20, 68, W - 40, 86, r=8, fill=LIGHT))
    return "".join(out)


def _mega_menu():
    out = [frame(), solid(20, 22, 42, 14, r=4, fill=NAVY)]
    for i in range(3):
        x = 84 + i * 56
        out.append(solid(x, 26, 34, 6, fill=NAVY if i == 1 else MUTE))
        if i == 1:
            out.append(chevron(x + 44, 29, "d", 4))
    out.append(box(56, 50, 244, 104, r=8, fill=WHITE, sw=2.5))
    for c in range(2):
        x = 70 + c * 66
        out.append(solid(x, 62, 48, 6, fill=NAVY))
        out.append(lines(x, 78, 48, 3, gap=13, h=5))
    out.append(imgbox(204, 62, 82, 80))
    return "".join(out)


def _footer_columns():
    top = imgbox(20, 22, 118, 54) + lines(152, 30, 148, 3, gap=13, h=5)
    band = [solid(6, 92, W - 12, 82, r=0, fill=NAVY)]
    for i in range(4):
        x = 24 + i * 72
        band.append(solid(x, 106, 34, 7, r=3, fill=WHITE))
        for j in range(3):
            band.append(solid(x, 122 + j * 11, 48, 5, r=2, fill=SOFT))
    band.append(solid(20, 158, W - 40, 1.5, r=0, fill=SOFT))
    return top + clipped("".join(band)) + frame()


def _table_of_contents():
    out = [frame(), solid(20, 26, 4, 106, r=2, fill=LIGHT),
           solid(20, 50, 4, 24, r=2, fill=GOLD)]
    for i in range(5):
        out.append(solid(34, 28 + i * 22, 64 - (i % 2) * 16, 6,
                         fill=NAVY if i == 1 else MUTE))
    out.append(title_line(122, 26, 118, 10))
    out.append(lines(122, 50, 178, 6, gap=14, h=5))
    return "".join(out)


def _cookie_consent():
    out = [frame(), imgbox(20, 22, 110, 74), lines(146, 30, 154, 4, gap=14, h=5)]
    out.append(box(16, 110, W - 32, 52, r=8, fill=WHITE, sw=2.5))
    out.append(solid(30, 122, 92, 6, fill=NAVY))
    out.append(solid(30, 138, 132, 5))
    out.append(box(186, 124, 54, 24, r=6, sw=2.5))
    out.append(btn(250, 124, 52, 24))
    return "".join(out)


# --- v2: reservas y horarios ----------------------------------------------

def _booking_calendar():
    out = [frame(), solid(20, 20, 64, 8, r=4, fill=NAVY),
           chevron(276, 24, "l", 4), chevron(298, 24, "r", 4)]
    for c in range(7):
        out.append(solid(31 + c * 40.7, 38, 14, 4))
    out.append(cal_grid(20, 50, 280, 104, active=(2, 3)))
    return "".join(out)


def _time_slots():
    ocupados = {(0, 2), (1, 0), (3, 3), (4, 1)}
    out = [frame()]
    for c in range(5):
        x = 22 + c * 58
        out.append(solid(x, 22, 44, 7, r=3, fill=NAVY))
        for r in range(4):
            if (c, r) == (2, 1):
                fill = GOLD
            elif (c, r) in ocupados:
                fill = MUTE
            else:
                fill = LIGHT
            out.append(chip(x, 42 + r * 28, 44, 20, fill=fill))
    return "".join(out)


def _opening_hours():
    out = [frame(), ring(74, 90, 40, sw=3),
           '<path d="M74 90 V66 M74 90 L92 100" stroke="%s" stroke-width="3" '
           'stroke-linecap="round" fill="none"/>' % NAVY,
           circle(74, 90, 4, GOLD)]
    for i in range(6):
        y = 30 + i * 21
        hoy = (i == 2)
        if hoy:
            out.append(solid(134, y - 5, 166, 20, r=5, fill=GOLD))
        out.append(solid(146, y + 2, 54, 6, fill=NAVY if hoy else MUTE))
        out.append(solid(232, y + 2, 56, 6, fill=NAVY if hoy else MUTE))
    return "".join(out)


def _multi_step_form():
    out = [frame(),
           '<path d="M40 30 H280" stroke="%s" stroke-width="2.5"/>' % MUTE]
    for i in range(4):
        out.append(circle(40 + i * 80, 30, 11, GOLD if i == 0 else NAVY))
    for i in range(3):
        out.append(box(20, 58 + i * 32, 168, 24, r=5, sw=2.5))
    out.append(box(202, 58, 98, 88, r=8, fill=LIGHT, sw=2.5))
    out.append(lines(214, 72, 74, 3, gap=14, h=5))
    out.append(btn(214, 120, 74, 18))
    return "".join(out)


# --- v2: configuracion y precio -------------------------------------------

def _price_calculator():
    out = [frame()]
    for i, f in enumerate((0.35, 0.62, 0.8)):
        y = 44 + i * 38
        out.append(solid(20, y - 20, 58, 6))
        out.append(slider(20, y, 150, f))
    out.append(box(196, 30, 104, 118, r=8, fill=LIGHT, sw=2.5))
    out.append(solid(210, 44, 40, 5))
    out.append(title_line(210, 58, 76, 18))
    out.append(lines(210, 88, 76, 2, gap=12, h=5))
    out.append(btn(210, 118, 76, 18))
    return "".join(out)


def _product_configurator():
    out = [frame(), imgbox(20, 26, 140, 128), solid(176, 30, 58, 6)]
    for i in range(5):
        cx = 186 + i * 26
        out.append(circle(cx, 56, 10, GOLD if i == 1 else MUTE))
        if i == 1:
            out.append(ring(cx, 56, 14, sw=2.5))
    out.append(solid(176, 84, 44, 6))
    for i in range(4):
        out.append(chip(176 + i * 32, 96, 26, 20,
                        fill=NAVY if i == 2 else LIGHT))
    out.append(btn(176, 130, 124, 22))
    return "".join(out)


# --- v2: datos ------------------------------------------------------------

def _stats_chart():
    out = [frame(),
           '<path d="M30 140 H296 M30 140 V32" stroke="%s" stroke-width="2.5" '
           'fill="none" stroke-linecap="round"/>' % MUTE]
    alturas = (38, 62, 50, 84, 70, 96)
    for i, hh in enumerate(alturas):
        x = 44 + i * 42
        out.append(bar(x, 138, 26, hh, GOLD if i == len(alturas) - 1 else NAVY))
        out.append(solid(x + 2, 150, 22, 5))
    return "".join(out)


def _donut_stats():
    out = [frame()]
    for i, f in enumerate((0.72, 0.45, 0.9)):
        cx = 66 + i * 94
        out.append(donut(cx, 76, 30, f))
        out.append(solid(cx - 26, 122, 52, 7, r=3, fill=NAVY))
        out.append(solid(cx - 18, 136, 36, 5))
    return "".join(out)


def _progress_bars():
    out = [frame()]
    for i, f in enumerate((0.85, 0.6, 0.72, 0.4)):
        y = 40 + i * 30
        out.append(solid(20, y - 12, 56, 6))
        out.append(solid(20, y, 280, 10, r=5, fill=LIGHT))
        out.append(solid(20, y, 280 * f, 10, r=5, fill=GOLD if i == 0 else NAVY))
    return "".join(out)


def _data_table():
    out = [frame(), solid(20, 24, 280, 22, r=5, fill=NAVY)]
    for c in range(4):
        out.append(solid(32 + c * 68, 31, 44, 6, r=3, fill=WHITE))
    for r in range(4):
        y = 52 + r * 22
        if r % 2 == 0:
            out.append(solid(20, y, 280, 20, r=3, fill=LIGHT))
        for c in range(4):
            out.append(solid(32 + c * 68, y + 7, 28 if c == 3 else 44, 6))
    out.append(dots(266, 152, 3, 0, r=4, gap=14))
    return "".join(out)


def _comparison_table():
    out = [frame(), solid(181, 20, 62, 138, r=8, fill=LIGHT)]
    for c in range(3):
        out.append(solid(130 + c * 62, 28, 40, 7, r=3, fill=NAVY))
    for r in range(4):
        y = 54 + r * 24
        out.append(solid(20, y + 3, 96, 6))
        for c in range(3):
            cx = 150 + c * 62
            if c == 0 and r > 1:
                out.append(circle(cx, y + 6, 5, MUTE))
            else:
                out.append(check(cx, y + 6, 6, GOLD if c == 1 else NAVY))
    return "".join(out)


# --- v2: inmobiliaria -----------------------------------------------------

def _property_map_list():
    out = [frame()]
    for i in range(3):
        y = 26 + i * 44
        out.append(box(18, y, 130, 38, r=6, sw=2.5,
                       fill=LIGHT if i == 0 else "none"))
        out.append(imgbox(24, y + 6, 34, 26, r=4))
        out.append(solid(66, y + 9, 66, 6, fill=NAVY))
        out.append(solid(66, y + 21, 44, 5))
    out.append(box(160, 26, 140, 128, r=8, fill=LIGHT, sw=2.5))
    out.append('<path d="M160 112 L200 84 L240 118 L300 74" stroke="%s" '
               'stroke-width="2.5" fill="none" opacity="0.5"/>' % NAVY)
    out.append(pin(246, 100, 6, NAVY))
    out.append(pin(282, 62, 6, NAVY))
    out.append(pin(196, 70))
    return "".join(out)


def _floor_plan():
    # Tres estancias, tabiques con hueco de puerta y arco de barrido, y una cota
    # arriba. Sin el arco y los huecos, un plano es indistinguible de dos cajas.
    out = [frame(), solid(30, 36, 138, 114, r=2, fill=LIGHT),
           solid(172, 102, 118, 48, r=2, fill=LIGHT),
           box(28, 34, 264, 118, r=3, sw=4)]
    out.append(solid(168, 34, 4, 42, r=0, fill=NAVY))
    out.append(solid(168, 96, 4, 56, r=0, fill=NAVY))
    out.append('<path d="M170 96 A20 20 0 0 0 190 76" stroke="%s" '
               'stroke-width="2" fill="none" stroke-dasharray="3 3"/>' % NAVY)
    out.append(solid(172, 98, 26, 4, r=0, fill=NAVY))
    out.append(solid(228, 98, 62, 4, r=0, fill=NAVY))
    out.append(circle(213, 100, 4, GOLD))
    out.append(dashed(28, 24, 292, 24))
    out.append(solid(28, 19, 2, 10, r=0, fill=MUTE))
    out.append(solid(290, 19, 2, 10, r=0, fill=MUTE))
    return "".join(out)


# --- v2: restauracion -----------------------------------------------------

def _menu_carta():
    out = [frame()]
    for c in range(2):
        x = 22 + c * 146
        out.append(solid(x, 24, 52, 7, r=3, fill=GOLD))
        for r in range(4):
            y = 44 + r * 27
            out.append(solid(x, y, 56 - r * 4, 6, fill=NAVY))
            out.append(dashed(x + 64, y + 3, x + 104, y + 3))
            out.append(solid(x + 110, y, 20, 6))
            out.append(solid(x, y + 11, 74, 4))
    return "".join(out)


# --- v2: formacion --------------------------------------------------------

def _lesson_player():
    out = [frame(), imgbox(20, 26, 180, 104), play(110, 74, 18),
           solid(20, 138, 180, 6, r=3, fill=LIGHT),
           solid(20, 138, 108, 6, r=3, fill=GOLD)]
    for i in range(5):
        y = 28 + i * 25
        act = (i == 1)
        if act:
            out.append(solid(208, y - 4, 94, 24, r=5, fill=LIGHT))
        out.append(circle(222, y + 8, 7, GOLD if act else (NAVY if not i else MUTE)))
        if i == 0:
            out.append(check(222, y + 8, 3.4, WHITE))
        out.append(solid(238, y + 5, 54, 6, fill=NAVY if act else MUTE))
    return "".join(out)


def _quiz():
    out = [frame(), solid(20, 22, 280, 6, r=3, fill=LIGHT),
           solid(20, 22, 168, 6, r=3, fill=GOLD),
           solid(20, 40, 190, 8, r=4, fill=NAVY), solid(20, 56, 130, 6)]
    for i in range(3):
        y = 74 + i * 28
        sel = (i == 1)
        out.append(box(20, y, 280, 22, r=6, sw=2.5,
                       fill=LIGHT if sel else "none"))
        out.append(radio(36, y + 11, sel))
        out.append(solid(52, y + 8, 120 + i * 20, 6))
    return "".join(out)


# --- v2: eventos ----------------------------------------------------------

def _event_countdown():
    out = [frame(), solid(94, 26, 132, 9, r=4, fill=NAVY)]
    for i in range(4):
        x = 26 + i * 72
        out.append(solid(x, 52, 58, 56, r=8, fill=LIGHT))
        out.append(title_line(x + 13, 66, 32, 16))
        out.append(solid(x + 15, 90, 28, 5))
        if i < 3:
            out.append(circle(x + 66, 72, 2.5, NAVY))
            out.append(circle(x + 66, 86, 2.5, NAVY))
    out.append(btn(132, 126, 56, 22))
    return "".join(out)


def _event_agenda():
    out = [frame(), '<path d="M76 24 V154" stroke="%s" stroke-width="2.5"/>' % MUTE]
    y = 26
    for i, hh in enumerate((30, 44, 24)):
        out.append(solid(22, y + 6, 40, 6))
        out.append(circle(76, y + 12, 6, GOLD if i == 1 else NAVY))
        out.append(box(94, y, 206, hh, r=6, sw=2.5,
                       fill=LIGHT if i == 1 else "none"))
        out.append(solid(106, y + 9, 110, 6, fill=NAVY))
        if hh > 34:
            out.append(solid(106, y + 24, 150, 5))
        y += hh + 14
    return "".join(out)


# --- v2: comercio ---------------------------------------------------------

def _product_zoom():
    out = [frame()]
    for i in range(4):
        out.append(imgbox(20, 26 + i * 34, 34, 28, r=4))
    out.append(box(18, 58, 38, 32, r=5, sw=2.5, stroke=GOLD))
    out.append(imgbox(66, 26, 234, 128))
    out.append('<path d="M238 110 L262 134" stroke="%s" stroke-width="6" '
               'stroke-linecap="round"/>' % NAVY)
    out.append(circle(220, 92, 26, WHITE))
    out.append(ring(220, 92, 26, sw=3))
    out.append(plus(220, 92, 7))
    return "".join(out)


def _size_guide():
    out = [frame(), circle(56, 40, 11),
           '<path d="M56 54 C40 60 36 76 38 96 L44 140 M56 54 C72 60 76 76 74 96 '
           'L68 140" stroke="%s" stroke-width="3" fill="none" '
           'stroke-linecap="round"/>' % NAVY,
           dashed(28, 76, 86, 76, GOLD, 2, "3 4"),
           dashed(28, 106, 86, 106, GOLD, 2, "3 4"),
           solid(112, 26, 188, 18, r=4, fill=NAVY)]
    for c in range(3):
        out.append(solid(124 + c * 62, 32, 38, 6, r=3, fill=WHITE))
    for r in range(4):
        y = 50 + r * 26
        if r % 2 == 0:
            out.append(solid(112, y, 188, 20, r=3, fill=LIGHT))
        for c in range(3):
            out.append(solid(124 + c * 62, y + 7, 38, 6))
    return "".join(out)


def _seat_picker():
    ocupados = {(0, 2), (1, 5), (2, 1), (3, 6), (1, 8)}
    sel = {(2, 4), (2, 5)}
    out = [frame(), '<path d="M64 42 Q160 20 256 42" stroke="%s" '
           'stroke-width="5" fill="none" stroke-linecap="round"/>' % NAVY]
    for r in range(4):
        for c in range(9):
            x = 62 + c * 24
            y = 62 + r * 21 + abs(c - 4) * 1.6
            if (r, c) in sel:
                fill = GOLD
            elif (r, c) in ocupados:
                fill = MUTE
            else:
                fill = LIGHT
            out.append(solid(x, y, 17, 14, r=4, fill=fill))
    for i, f in enumerate((LIGHT, GOLD, MUTE)):
        x = 66 + i * 76
        out.append(solid(x, 158, 14, 11, r=3, fill=f))
        out.append(solid(x + 20, 161, 34, 5))
    return "".join(out)


# --- v2: comunidad y conversacion -----------------------------------------

def _comments_thread():
    out = [frame()]
    for x, y, w, h in ((20, 24, 252, 40), (58, 72, 224, 38), (20, 118, 252, 32)):
        out.append(avatar(x + 11, y + 12))
        out.append(box(x + 28, y, w, h, r=8, sw=2.5))
        out.append(solid(x + 40, y + 9, 58, 6, fill=NAVY))
        out.append(solid(x + 40, y + 23, w - 60, 5))
    return "".join(out)


def _chat_panel():
    out = [frame(), avatar(30, 32), solid(48, 24, 78, 7, r=3, fill=NAVY),
           solid(48, 38, 48, 5), solid(6, 54, W - 12, 1.5, r=0, fill=MUTE),
           solid(20, 66, 142, 28, r=12, fill=LIGHT),
           solid(34, 76, 92, 6), solid(158, 102, 142, 28, r=12, fill=GOLD),
           solid(172, 112, 92, 6, fill=NAVY),
           box(20, 140, 240, 26, r=13, sw=2.5), solid(38, 150, 88, 5),
           circle(286, 153, 14, GOLD), chevron(286, 153, "r", 5)]
    return "".join(out)


def _ratings_breakdown():
    out = [frame(), title_line(24, 40, 64, 26)]
    for i in range(5):
        out.append(star(30 + i * 15, 84, 6))
    out.append(solid(24, 100, 64, 5))
    for i, f in enumerate((0.72, 0.16, 0.06, 0.03, 0.03)):
        y = 34 + i * 26
        out.append(star(118, y + 4, 6))
        out.append(solid(134, y, 142, 8, r=4, fill=LIGHT))
        out.append(solid(134, y, 142 * f, 8, r=4, fill=NAVY if i else GOLD))
        out.append(solid(286, y + 1, 14, 6))
    return "".join(out)


def _ai_search():
    out = [frame(), box(20, 22, 280, 30, r=15, sw=3), star(40, 37, 8),
           solid(58, 34, 148, 6), btn(246, 26, 44, 22),
           solid(20, 66, 280, 60, r=8, fill=LIGHT),
           lines(32, 78, 250, 3, gap=14, h=5)]
    for i in range(3):
        out.append(chip(20 + i * 76, 138, 66, 18))
        out.append(solid(32 + i * 76, 145, 42, 5, fill=NAVY))
    return "".join(out)


# --- v2: medios e interaccion ---------------------------------------------

def _audio_player():
    out = [frame(), play(46, 88, 22), wave(84, 88, 176, n=26, h=48),
           solid(272, 82, 28, 6), solid(20, 146, 280, 6, r=3, fill=LIGHT),
           solid(20, 146, 120, 6, r=3, fill=GOLD), circle(140, 149, 7, NAVY)]
    return "".join(out)


def _hotspot_image():
    out = [frame(), imgbox(20, 24, 180, 130)]
    for cx, cy in ((60, 62), (112, 120), (166, 52)):
        out.append(circle(cx, cy, 9, GOLD))
        out.append(circle(cx, cy, 3.5, NAVY))
    out.append(dashed(166, 52, 212, 52, NAVY, 2, "3 4"))
    out.append(box(212, 34, 88, 66, r=8, fill=WHITE, sw=2.5))
    out.append(solid(224, 46, 52, 6, fill=NAVY))
    out.append(lines(224, 62, 64, 2, gap=12, h=5))
    return "".join(out)


def _file_upload():
    out = [frame(),
           '<rect x="20" y="22" width="280" height="94" rx="10" fill="%s" '
           'stroke="%s" stroke-width="3" stroke-dasharray="9 8"/>' % (LIGHT, NAVY),
           '<path d="M160 84 V48 M146 62 L160 46 L174 62" stroke="%s" '
           'stroke-width="3.5" fill="none" stroke-linecap="round" '
           'stroke-linejoin="round"/>' % NAVY,
           solid(122, 94, 76, 6),
           box(20, 128, 280, 30, r=6, sw=2.5),
           solid(32, 137, 15, 13, r=2, fill=NAVY),
           solid(58, 136, 82, 5), solid(58, 148, 152, 5, r=2, fill=LIGHT),
           solid(58, 148, 98, 5, r=2, fill=GOLD),
           circle(282, 143, 8, NAVY), check(282, 143, 3.6, WHITE)]
    return "".join(out)


# --- v2: estructuras ------------------------------------------------------

def _bento_grid():
    return (frame() + imgbox(20, 26, 148, 82) + box(176, 26, 60, 82, r=6, sw=2.5) +
            imgbox(244, 26, 56, 40) + box(244, 74, 56, 34, r=6, sw=2.5) +
            box(20, 116, 88, 38, r=6, sw=2.5) + imgbox(116, 116, 184, 38))


def _masonry_grid():
    out = []
    for i, alturas in enumerate(((46, 66, 40), (76, 42, 58), (38, 58, 70),
                                 (62, 80, 36))):
        x, y = 20 + i * 72, 20
        for h in alturas:
            out.append(imgbox(x, y, 64, h))
            y += h + 8
    return clipped("".join(out)) + frame()


def _marquee_band():
    out = [title_line(96, 28, 128, 10), solid(6, 62, W - 12, 56, r=0, fill=LIGHT)]
    x, i = -18, 0
    while x < 330:
        w = 54 + (i % 3) * 22
        out.append(box(x, 78, w, 24, r=12, sw=2.5,
                       fill=GOLD if i % 3 == 1 else WHITE))
        x += w + 14
        i += 1
    out.append(lines(70, 132, 180, 2, gap=13, h=5))
    return clipped("".join(out)) + frame()


def _timeline_vertical():
    out = [frame(), '<path d="M160 20 V158" stroke="%s" stroke-width="3"/>' % MUTE]
    for i in range(4):
        cy = 34 + i * 36
        x = 30 if i % 2 == 0 else 178
        out.append(box(x, cy - 16, 112, 32, r=6, sw=2.5))
        out.append(solid(x + 12, cy - 8, 58, 6, fill=NAVY))
        out.append(solid(x + 12, cy + 2, 84, 5))
        out.append(circle(160, cy, 8, GOLD if i == 0 else NAVY))
    return "".join(out)


def _split_screen():
    inner = (solid(6, 6, W - 12, H - 12, r=0, fill=NAVY) +
             imgbox(6, 6, 154, H - 12, r=0) +
             solid(180, 52, 100, 10, r=4, fill=WHITE) +
             solid(180, 72, 74, 6, r=3, fill=SOFT) +
             solid(180, 86, 96, 6, r=3, fill=SOFT) +
             btn(180, 112, 62, 22))
    return clipped(inner)


def _horizontal_scroll():
    out = []
    for i in range(3):
        x = 20 + i * 108
        out.append(imgbox(x, 26, 96, 74))
        out.append(solid(x, 108, 62, 7, r=3, fill=NAVY))
        out.append(solid(x, 122, 88, 5))
    out.append(solid(20, 146, 200, 6, r=3, fill=LIGHT))
    out.append(solid(20, 146, 96, 6, r=3, fill=NAVY))
    return clipped("".join(out)) + frame()


def _org_chart():
    out = [frame(), box(128, 20, 64, 26, r=5, sw=2.5, fill=LIGHT),
           '<path d="M160 46 V62 M60 62 H260 M60 62 V78 M160 62 V78 M260 62 V78" '
           'stroke="%s" stroke-width="2.5" fill="none"/>' % MUTE]
    for i in range(3):
        out.append(box(28 + i * 100, 78, 64, 24, r=5, sw=2.5))
    out.append('<path d="M160 102 V118 M116 118 H204 M116 118 V132 M204 118 V132" '
               'stroke="%s" stroke-width="2.5" fill="none"/>' % MUTE)
    for i in range(2):
        out.append(box(90 + i * 88, 132, 52, 22, r=5, sw=2.5))
    return "".join(out)


def _roadmap_gantt():
    out = [frame()]
    for c in range(5):
        out.append(solid(100 + c * 44, 24, 1.5, 118, r=0, fill=LIGHT))
    for i, (off, w) in enumerate(((0, 120), (60, 92), (28, 150), (100, 80))):
        y = 40 + i * 28
        out.append(solid(20, y + 5, 62, 6))
        out.append(solid(100 + off, y, w, 16, r=4,
                         fill=GOLD if i == 1 else NAVY))
    for i in range(3):
        cx = 140 + i * 60
        out.append('<path d="M%g 150 l7 -7 l7 7 l-7 7 Z" fill="%s"/>'
                   % (cx, GOLD if i == 1 else MUTE))
    return "".join(out)


# --- v2: directorio -------------------------------------------------------

def _directory_az():
    out = [frame()]
    for i in range(9):
        x = 22 + i * 32
        out.append(chip(x, 20, 24, 18, GOLD if i == 2 else LIGHT))
        out.append(solid(x + 9, 26, 6, 6, r=1, fill=NAVY))
    for c in range(3):
        x = 26 + c * 96
        out.append(solid(x, 52, 14, 10, r=3, fill=NAVY))
        out.append(solid(x, 68, 76, 1.5, r=0, fill=MUTE))
        for r in range(4):
            out.append(solid(x, 78 + r * 19, 76 - (r % 2) * 20, 6))
    return "".join(out)


# El catalogo, agrupado. La categoria es DATO, no un comentario: permite pedir
# "solo inmobiliaria" al montar el deck de un cliente. `BLOCKS` se deriva de aqui.
CATALOGO = [
    ("Portada y cabeceras", {
        "hero-banner": _hero,
        "hero-fullscreen": _hero_fullscreen,
        "carousel-featured": _carousel_featured,
        "page-header": _page_header,
        "welcome-video": _welcome_video,
    }),
    ("Contenido base", {
        "title": _title,
        "text": _text,
        "text-image": _text_image,
        "text-image-alt": _text_image_alt,
        "article-body": _article_body,
        "seo-text": _seo_text,
        "pull-quote": _pull_quote,
        "full-width-band": _full_width_band,
        "spacer": _spacer,
    }),
    ("Confianza y marca", {
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
    }),
    ("Contenidos gestionables (CPT)", {
        "solution-selector": _solution_selector,
        "cpt-showcase": _cpt_showcase,
        "cpt-list": _cpt_list,
        "cpt-detail": _cpt_detail,
        "spec-sheet": _spec_sheet,
        "card-grid": _card_grid,
        "category-grid": _category_grid,
        "related-items": _related_items,
    }),
    ("Tienda (WooCommerce)", {
        "shop-catalog": _shop_catalog,
        "product-category": _product_category,
        "product-detail": _product_detail,
        "product-carousel": _product_carousel,
        "search-featured": _search_featured,
        "cart": _cart,
        "checkout": _checkout,
        "my-account": _my_account,
    }),
    ("Multimedia", {
        "gallery-grid": _gallery_grid,
        "gallery-carousel": _gallery_carousel,
        "video-gallery": _video_gallery,
        "video-fullwidth": _video_fullwidth,
        "video-text": _video_text,
        "image-compare": _image_compare,
    }),
    ("Blog", {
        "latest-news": _latest_news,
        "news-list": _news_list,
    }),
    ("Conversion y contacto", {
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
    }),
    ("Organizacion de la informacion", {
        "tabs-accordion": _tabs_accordion,
        "faq-accordion": _faq_accordion,
        "steps-process": _steps_process,
        "downloads": _downloads,
        "pricing-plans": _pricing_plans,
    }),
    ("Navegacion y chrome", {
        "nav-bar": _nav_bar,
        "mega-menu": _mega_menu,
        "footer-columns": _footer_columns,
        "table-of-contents": _table_of_contents,
        "cookie-consent": _cookie_consent,
    }),
    ("Reservas y horarios", {
        "booking-calendar": _booking_calendar,
        "time-slots": _time_slots,
        "opening-hours": _opening_hours,
        "multi-step-form": _multi_step_form,
    }),
    ("Configuracion y precio", {
        "price-calculator": _price_calculator,
        "product-configurator": _product_configurator,
    }),
    ("Datos", {
        "stats-chart": _stats_chart,
        "donut-stats": _donut_stats,
        "progress-bars": _progress_bars,
        "data-table": _data_table,
        "comparison-table": _comparison_table,
    }),
    # `property-features` (iconos + cifra + etiqueta) vivio aqui hasta que el
    # render lo delato: dibuja `why-us` y `kpis`. Misma silueta, fuera.
    ("Inmobiliaria", {
        "property-map-list": _property_map_list,
        "floor-plan": _floor_plan,
    }),
    ("Restauracion", {
        "menu-carta": _menu_carta,
    }),
    ("Formacion", {
        "lesson-player": _lesson_player,
        "quiz": _quiz,
    }),
    ("Eventos", {
        "event-countdown": _event_countdown,
        "event-agenda": _event_agenda,
    }),
    ("Comercio", {
        "product-zoom": _product_zoom,
        "size-guide": _size_guide,
        "seat-picker": _seat_picker,
    }),
    ("Comunidad y conversacion", {
        "comments-thread": _comments_thread,
        "chat-panel": _chat_panel,
        "ratings-breakdown": _ratings_breakdown,
        "ai-search": _ai_search,
    }),
    ("Medios e interaccion", {
        "audio-player": _audio_player,
        "hotspot-image": _hotspot_image,
        "file-upload": _file_upload,
    }),
    ("Estructuras", {
        "bento-grid": _bento_grid,
        "masonry-grid": _masonry_grid,
        "marquee-band": _marquee_band,
        "timeline-vertical": _timeline_vertical,
        "split-screen": _split_screen,
        "horizontal-scroll": _horizontal_scroll,
        "org-chart": _org_chart,
        "roadmap-gantt": _roadmap_gantt,
    }),
    ("Directorio", {
        "directory-az": _directory_az,
    }),
]

BLOCKS = {slug: fn for _, grupo in CATALOGO for slug, fn in grupo.items()}

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
