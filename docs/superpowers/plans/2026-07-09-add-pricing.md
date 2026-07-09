# add_pricing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Anadir a `lib/slides.py` un layout `add_pricing` que presente un desglose de presupuesto (partidas numeradas con importe, tarjeta de total y nota al pie), paginando solo cuando hace falta.

**Architecture:** Tres funciones puras y comprobables (`_fmt_eur`, `_fmt_miles`, `_split_rows`) mas un pintor privado por pagina (`_pricing_page`) y la funcion publica `add_pricing`, que valida, reparte las partidas y devuelve la lista de slides. La logica de negocio (formato, reparto, validacion) queda separada del dibujo, que es lo unico no testeable sin abrir PowerPoint.

**Tech Stack:** Python 3.10+, `python-pptx`. Tests con `pytest` (nueva dependencia de desarrollo, no de ejecucion).

## Global Constraints

- `lib/slides.py`, `content/muestrario.py` y los tests son **ASCII puro**: sin acentos, sin ene, sin comillas tipograficas. Verificar con `python -c "print(sum(1 for b in open('RUTA','rb').read() if b>127))"` -> debe dar `0`.
- El simbolo del euro se escribe **siempre** como el escape `\u20AC`, nunca como caracter literal.
- No se anaden dependencias de ejecucion: `requirements.txt` sigue siendo `python-pptx` + `Pillow`.
- Maximo **10** partidas. Mas de 10 -> `ValueError`. Nunca truncar en silencio.
- `page` recibe el **contador** (`page=n`), no su valor (`page=n()`).
- `add_pricing` devuelve **siempre una lista** de slides.
- Aritmetica de EMU como en el resto del fichero: `Emu(int(a) + int(b))`, nunca sumar objetos `Emu` directamente.
- La altura de fila esta topada (`ROW_H_MAX`) y el bloque de filas se centra en el hueco disponible: con 1 o 2 partidas las filas NO deben estirarse a media diapositiva.

## Correccion al spec

El spec dice reutilizar `_letter_badge()`. Tras leerlo (`lib/slides.py:1290`), **no sirve**: dibuja un circulo de *contorno*, con la letra en `T.FONT_HEAD` a 16pt fijos y el color del texto atado al del trazo. Necesitamos un circulo *relleno* navy con el ordinal dorado en `T.FONT_NUM`. Adaptarlo pediria cuatro parametros opcionales para un unico llamante. Se anade en su lugar `_num_badge()`, seis lineas, una responsabilidad. `_letter_badge` no se toca.

## File Structure

| Fichero | Responsabilidad |
|---------|-----------------|
| `lib/slides.py` (modificar) | `_fmt_miles`, `_fmt_eur`, `_split_rows`, `_num_badge`, `_pricing_page`, `add_pricing` |
| `tests/test_pricing.py` (crear) | Tests de formato, reparto, validacion y numero de slides |
| `requirements-dev.txt` (crear) | `pytest` |
| `content/muestrario.py` (modificar) | Una diapositiva de ejemplo con 3 partidas |
| `CLAUDE.md`, `README.md` (modificar) | Catalogo de layouts y conteo |

---

### Task 1: Formato de importes en es-ES

**Files:**
- Create: `requirements-dev.txt`
- Create: `tests/test_pricing.py`
- Modify: `lib/slides.py` (anadir constantes y helpers tras `_emph_runs`, sobre `_title`)

**Interfaces:**
- Consumes: nada.
- Produces: `_fmt_miles(entero: int) -> str`, `_fmt_eur(valor: int|float) -> str`, constantes `EURO: str`, `MAX_PRICING_ROWS: int = 10`, `ROWS_PER_PAGE: int = 5`, `ROW_H_MAX: Emu = Inches(1.05)`.

- [ ] **Step 1: Crear la dependencia de desarrollo**

`requirements-dev.txt`:

```
# Solo para ejecutar los tests. Las dependencias de ejecucion estan en
# requirements.txt (python-pptx + Pillow).
-r requirements.txt
pytest>=8.0
```

Instalar: `python -m pip install -r requirements-dev.txt`

- [ ] **Step 2: Escribir el test que falla**

`tests/test_pricing.py`:

```python
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
```

- [ ] **Step 3: Ejecutar el test y verificar que falla**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: FAIL con `AttributeError: module 'lib.slides' has no attribute '_fmt_miles'`

- [ ] **Step 4: Implementar**

En `lib/slides.py`, justo despues de la funcion `_emph_runs` y antes de `_title`:

