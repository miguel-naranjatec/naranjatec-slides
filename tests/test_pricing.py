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
