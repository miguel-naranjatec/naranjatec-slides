# add_pricing: layout de desglose de presupuesto

Fecha: 2026-07-09
Estado: aprobado, pendiente de implementar

## Problema

`lib/slides.py` no tiene ningun layout para presentar un presupuesto: partidas con
importe, total y nota al pie. En un deck de cliente esto ya dolio: el desglose
de 5 partidas hubo que fusionarlo a 4 para meterlo en `add_bullets`, que pinta
`bullets[:4]` y descarta el resto en silencio.

Referencia aportada por el usuario: una diapositiva "Overzicht van de kosten" con
tres partidas numeradas a la izquierda (concepto + importe) y una tarjeta de total
a la derecha, sobre fondo oscuro, con una nota al pie en cursiva.

## Alcance

Un solo layout nuevo, `add_pricing`, en `lib/slides.py`. Sin cambios en
`brand/theme.py`. Una diapositiva de ejemplo en `content/muestrario.py`.

Fuera de alcance: rehacer el desglose del deck de cliente (se hara despues,
como cambio de contenido aparte).

## API

```python
add_pricing(prs, title, rows, note="", total=None, subtitle="", page=None, section="")
```

| Parametro  | Tipo | Descripcion |
|------------|------|-------------|
| `title`    | str  | Titulo. Admite marcado `*enfasis*` (Playfair italica). |
| `rows`     | list | `[(concepto, importe), ...]`. `importe` es `int` o `float`. Maximo 10. |
| `note`     | str  | Nota al pie. Se pinta solo en la ultima pagina. Opcional. |
| `total`    | None / str | `None` (por defecto): el total es la suma de `rows`. Si se pasa un `str`, se usa tal cual (p.ej. `"A convenir"`). |
| `subtitle` | str  | Subtitulo serif bajo el titulo. Opcional. |
| `page`     | callable | El CONTADOR, no su valor: `page=n`, no `page=n()`. Se invoca una vez por pagina generada. |
| `section`  | str  | Etiqueta de la barra superior. |

Devuelve **siempre una lista de slides**, aunque solo genere una. Devolver a veces
un slide suelto y a veces una lista romperia al llamante justo cuando el
presupuesto crece y pasa de una pagina a dos.

## Paginacion

- `len(rows) <= 5` -> **una** pagina: filas a la izquierda (60% del ancho),
  tarjeta de total a la derecha.
- `6 <= len(rows) <= 10` -> **dos** paginas, con reparto equilibrado
  (`ceil(n/2)` en la primera): 6 -> 3+3, 7 -> 4+3, 10 -> 5+5. Ambas paginas
  quedan asi con 5 filas o menos.
  - Primera pagina: filas a **ancho completo**, sin tarjeta. Sin nota al pie.
  - Ultima pagina: filas a la izquierda + tarjeta de total a la derecha + nota.
- `len(rows) > 10` -> `ValueError`.
- `rows` vacia -> `ValueError`.

**Por que `ValueError` y no truncar.** `add_bullets` hace `bullets[:4]` en
silencio. Que se pierda una vineta es un fallo de maquetacion; que se pierda una
partida de un presupuesto es un error de negocio que llega al cliente. El build
debe romper.

## Importes

Los importes son numeros y el total se calcula sumandolos. Asi el total no puede
contradecir al desglose cuando alguien edita una partida y se olvida del total.

Formato `es-ES`: separador de miles `.`, decimales `,`, y el simbolo del euro al
final separado por un espacio normal.

- `int`, o `float` con parte decimal nula -> sin decimales: `1300` -> `1.300 EUR`
- `float` con decimales -> dos decimales: `1300.5` -> `1.300,50 EUR`

(Arriba se escribe `EUR` porque este documento tambien es ASCII. Lo que se pinta
en la diapositiva es el simbolo del euro.)

En el codigo el euro se escribe como el escape `\u20AC`, NUNCA como
caracter literal: `lib/slides.py` es ASCII puro (misma regla que los glifos PUA de iconos).

`total=` acepta solo `None` o `str`. Un `str` se pinta tal cual y se salta el
formateo (caso `"A convenir"`). No se acepta un numero en `total=`: si el total
fuese un numero distinto de la suma, tendriamos otra vez el bug que este diseno
evita.

## Composicion visual

Fondo `T.BG` (blanco calido), como el resto de slides de contenido. El navy queda
reservado a separadores, statement y CTA.

**Fila** (tarjeta blanca que flota, `_rect` + `_soft_shadow`, radio 0.06):
- Chip circular navy (`T.AZUL_OSCURO`) a la izquierda, con el ordinal en
  `T.FONT_NUM` dorado. Se reutiliza el helper `_letter_badge()`, que ya dibuja un
  circulo con un caracter centrado; si le falta el color de texto, se le anade el
  parametro en vez de duplicar el helper.
- Concepto en `T.FONT_HEAD`, `T.AZUL_OSCURO`.
- Importe alineado a la derecha, en `T.FONT_NUM`, `T.AZUL_OSCURO`.

**Tarjeta de total** (solo en la ultima pagina, columna derecha, alto del bloque
de filas): fondo `T.AMARILLO`, radio 0.08.
- Etiqueta `TOTAL ESTIMADO` en `T.FONT_MONO`, tracking, `T.AZUL_OSCURO`.
- Cifra grande en `T.FONT_NUM`, `T.AZUL_OSCURO`.
- Coletilla (`"IVA no incluido"`) en Playfair italica, `T.AZUL_OSCURO`.

Se eligio amarillo por decision del usuario. La alternativa evaluada era `T.AZUL`
(el azul brillante de la referencia); se descarto el navy por repetir el color de
los chips de las filas.

**Nota al pie**: `T.FONT_BODY`, `T.GRIS_SUAVE`, ~10pt, a todo el ancho, por
debajo del bloque de filas. Solo en la ultima pagina.

**Geometria**: `MARGIN = 0.7in`, `CONTENT_W = 11.93in`. El titulo se coloca con
`_title()` y el contenido arranca en
`max(default, titulo_abajo + GAP_AFTER_TITLE)`, como los demas layouts. Las filas
reparten el alto disponible entre el numero de filas de esa pagina, con un hueco
fijo entre ellas.

## Casos borde

| Caso | Comportamiento |
|------|----------------|
| `rows` vacia | `ValueError` |
| `len(rows) > 10` | `ValueError` |
| `total` es un numero | `TypeError` (solo `None` o `str`) |
| `page=n()` en vez de `page=n` | `TypeError` explicito: "page debe ser el contador, no su valor" |
| `page=None` | No se pinta numero de pagina (coherente con el resto) |
| Importe negativo (descuento) | Se pinta con signo y suma normalmente |
| `note=""` | No se reserva espacio para la nota |

## Documentacion a actualizar

- `CLAUDE.md`: entrada en el catalogo de layouts, marcando que es MULTIPAGINA y
  que `page` recibe el contador (la unica excepcion de la libreria, junto a
  `add_timeline`, que directamente no lleva `page`).
- `README.md`: el conteo "~25 layouts" y la lista de tipos.

## Verificacion

1. `python build/build.py test` genera el muestrario con la nueva diapositiva.
2. Exportar a PNG (PowerPoint COM) y revisar: 5 partidas en una pagina, 7 en dos.
3. `python -c "print(sum(1 for b in open('lib/slides.py','rb').read() if b>127))"`
   debe seguir dando 0.
4. Casos borde: 0 partidas, 11 partidas y `page=n()` deben lanzar.
