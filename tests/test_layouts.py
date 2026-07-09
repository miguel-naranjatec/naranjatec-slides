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