```python
# --- Presupuestos (add_pricing) ------------------------------------------

EURO = "\u20AC"          # NUNCA el caracter literal: el fichero es ASCII puro
MAX_PRICING_ROWS = 10    # mas partidas -> ValueError (no se truncan en silencio)
ROWS_PER_PAGE = 5        # filas que caben holgadas en una pagina
ROW_H_MAX = Inches(1.05)  # tope de alto de fila: con 1 partida no se estira


def _fmt_miles(entero):
    """1234567 -> '1.234.567' (separador de miles es-ES)."""
    s = str(int(entero))
    grupos = []
    while len(s) > 3:
        grupos.insert(0, s[-3:])
        s = s[:-3]
    grupos.insert(0, s)
    return ".".join(grupos)


def _fmt_eur(valor):
    """Importe en es-ES: 1300 -> '1.300 EUR'; 1300.5 -> '1.300,50 EUR'.

    (En el codigo EUR es el escape EURO; aqui se nombra asi por ser ASCII.)
    Los enteros no llevan decimales; los decimales van con coma y dos cifras.
    """
    negativo = valor < 0
    v = abs(valor)
    entero = int(v)
    centimos = int(round((float(v) - entero) * 100))
    if centimos == 100:          # 1299.999 -> 1.300
        entero += 1
        centimos = 0
    if centimos:
        cuerpo = "%s,%02d" % (_fmt_miles(entero), centimos)
    else:
        cuerpo = _fmt_miles(entero)
    return "%s%s %s" % ("-" if negativo else "", cuerpo, EURO)
```

- [ ] **Step 5: Ejecutar los tests y verificar que pasan**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: PASS (6 passed)

- [ ] **Step 6: Verificar ASCII**

Run: `python -c "print(sum(1 for b in open('lib/slides.py','rb').read() if b>127))"`
Expected: `0`

Run: `python -c "print(sum(1 for b in open('tests/test_pricing.py','rb').read() if b>127))"`
Expected: `0`

- [ ] **Step 7: Commit**

```bash
git add requirements-dev.txt tests/test_pricing.py lib/slides.py
git commit -m "add_pricing: formato de importes en es-ES"
```

---

### Task 2: Reparto de partidas en paginas

**Files:**
- Modify: `lib/slides.py` (anadir `_split_rows` tras `_fmt_eur`)
- Modify: `tests/test_pricing.py` (anadir tests)

**Interfaces:**
- Consumes: `ROWS_PER_PAGE` de Task 1.
- Produces: `_split_rows(rows: list) -> list[list]`. Una sola pagina si `len(rows) <= 5`; dos paginas equilibradas si hay entre 6 y 10.

- [ ] **Step 1: Escribir el test que falla**

Anadir al final de `tests/test_pricing.py`:

```python
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
```

- [ ] **Step 2: Ejecutar y verificar que falla**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: FAIL con `AttributeError: module 'lib.slides' has no attribute '_split_rows'`

- [ ] **Step 3: Implementar**

En `lib/slides.py`, justo despues de `_fmt_eur`:

```python
def _split_rows(rows):
    """Reparte las partidas en paginas de ROWS_PER_PAGE o menos.

    Con 5 o menos, una sola pagina. Con 6-10, dos paginas equilibradas
    (7 -> 4+3), para que ninguna quede casi vacia.
    """
    n = len(rows)
    if n <= ROWS_PER_PAGE:
        return [list(rows)]
    corte = (n + 1) // 2
    return [list(rows[:corte]), list(rows[corte:])]
```

- [ ] **Step 4: Ejecutar y verificar que pasan**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: PASS (10 passed)

- [ ] **Step 5: Commit**

```bash
git add lib/slides.py tests/test_pricing.py
git commit -m "add_pricing: reparto equilibrado de partidas en paginas"
```

---

### Task 3: Validacion y contrato de add_pricing

**Files:**
- Modify: `lib/slides.py` (anadir `add_pricing` al final, junto a los demas `add_*`)
- Modify: `tests/test_pricing.py`

**Interfaces:**
- Consumes: `_split_rows`, `MAX_PRICING_ROWS` (Tasks 1-2); `new_presentation()` ya existente.
- Produces: `add_pricing(prs, title, rows, note="", total=None, subtitle="", page=None, section="") -> list`. En esta task devuelve slides vacios (sin pintar); Tasks 4-5 los rellenan.

- [ ] **Step 1: Escribir el test que falla**

