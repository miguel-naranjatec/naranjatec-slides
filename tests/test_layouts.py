"""Tests de los layouts que validan su entrada. ASCII puro.

El resto de layouts solo dibujan: no hay logica que probar sin abrir PowerPoint.
Aqui solo se fijan los limites que, si se rompen en silencio, hacen perder
contenido (un producto adicional, un punto de la solucion).
"""

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
