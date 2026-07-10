"""Tests de los layouts que validan su entrada. ASCII puro.

El resto de layouts solo dibujan: no hay logica que probar sin abrir PowerPoint.
Aqui solo se fijan los limites que, si se rompen en silencio, hacen perder
contenido (un producto adicional, un punto de la solucion).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import brand.theme as T
import lib.slides as s


def _prs():
    return s.new_presentation()


def _extra(price=100, image=None):
    return {"price": price, "name": "X", "desc": "y",
            "icon": T.ICON["bolt"], "image": image}


def _punto():
    return ("Titular", "Texto", T.ICON["check"])


def _imgs():
    return [T.img("ecco-working.jpg"), T.img("ecco-office.jpg")]


# --- add_extras -----------------------------------------------------------

def test_add_extras_admite_de_dos_a_cuatro():
    for n in (2, 3, 4):
        slide = s.add_extras(_prs(), "Extras", [_extra()] * n)
        assert slide is not None


def test_add_extras_con_una_sola_lanza():
    with pytest.raises(ValueError, match="entre 2 y 4"):
        s.add_extras(_prs(), "Extras", [_extra()])


def test_add_extras_con_cinco_lanza_en_vez_de_truncar():
    with pytest.raises(ValueError, match="entre 2 y 4"):
        s.add_extras(_prs(), "Extras", [_extra()] * 5)


def test_add_extras_sin_imagen_no_revienta():
    slide = s.add_extras(_prs(), "Extras", [_extra(), _extra()])
    assert slide is not None


def test_add_extras_formatea_el_precio_con_signo_mas():
    slide = s.add_extras(_prs(), "Extras", [_extra(375), _extra(150)])
    textos = [sp.text_frame.text for sp in slide.shapes if sp.has_text_frame]
    assert ("+375 " + s.EURO) in textos
    assert ("+150 " + s.EURO) in textos


# --- add_solution ---------------------------------------------------------

def test_add_solution_admite_de_dos_a_cuatro_puntos():
    for n in (2, 3, 4):
        slide = s.add_solution(_prs(), "Solucion", [_punto()] * n, _imgs())
        assert slide is not None


def test_add_solution_con_cinco_puntos_lanza():
    with pytest.raises(ValueError, match="entre 2 y 4"):
        s.add_solution(_prs(), "Solucion", [_punto()] * 5, _imgs())


def test_add_solution_exige_dos_imagenes():
    with pytest.raises(ValueError, match="2 imagenes"):
        s.add_solution(_prs(), "Solucion", [_punto()] * 2, _imgs()[:1])


def test_add_solution_highlight_anade_una_forma():
    sin = s.add_solution(_prs(), "S", [_punto()] * 3, _imgs())
    con = s.add_solution(_prs(), "S", [_punto()] * 3, _imgs(), highlight=1)
    assert len(con.shapes) == len(sin.shapes) + 1


# --- add_stats_feature ----------------------------------------------------

def _stat(v="+22"):
    return {"value": v, "label": "una etiqueta corta", "icon": T.ICON["shield"]}


def test_add_stats_feature_admite_de_dos_a_cuatro():
    for n in (2, 3, 4):
        slide = s.add_stats_feature(_prs(), "Cifras", [_stat()] * n,
                                    T.img("ecco-working.jpg"))
        assert slide is not None


def test_add_stats_feature_con_cinco_lanza():
    with pytest.raises(ValueError, match="entre 2 y 4"):
        s.add_stats_feature(_prs(), "Cifras", [_stat()] * 5,
                            T.img("ecco-working.jpg"))


def test_ninguna_caja_con_medida_no_positiva():
    # Un alto negativo produce un .pptx que PowerPoint se niega a abrir, y
    # python-pptx no se queja. Este es el caso que lo destapo.
    slide = s.add_stats_feature(_prs(), "Cifras", [_stat()] * 4,
                                T.img("ecco-working.jpg"),
                                subtitle="Con subtitulo, que es el caso justo")
    for sp in slide.shapes:
        assert int(sp.height) > 0
        assert int(sp.width) > 0


def test_check_box_lanza_con_medidas_no_positivas():
    with pytest.raises(ValueError, match="caja invalida"):
        s._check_box(s.Inches(2), s.Inches(-0.5), "prueba")
    with pytest.raises(ValueError, match="caja invalida"):
        s._check_box(0, s.Inches(1), "prueba")


# --- add_next_steps -------------------------------------------------------

def _paso():
    return ("Titular", "Texto corto.", T.ICON["check"])


def test_add_next_steps_admite_de_tres_a_cinco():
    for n in (3, 4, 5):
        slide = s.add_next_steps(_prs(), "Pasos", [_paso()] * n)
        assert slide is not None


def test_add_next_steps_con_dos_lanza():
    with pytest.raises(ValueError, match="entre 3 y 5"):
        s.add_next_steps(_prs(), "Pasos", [_paso()] * 2)


def test_add_next_steps_con_seis_lanza():
    with pytest.raises(ValueError, match="entre 3 y 5"):
        s.add_next_steps(_prs(), "Pasos", [_paso()] * 6)


def test_add_next_steps_pinta_un_arco_y_una_punta_por_hueco():
    # n pasos -> n-1 arcos (formas libres, custGeom) y n-1 puntas (triangulos).
    for n in (3, 4, 5):
        slide = s.add_next_steps(_prs(), "Pasos", [_paso()] * n)
        xml = slide.shapes._spTree.xml
        # OJO: "custGeom" aparece dos veces por forma (apertura y cierre).
        assert xml.count("<a:custGeom>") == n - 1, "arcos con n=%d" % n
        assert xml.count('prst="triangle"') == n - 1, "puntas con n=%d" % n


# --- add_blocks_grid ------------------------------------------------------

def _bloque():
    return ("hero-banner", "Hero", "Imagen, titular y CTA.")


def test_add_blocks_grid_devuelve_siempre_lista():
    out = s.add_blocks_grid(_prs(), "Bloques", [_bloque()] * 3)
    assert isinstance(out, list) and len(out) == 1


def test_add_blocks_grid_pagina_de_doce_en_doce():
    for n, paginas in ((12, 1), (13, 2), (24, 2), (25, 3)):
        out = s.add_blocks_grid(_prs(), "Bloques", [_bloque()] * n)
        assert len(out) == paginas, "n=%d" % n


def test_add_blocks_grid_invoca_el_contador_por_pagina():
    llamadas = []

    def contador():
        llamadas.append(len(llamadas) + 1)
        return len(llamadas)

    s.add_blocks_grid(_prs(), "Bloques", [_bloque()] * 13, page=contador)
    assert llamadas == [1, 2]


def test_add_blocks_grid_vacia_lanza():
    with pytest.raises(ValueError, match="vacia"):
        s.add_blocks_grid(_prs(), "Bloques", [])


def test_add_blocks_grid_page_evaluado_lanza():
    with pytest.raises(TypeError, match="contador"):
        s.add_blocks_grid(_prs(), "Bloques", [_bloque()], page=7)


def test_block_inexistente_lanza_con_pista():
    with pytest.raises(FileNotFoundError, match="make_blocks"):
        T.block("este-bloque-no-existe")


def test_todos_los_svg_tienen_su_png():
    # El SVG es la fuente; el PNG es lo que entra en el .pptx. Si falta uno,
    # el deck revienta al construirse, no al abrirse.
    svgs = {p.stem for p in T.BLOCKS_SRC.glob("*.svg")}
    pngs = {p.stem for p in T.BLOCKS_DIR.glob("*.png")}
    assert svgs, "no hay SVG de bloques"
    assert svgs - pngs == set(), "sin rasterizar: %s" % sorted(svgs - pngs)
    assert pngs - svgs == set(), "PNG huerfanos: %s" % sorted(pngs - svgs)


# --- catalogo de bloques (scripts/gen_blocks.py) ---------------------------

def _gen_blocks():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    import gen_blocks
    return gen_blocks


def test_ningun_slug_repetido_entre_grupos():
    # `BLOCKS` es un dict derivado de `CATALOGO`: si dos grupos declaran el mismo
    # slug, el segundo se come al primero en silencio y perdemos un bloque sin
    # que nadie se entere.
    g = _gen_blocks()
    vistos, repes = set(), []
    for _, grupo in g.CATALOGO:
        for slug in grupo:
            if slug in vistos:
                repes.append(slug)
            vistos.add(slug)
    assert repes == [], "slugs repetidos: %s" % sorted(repes)


def test_todo_bloque_tiene_categoria():
    g = _gen_blocks()
    declarados = sum(len(grupo) for _, grupo in g.CATALOGO)
    assert declarados == len(g.BLOCKS)


def test_cada_svg_generado_corresponde_a_un_bloque_del_catalogo():
    # Un SVG que sobra en disco es un bloque borrado del catalogo cuyo fichero
    # nadie limpio: aparecera en el deck aunque ya no exista la funcion.
    g = _gen_blocks()
    svgs = {p.stem for p in T.BLOCKS_SRC.glob("*.svg")}
    assert svgs == set(g.BLOCKS), "descuadre: %s" % sorted(svgs ^ set(g.BLOCKS))


# --- el skill propuesta-a-deck --------------------------------------------
# El skill le dice a la IA que layouts y que bloques usar. Si uno se renombra o
# se borra, el skill sigue recomendandolo y el deck revienta al construirse.

SKILL = (Path(__file__).resolve().parent.parent / ".claude" / "skills" /
         "propuesta-a-deck" / "SKILL.md")

_SLUG = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")
_LAYOUT = re.compile(r"`(add_[a-z_]+)`")


def test_el_skill_solo_cita_layouts_que_existen():
    citados = set(_LAYOUT.findall(SKILL.read_text(encoding="utf-8")))
    assert citados, "el skill no cita ningun layout"
    faltan = sorted(nombre for nombre in citados if not hasattr(s, nombre))
    assert faltan == [], "el skill cita layouts inexistentes: %s" % faltan


def test_el_skill_solo_cita_bloques_que_existen():
    texto = SKILL.read_text(encoding="utf-8")
    g = _gen_blocks()
    # El skill nombra su propio slug en el frontmatter; no es un bloque.
    citados = set(_SLUG.findall(texto)) - {"propuesta-a-deck"}
    assert citados, "el skill no cita ningun bloque"
    faltan = sorted(slug for slug in citados if slug not in g.BLOCKS)
    assert faltan == [], "el skill cita bloques inexistentes: %s" % faltan