Anadir a `tests/test_pricing.py`:

```python
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
```

- [ ] **Step 2: Ejecutar y verificar que falla**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: FAIL con `AttributeError: module 'lib.slides' has no attribute 'add_pricing'`

- [ ] **Step 3: Implementar**

Al final de `lib/slides.py`:

```python
def add_pricing(prs, title, rows, note="", total=None, subtitle="", page=None,
                section=""):
    """Desglose de presupuesto: partidas numeradas + tarjeta de total + nota.

    rows  : [(concepto, importe)] con importe int/float. Maximo 10 partidas.
    total : None -> se suma a partir de rows. Un str se pinta tal cual
            ("A convenir"). NO acepta un numero: el total nunca debe poder
            contradecir al desglose.
    page  : el CONTADOR, no su valor. page=n, no page=n(). Se invoca una vez
            por pagina generada.

    MULTIPAGINA: con 6-10 partidas genera dos diapositivas (la primera a ancho
    completo, sin tarjeta) y el total va en la ultima. Devuelve SIEMPRE la lista
    de slides, tenga una o dos.
    """
    if not rows:
        raise ValueError("add_pricing: 'rows' no puede estar vacia")
    if len(rows) > MAX_PRICING_ROWS:
        raise ValueError(
            "add_pricing: %d partidas; el maximo es %d. Agrupa partidas o usa "
            "dos diapositivas: no se truncan en silencio."
            % (len(rows), MAX_PRICING_ROWS))
    if total is not None and not isinstance(total, str):
        raise TypeError(
            "add_pricing: 'total' debe ser None o str (p.ej. 'A convenir'); "
            "los importes se suman a partir de 'rows'")
    if page is not None and not callable(page):
        raise TypeError(
            "add_pricing: 'page' debe ser el contador (page=n), no su valor "
            "(page=n())")

    rows = [tuple(r) for r in rows]
    texto_total = total if total is not None else _fmt_eur(sum(r[1] for r in rows))
    paginas = _split_rows(rows)
    slides = []
    ordinal = 1
    for i, chunk in enumerate(paginas):
        ultima = (i == len(paginas) - 1)
        slides.append(_pricing_page(
            prs, title, chunk, ordinal=ordinal, subtitle=subtitle,
            section=section, page=(page() if page is not None else None),
            texto_total=(texto_total if ultima else None),
            note=(note if ultima else "")))
        ordinal += len(chunk)
    return slides
```

Y un `_pricing_page` provisional (Tasks 4-5 lo completan), justo antes de `add_pricing`:

```python
def _pricing_page(prs, title, rows, ordinal, subtitle, section, page,
                  texto_total, note):
    """Pinta UNA pagina del desglose. texto_total=None -> sin tarjeta (pagina
    no final): las filas ocupan todo el ancho."""
    slide = _slide(prs)
    _topbar(slide, section)
    _title(slide, title, y=Inches(1.35))
    _pagenum(slide, page)
    return slide
```

- [ ] **Step 4: Ejecutar y verificar que pasan**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: PASS (17 passed)

- [ ] **Step 5: Commit**

```bash
git add lib/slides.py tests/test_pricing.py
git commit -m "add_pricing: contrato, validacion y paginacion"
```

---

### Task 4: Filas con chip numerado e importe

**Files:**
- Modify: `lib/slides.py` (anadir `_num_badge`; completar `_pricing_page`)
- Modify: `tests/test_pricing.py`

**Interfaces:**
- Consumes: `_rect`, `_text`, `_soft_shadow`, `_title`, `_topbar`, `_slide`, `_pagenum`, `MARGIN`, `CONTENT_W`, `GAP_AFTER_TITLE`, `_fmt_eur`.
- Produces: `_num_badge(slide, x, y, size, num)`. `_pricing_page` pinta las filas y respeta `ordinal` (los numeros continuan en la segunda pagina).

- [ ] **Step 1: Escribir el test que falla**

Anadir a `tests/test_pricing.py`:

```python
def _textos(slide):
    out = []
    for sp in slide.shapes:
        if sp.has_text_frame:
            out.append(sp.text_frame.text)
    return out


def test_las_filas_pintan_concepto_e_importe_formateado():
    slide = s.add_pricing(_prs(), "Inversion", [("Desarrollo", 2950)])[0]
    textos = _textos(slide)
    assert "Desarrollo" in textos
    assert ("2.950 " + s.EURO) in textos


def test_los_ordinales_continuan_en_la_segunda_pagina():
    paginas = s.add_pricing(_prs(), "Inversion", _filas(7))
    assert "1" in _textos(paginas[0])
    assert "4" in _textos(paginas[0])
    assert "5" in _textos(paginas[1])
    assert "7" in _textos(paginas[1])
    assert "5" not in _textos(paginas[0])
```

