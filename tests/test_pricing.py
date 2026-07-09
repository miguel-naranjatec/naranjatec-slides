"""Tests de add_pricing (lib/slides.py). ASCII puro."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import lib.slides as s


def test_fmt_miles_agrupa_de_tres_en_tres():
    assert s._fmt_miles(1) == "1"
    assert s._fmt_miles(999) == "999"
    assert s._fmt_miles(1300) == "1.300"
    assert s._fmt_miles(1234567) == "1.234.567"


def test_fmt_eur_entero_sin_decimales():
    assert s._fmt_eur(1300) == "1.300 " + s.EURO
    assert s._fmt_eur(5530) == "5.530 " + s.EURO


def test_fmt_eur_float_sin_parte_decimal_no_pinta_decimales():
    assert s._fmt_eur(1300.0) == "1.300 " + s.EURO


def test_fmt_eur_con_decimales_usa_coma():
    assert s._fmt_eur(1300.5) == "1.300,50 " + s.EURO
    assert s._fmt_eur(0.05) == "0,05 " + s.EURO


def test_fmt_eur_negativo_para_descuentos():
    assert s._fmt_eur(-250) == "-250 " + s.EURO


def test_euro_es_el_simbolo_no_la_cadena_eur():
    assert s.EURO == "\u20AC"


def test_fmt_eur_cero_negativo_no_lleva_signo():
    assert s._fmt_eur(-0.004) == "0 " + s.EURO
    assert s._fmt_eur(-0.0) == "0 " + s.EURO


def test_fmt_eur_acarreo_al_redondear_centimos():
    assert s._fmt_eur(1299.999) == "1.300 " + s.EURO
    assert s._fmt_eur(0.999) == "1 " + s.EURO


def _filas(n):
    return [("Partida %d" % i, 100 * i) for i in range(1, n + 1)]


def test_split_rows_una_pagina_hasta_cinco():
    for n in (1, 3, 5):
        paginas = s._split_rows(_filas(n))
        assert len(paginas) == 1
        assert len(paginas[0]) == n


def test_split_rows_dos_paginas_equilibradas():
    assert [len(p) for p in s._split_rows(_filas(6))] == [3, 3]
    assert [len(p) for p in s._split_rows(_filas(7))] == [4, 3]
    assert [len(p) for p in s._split_rows(_filas(10))] == [5, 5]


def test_split_rows_ninguna_pagina_excede_el_maximo():
    for n in range(1, s.MAX_PRICING_ROWS + 1):
        for pagina in s._split_rows(_filas(n)):
            assert len(pagina) <= s.ROWS_PER_PAGE


def test_split_rows_conserva_el_orden():
    paginas = s._split_rows(_filas(7))
    juntas = paginas[0] + paginas[1]
    assert juntas == _filas(7)


def _prs():
    return s.new_presentation()


def test_add_pricing_devuelve_lista_incluso_con_una_pagina():
    out = s.add_pricing(_prs(), "Inversion", _filas(3))
    assert isinstance(out, list)
    assert len(out) == 1


def test_add_pricing_dos_paginas_con_siete_partidas():
    out = s.add_pricing(_prs(), "Inversion", _filas(7))
    assert len(out) == 2


def test_add_pricing_invoca_el_contador_una_vez_por_pagina():
    llamadas = []

    def contador():
        llamadas.append(len(llamadas) + 1)
        return len(llamadas)

    s.add_pricing(_prs(), "Inversion", _filas(7), page=contador)
    assert llamadas == [1, 2]


def test_add_pricing_rows_vacia_lanza():
    with pytest.raises(ValueError, match="vacia"):
        s.add_pricing(_prs(), "Inversion", [])


def test_add_pricing_mas_de_diez_lanza_en_vez_de_truncar():
    with pytest.raises(ValueError, match="maximo"):
        s.add_pricing(_prs(), "Inversion", _filas(11))


def test_add_pricing_total_numerico_lanza():
    with pytest.raises(TypeError, match="None o str"):
        s.add_pricing(_prs(), "Inversion", _filas(3), total=5530)


def test_add_pricing_page_evaluado_lanza():
    with pytest.raises(TypeError, match="contador"):
        s.add_pricing(_prs(), "Inversion", _filas(3), page=7)