- [ ] **Step 2: Ejecutar y verificar que falla**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: FAIL: `assert 'Desarrollo' in []` (la pagina aun no pinta filas)

- [ ] **Step 3: Implementar `_num_badge`**

En `lib/slides.py`, justo despues de `_letter_badge`:

```python
def _num_badge(slide, x, y, size, num):
    """Circulo RELLENO navy con un ordinal dorado (filas de add_pricing).

    Distinto de _letter_badge, que es de contorno y usa el color del trazo para
    el texto.
    """
    _rect(slide, x, y, size, size, fill=T.AZUL_OSCURO, shape=MSO_SHAPE.OVAL)
    _text(slide, x, y, size, size,
          [[(num, {"size": Pt(12), "bold": True, "color": T.AMARILLO,
                   "font": T.FONT_NUM})]],
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
```

- [ ] **Step 4: Completar `_pricing_page` con las filas**

Reemplazar el `_pricing_page` provisional por:

```python
def _pricing_page(prs, title, rows, ordinal, subtitle, section, page,
                  texto_total, note):
    """Pinta UNA pagina del desglose. texto_total=None -> sin tarjeta (pagina
    no final): las filas ocupan todo el ancho."""
    slide = _slide(prs)
    _topbar(slide, section)
    tb = _title(slide, title, y=Inches(1.35))
    top = max(int(Inches(2.5)), int(tb) + int(GAP_AFTER_TITLE))
    if subtitle:
        _text(slide, MARGIN, Emu(int(tb) + int(Inches(0.1))), Inches(9.0),
              Inches(0.5),
              [[(subtitle, {"size": Pt(14), "italic": True,
                            "color": T.GRIS_SUAVE,
                            "font": T.FONT_TITLE_EMPH})]])
        top += int(Inches(0.45))

    bottom = int(Inches(6.3)) if note else int(Inches(6.6))
    block_h = bottom - top

    con_total = texto_total is not None
    gap_col = int(Inches(0.5))
    rows_w = int(0.60 * int(CONTENT_W)) if con_total else int(CONTENT_W)

    # Alto de fila topado: sin el tope, una sola partida ocuparia todo el hueco.
    # El bloque resultante se centra verticalmente entre `top` y `bottom`.
    k = len(rows)
    gap_r = int(Inches(0.18))
    row_h = min(ROW_H_MAX, (block_h - (k - 1) * gap_r) // k)
    used_h = k * row_h + (k - 1) * gap_r
    rows_top = top + (block_h - used_h) // 2

    badge = int(Inches(0.34))
    pad = int(Inches(0.28))
    amount_w = int(Inches(2.3))
    concept_x = int(MARGIN) + pad + badge + pad
    concept_w = int(MARGIN) + rows_w - amount_w - int(Inches(0.5)) - concept_x

    for i, (concepto, importe) in enumerate(rows):
        y = rows_top + i * (row_h + gap_r)
        card = _rect(slide, MARGIN, Emu(y), Emu(rows_w), Emu(row_h),
                     fill=T.BLANCO, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
                     radius=0.06)
        _soft_shadow(card, alpha=10000)
        _num_badge(slide, Emu(int(MARGIN) + pad),
                   Emu(y + (row_h - badge) // 2), Emu(badge),
                   "%d" % (ordinal + i))
        _text(slide, Emu(concept_x), Emu(y), Emu(concept_w), Emu(row_h),
              [[(concepto, {"size": Pt(14.5), "color": T.AZUL_OSCURO,
                            "font": T.FONT_HEAD})]],
              anchor=MSO_ANCHOR.MIDDLE)
        _text(slide, Emu(int(MARGIN) + rows_w - amount_w - int(Inches(0.35))),
              Emu(y), Emu(amount_w), Emu(row_h),
              [[(_fmt_eur(importe), {"size": Pt(15), "bold": True,
                                     "color": T.AZUL_OSCURO,
                                     "font": T.FONT_NUM})]],
              align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

    _pagenum(slide, page)
    return slide
```

- [ ] **Step 5: Ejecutar y verificar que pasan**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: PASS (19 passed)

- [ ] **Step 6: Verificar ASCII**

Run: `python -c "print(sum(1 for b in open('lib/slides.py','rb').read() if b>127))"`
Expected: `0`

- [ ] **Step 7: Commit**

```bash
git add lib/slides.py tests/test_pricing.py
git commit -m "add_pricing: filas con chip numerado e importe"
```

---

### Task 5: Tarjeta de total y nota al pie

**Files:**
- Modify: `lib/slides.py` (completar `_pricing_page`)
- Modify: `tests/test_pricing.py`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: la ultima pagina pinta la tarjeta amarilla con `TOTAL ESTIMADO`, la cifra y la coletilla; y la nota al pie si `note` no esta vacia.

- [ ] **Step 1: Escribir el test que falla**

Anadir a `tests/test_pricing.py`:

```python
def test_el_total_se_suma_solo():
    slide = s.add_pricing(_prs(), "Inversion",
                          [("A", 1300), ("B", 2950), ("C", 1280)])[0]
    assert ("5.530 " + s.EURO) in _textos(slide)


def test_total_string_se_pinta_tal_cual():
    slide = s.add_pricing(_prs(), "Inversion", _filas(2),
                          total="A convenir")[0]
    assert "A convenir" in _textos(slide)


def test_la_tarjeta_de_total_solo_esta_en_la_ultima_pagina():
    paginas = s.add_pricing(_prs(), "Inversion", _filas(7))
    assert "TOTAL ESTIMADO" not in _textos(paginas[0])
    assert "TOTAL ESTIMADO" in _textos(paginas[1])


def test_la_nota_solo_esta_en_la_ultima_pagina():
    paginas = s.add_pricing(_prs(), "Inversion", _filas(7),
                            note="Precios sin IVA.")
    assert "Precios sin IVA." not in _textos(paginas[0])
    assert "Precios sin IVA." in _textos(paginas[1])


def test_importes_negativos_restan_del_total():
    slide = s.add_pricing(_prs(), "Inversion",
                          [("Web", 1000), ("Descuento", -250)])[0]
    textos = _textos(slide)
    assert ("-250 " + s.EURO) in textos
    assert ("750 " + s.EURO) in textos
```

- [ ] **Step 2: Ejecutar y verificar que falla**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: FAIL: `assert '5.530 EUR' in [...]` (la tarjeta no se pinta)

- [ ] **Step 3: Implementar**

En `_pricing_page`, justo antes de `_pagenum(slide, page)`, anadir:

```python
    # La tarjeta se alinea con el BLOQUE REAL de filas (rows_top/used_h), no con
    # el hueco completo: si no, con pocas partidas quedaria descuadrada.
    if con_total:
        card_x = int(MARGIN) + rows_w + gap_col
        card_w = int(CONTENT_W) - rows_w - gap_col
        card = _rect(slide, Emu(card_x), Emu(rows_top), Emu(card_w),
                     Emu(used_h), fill=T.AMARILLO,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
        _soft_shadow(card, alpha=9000)
        _text(slide, Emu(card_x), Emu(rows_top + int(Inches(0.5))), Emu(card_w),
              Inches(0.4),
              [[("TOTAL ESTIMADO", {"size": Pt(11), "color": T.AZUL_OSCURO,
                                    "font": T.FONT_MONO, "spacing": 120})]],
              align=PP_ALIGN.CENTER)
        cifra_h = int(Inches(1.2))
        _text(slide, Emu(card_x), Emu(rows_top + (used_h - cifra_h) // 2),
              Emu(card_w), Emu(cifra_h),
              [[(texto_total, {"size": Pt(38), "bold": True,
                               "color": T.AZUL_OSCURO, "font": T.FONT_NUM})]],
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _text(slide, Emu(card_x), Emu(rows_top + used_h - int(Inches(0.8))),
              Emu(card_w), Inches(0.4),
              [[("IVA no incluido", {"size": Pt(12), "italic": True,
                                     "color": T.AZUL_OSCURO,
                                     "font": T.FONT_TITLE_EMPH})]],
              align=PP_ALIGN.CENTER)

    if note:
        _text(slide, MARGIN, Emu(bottom + int(Inches(0.25))), CONTENT_W,
              Inches(0.6),
              [[(note, {"size": Pt(10), "italic": True, "color": T.GRIS_SUAVE,
                        "font": T.FONT_BODY})]], line_spacing=1.25)
```

- [ ] **Step 4: Ejecutar y verificar que pasan**

Run: `python -m pytest tests/test_pricing.py -q`
Expected: PASS (24 passed)

- [ ] **Step 5: Commit**

```bash
git add lib/slides.py tests/test_pricing.py
git commit -m "add_pricing: tarjeta de total y nota al pie"
```

---

### Task 6: Diapositiva de ejemplo y verificacion visual

**Files:**
- Modify: `content/muestrario.py` (anadir la slide tras `add_stats`)

**Interfaces:**
- Consumes: `add_pricing`. Ojo: en `muestrario.py` el contador se llama `n`; hay que pasar `page=n`, **sin parentesis**.

- [ ] **Step 1: Anadir la diapositiva al muestrario**

En `content/muestrario.py`, tras la llamada a `s.add_stats(...)`:

```python
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
```

- [ ] **Step 2: Generar el deck**

Run: `python build/build.py test`
Expected: `[ok] test -> output/NaranjaTec-Test-Disenos.pptx (30 diapositivas)`

Si da `PermissionError`, cerrar el .pptx en PowerPoint y repetir.

- [ ] **Step 3: Verificar ASCII del muestrario**

Run: `python -c "print(sum(1 for b in open('content/muestrario.py','rb').read() if b>127))"`
Expected: `0`

- [ ] **Step 4: Comprobar la paginacion con 7 partidas**

Run:

```bash
python -c "import sys; sys.path.insert(0,'.'); import lib.slides as s; prs=s.new_presentation(); print(len(s.add_pricing(prs,'X',[('P%d'%i,100*i) for i in range(1,8)])))"
```

Expected: `2`

- [ ] **Step 5: Verificacion visual (Windows con PowerPoint)**

Exportar a PNG y mirar la diapositiva nueva:

```powershell
$out = "$env:TEMP\pricing-render"
New-Item -ItemType Directory -Force $out | Out-Null
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("D:\AI\presentaciones-naranjatec\output\NaranjaTec-Test-Disenos.pptx", $true, $false, $false)
$pres.Export($out, "PNG", 1600, 900)
$pres.Close(); $ppt.Quit()
```

Revisar: el concepto no invade el importe, la cifra del total cabe en la tarjeta, la nota no pisa el numero de pagina.

En Linux/Cowork: `python scripts/preview.py test`.

- [ ] **Step 6: Commit**

```bash
git add content/muestrario.py
git commit -m "Muestrario: diapositiva de desglose de presupuesto"
```

---

### Task 7: Documentacion

**Files:**
- Modify: `CLAUDE.md` (catalogo de layouts)
- Modify: `README.md` (lista de tipos)

**Interfaces:**
- Consumes: nada. Cierra el trabajo.

- [ ] **Step 1: Anadir la entrada al catalogo de CLAUDE.md**

En `CLAUDE.md`, en el "Catalogo de layouts", tras la entrada de `add_product`:

```markdown
- `add_pricing(prs, title, rows, note="", total=None, subtitle="", page=n, section="")`
  Desglose de presupuesto: partidas numeradas + importe, tarjeta de total amarilla
  y nota al pie. `rows`: `[(concepto, importe)]`, importe numerico, **MAXIMO 10**
  (mas -> `ValueError`, NO trunca como `add_bullets`). El total se SUMA solo;
  `total=` solo acepta un `str` para forzar texto ("A convenir").
  **MULTIPAGINA**: con 6-10 partidas genera 2 slides (la 1a a ancho completo, sin
  tarjeta) y devuelve SIEMPRE una lista. `page` recibe el CONTADOR (`page=n`), no
  su valor (`page=n()`): unica excepcion de la libreria.
```

- [ ] **Step 2: Anadir el aviso a la seccion de convenciones de CLAUDE.md**

En "Convenciones de contenido", tras la linea del numero de pagina:

```markdown
- Excepciones de `page`: los separadores y `add_timeline` NO lo llevan;
  `add_pricing` recibe la FUNCION contador (`page=n`), no su valor.
```

- [ ] **Step 3: Actualizar el conteo de README.md**

En `README.md`, seccion "Tipos de diapositiva", cambiar `~25 layouts` por `~26 layouts` y anadir `desglose de presupuesto` a la enumeracion.

- [ ] **Step 4: Verificar ASCII**

Run: `python -c "print(sum(1 for b in open('CLAUDE.md','rb').read() if b>127))"`
Expected: `0`

- [ ] **Step 5: Ejecutar toda la suite una ultima vez**

Run: `python -m pytest tests/ -q`
Expected: PASS (24 passed)

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "Documentar add_pricing en el catalogo de layouts"
```
