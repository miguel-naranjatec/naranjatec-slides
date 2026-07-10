# CLAUDE.md - Manual operativo del proyecto

Generador de presentaciones `.pptx` de marca NaranjaTec con `python-pptx`. Este
fichero es el manual para cualquier asistente (Claude Code / Claude Cowork) que
trabaje en el repo: como generar decks, las convenciones y los errores a evitar.

## Que hace y como se genera

Produce `.pptx` editables con la marca aplicada de forma consistente. NO se editan
diapositivas a mano: se escribe un modulo de CONTENIDO en Python (datos) que llama
a los layouts de `lib/slides.py` (maquetacion).

```
python build/build.py <alias>   # genera un deck -> output/<OUTFILE>.pptx
python build/build.py           # genera todos los decks registrados
python build/build.py --list    # lista alias disponibles
```

Alias registrados en `DECKS` (`build/build.py`): `test` (muestrario de todos los
layouts) y `nereidas` (deck de cliente real, ejemplo canonico). Requisitos:
`pip install -r requirements.txt` (solo `python-pptx` + `Pillow`).

## Arquitectura (3 capas)

- `brand/theme.py`  - paleta, tipografia, glifos de icono (`ICON`), medidas,
  `img(nombre)` (resuelve `brand/assets/img/`). FUENTE DE VERDAD de la marca.
- `lib/slides.py`   - libreria de layouts (`add_*`) + helpers privados (`_*`).
- `content/*.py`    - datos de cada deck: define `OUTFILE` (str) y `build(prs)`.
  `templates/*.py` existen pero NO estan registrados en `DECKS`.
- `content/fijas.py` - diapositivas FIJAS (nuestras, no del cliente) y el contacto
  por defecto. Registro `FIJAS`; se listan con `python content/fijas.py --list`.
  No es un deck: no tiene `OUTFILE` ni va en `DECKS`.

Un deck es un modulo con:
```python
import brand.theme as T
import lib.slides as s
OUTFILE = "Mi-Deck.pptx"
def build(prs):
    p = [0]
    def n():                      # contador de numero de pagina
        p[0] += 1; return p[0]
    s.add_cover(prs, title="...", image=T.img("naranjatec-web.jpg"))
    s.add_bullets(prs, "Titulo", [("Head", "detalle", T.ICON["cloud"])],
                  page=n(), section="Ejemplo")
    ...
    return prs
```

## Catalogo de layouts (`lib/slides.py`)

Casi todos aceptan `subtitle=""` (serif Playfair opcional bajo el titulo),
`page=n()` y `section=""` (etiqueta superior derecha). El titulo admite marcado
`*enfasis*` -> la parte entre asteriscos va en Playfair italica.

- `add_cover(prs, title, subtitle="", eyebrow="...", image=None, cta="...", eslogan=...)`
  Portada/hero; imagen opcional a la derecha con marco de acento.
- `add_index(prs, title, items, page=None, highlight=2)`
  Agenda de tarjetas. `items`: `(titulo, desc)` o `(titulo, desc, glyph)`. La
  tarjeta `highlight` se invierte a navy.
- `add_section(prs, text, number="", image=None)`
  Separador de seccion. Con `image=` -> foto a sangre + degradado navy. NO usa page.
- `add_statement(prs, text, image, author="", page=None)`
  Cita a sangre sobre foto + velo, icono bocadillo. Admite `*enfasis*`.
- `add_bullets(prs, title, bullets, image=None, subtitle="", page, section)`
  Lista (chip icono + titulo + detalle) izq, imagen der. `bullets`:
  `(head, detail)` o `(head, detail, glyph)`. **MAXIMO 4 items** (`bullets[:4]`).
- `add_two_column(prs, title, left, right, subtitle="", page, section)`
  Split a todo el alto (claro/navy). `left`/`right`:
  `{"heading","icon","items":[str,...]}`.
- `add_service_grid(prs, title, items, subtitle="", page, section)`
  Rejilla hasta 9 (3x3) sin cajas. `items`: `{"title","desc","icon"}`.
- `add_process(prs, title, steps, page, section)`
  Pasos numerados en rejilla **2x2 (max 4)**. `steps`: `(titulo, desc)`.
- `add_image_feature(prs, title, body, image, stat=None, side="right", subtitle="", page, section)`
  Texto + imagen + dato. `body`: str o lista de parrafos. `stat`: `(valor, etiqueta)`.
- `add_stats(prs, stats, title="", subtitle="", page, section)`
  Cifras en tarjetas que flotan. `stats`: `[{"value","label"}]`.
- `add_quote(prs, quote, author, role="", avatar=None, stars=5, image=None, page, section)`
  Testimonio. Con `image=` -> tarjeta glassmorfista sobre foto (backdrop-blur).
- `add_cta(prs, headline, contact, subtext="", image=None)`
  Cierre. `contact`: `[(icono, valor)]`. Con `image=` -> foto + degradado navy.
- `add_timeline(prs, title, milestones, subtitle="", section="")`
  **MULTIPAGINA**: devuelve una LISTA de slides (una por hito). NO recibe `page`.
  `milestones`: `[{"year","label","icon","text"}]`.
- `add_comparison(prs, title, columns, rows, subtitle="", page, section, highlight=1)`
  Tabla de checks. `columns`: `[str,...]`; `rows`: `[{"label","marks":[bool,...]}]`.
  La columna `highlight` se resalta en navy.
- `add_gallery_list(prs, title, subtitle, items, images, page=None)`
  Lista A/B/C/D + grid de 2 o 4 imgs a sangre. `items`: `[(titular, desc)]`.
- `add_gallery_text(prs, title, heading, body, images, subtitle="", page, section)`
  Parrafo + 3 imgs verticales. `body`: str o lista.
- `add_gallery_mosaic(prs, title, images, subtitle="", page, section)`
  Mosaico 2x2 + 1 grande (5 imgs).
- `add_feature_band(prs, title, features, image, intro="", subtitle="", page, section)`
  Banda de imagen (velo) + 4 columnas. `features`: `[{"icon","head","text"}]`.
- `add_mission(prs, title, features, image, caption_title, caption_text, page, section)`
  Features izq + imagen con pie navy der.
- `add_numbered_grid(prs, title, items, highlight="", page, section)`
  01-04 en 3 columnas + declaracion resaltada dorada. `items`: `[(titulo, texto)]`.
- `add_thanks(prs, headline, contact, image, page=None)`
  Cierre "gracias" sobre foto + panel. `contact`: `[(icono, label, valor)]`
  (OJO: 3-tupla, distinto de `add_cta` que usa 2-tupla).
- `add_hero_card(prs, title, body, cta, image, page=None)`
  Foto a sangre + tarjeta clara con boton pill al pie.
- `add_value_cards(prs, title, image, cards, subtitle="", page, section)`
  Imagen alta izq + titulo dcha + 3 tarjetas de acento abajo. `cards`:
  `{"head","text"}` o `{"value","label"}` (tarjeta-cifra).
- `add_overview(prs, title, subhead, body, points, images, subtitle="", page, section)`
  Texto + 2 imgs apiladas + 2 puntos numerados. `points`: `[(head, text)]`.
- `add_product(prs, title, stat, kicker, rows, page, section)`
  Titulo + cifra + kicker izq; filas titulo/imagen/parrafo dcha.
  `rows`: `[{"head","text","image","desc"}]`.
- `add_pricing(prs, title, rows, note="", total=None, subtitle="", page=n, section="")`
  Desglose de presupuesto: partidas numeradas + importe, tarjeta de total amarilla
  y nota al pie. `rows`: `[(concepto, importe)]`, importe numerico, **MAXIMO 10**
  (mas -> `ValueError`, NO trunca como `add_bullets`). El total se SUMA solo;
  `total=` solo acepta un `str` para forzar texto ("A convenir").
  **MULTIPAGINA**: con 6-10 partidas genera 2 slides (la 1a a ancho completo, sin
  tarjeta); el total Y la nota al pie van solo en la ultima. Devuelve SIEMPRE una
  lista. `page` recibe el CONTADOR (`page=n`), no su valor (`page=n()`): unica
  excepcion de la libreria.
- `add_stats_feature(prs, title, stats, image, subtitle="", page, section)`
  Cifras destacadas: rejilla 2x2 de tarjetas (circulo de icono + cifra grande +
  descripcion) izq y foto a sangre en la mitad dcha. `stats`:
  `{"value","label","icon"}`, de 2 a 4. Version rica de `add_stats`, que sigue
  existiendo para la banda de cifras sin foto.
- `add_extras(prs, title, extras, subtitle="", page, section)`
  Productos adicionales: 2-4 tarjetas altas con foto + velo navy, icono, precio
  grande (con `+` delante), nombre y descripcion corta. `extras`:
  `{"price": 375, "name", "desc", "icon", "image"}`. `price` es NUMERICO (lo
  formatea `_fmt_eur`); `image` es opcional (sin ella, tarjeta navy solida).
  Fuera de 2-4 -> `ValueError`.
- `add_solution(prs, title, points, images, subtitle="", highlight=None, page, section)`
  Dos fotos solapadas izq + 2-4 puntos dcha (circulo de icono + titular + texto).
  `points`: `[(titular, texto, glyph)]`. `highlight=i` eleva ese punto sobre una
  pildora blanca. `images`: DOS rutas. Fuera de 2-4 puntos -> `ValueError`.
- `add_message(prs, eyebrow, title, image, lead, body, author, role="", page, section)`
  Mensaje destacado a 3 columnas: antetitulo + titular + firma izq, foto vertical
  a sangre en el centro (con comillas doradas grandes), entradilla en negrita
  (`lead`) + cuerpo (`body`: str o lista) dcha.
- `add_blocks_grid(prs, title, blocks, subtitle="", page=n, section="")`
  Catalogo de bloques de pagina: 12 por diapositiva (4x3), cada tarjeta con el
  esquema del bloque, su nombre y una descripcion muy corta.
  `blocks`: `[(slug, nombre, descripcion)]`; `slug` es el nombre del SVG de
  `brand/assets/blocks/` (106 disponibles, agrupados por categoria en el
  `CATALOGO` de `scripts/gen_blocks.py`). **MULTIPAGINA**: devuelve SIEMPRE una
  lista y `page` recibe el CONTADOR (`page=n`), como `add_pricing`.
- `add_next_steps(prs, title, steps, subtitle="", page, section)`
  Proximos pasos: 3-5 circulos amarillos (icono navy) unidos por arcos elipticos
  grises que alternan arriba y abajo, con punta de flecha; debajo, numero,
  titular y descripcion. `steps`: `[(titular, texto, glyph)]`. Fuera de 3-5 ->
  `ValueError`. Los arcos son formas libres (`_arc_band`): python-pptx no tiene
  arco grueso. La altura del titular se MIDE (`_line_count`) y se reserva la del
  mas largo, para que un titular de dos lineas no pise su descripcion.
- `add_spotlight(prs, title, body, image, cta="", price=None, page, section)`
  Extra destacado: foto grande dcha + panel navy izq que la solapa, con titulo,
  parrafos y boton blanco con flecha. `body`: str o lista. `cta`: texto del boton.

## Convenciones de contenido

- Enfasis en titulos: `"Un desarrollo *a medida*"` -> "a medida" en Playfair italica.
- Imagenes: `T.img("nombre.jpg")` (relativo a `brand/assets/img/`; lanza error si
  no existe). Fotos de oficina reales en `T.img("oficina/naranjatec_XXXX.jpg")`.
- Iconos de linea: `T.ICON["cloud"]`, `["shield"]`, `["globe"]`, etc. (ver el dict
  `ICON` en `brand/theme.py`). Fuente `Material Symbols Outlined 300` (Google,
  congelada a peso 300 con `scripts/make_icon_font.py`, bundled en
  `brand/assets/fonts/Material_Icons/`). Las estrellas de valoracion de
  `add_quote` se dibujan como forma nativa rellena (`MSO_SHAPE.STAR_5_POINT`).
  Para anadir un icono nuevo: buscar su nombre en el `.codepoints`, anadirlo al
  dict `ICON_NAMES` de `scripts/make_icon_font.py` y regenerar.
- Subtitulos serif: pasar `subtitle="..."` (Playfair italica) en los layouts que lo
  aceptan.
- Numero de pagina: usar un contador `n()` como en los ejemplos; los separadores
  de seccion y `add_timeline` NO llevan `page`. Unica excepcion inversa:
  `add_pricing` recibe la FUNCION contador (`page=n`), no su valor (`page=n()`).

## Regla de codificacion (IMPORTANTE)

- **Codigo, comentarios y el deck de TEST (`content/muestrario.py`): ASCII puro.**
  Sin acentos, sin ene, sin BOM, sin comillas tipograficas ni guiones em/en.
- **Decks de CLIENTE (p.ej. `content/nereidas.py`): acentos y ene REALES** (UTF-8
  sin BOM, comillas rectas `"` `'`, guiones normales `-`). Es un entregable: el
  espanol debe estar bien escrito.
- Glifos de icono / PUA (rango U+E000-U+F8FF) SIEMPRE como escape `\uXXXX` en el
  codigo, NUNCA el caracter literal (rompe el ASCII y se manglea al editar). Ej.:
  estrella rellena = `"\uE735"`.
- Verificar ASCII de un fichero de codigo:
  `python -c "print(sum(1 for b in open('lib/slides.py','rb').read() if b>127))"`
  (debe dar 0).

## Gotchas (errores frecuentes)

- **PowerPoint bloquea el `.pptx` abierto**: al reconstruir da `PermissionError`.
  Solucion: cerrar el archivo, o guardar a una ruta temporal para verificar.
- **`python-pptx` NO acepta SVG** (`UnidentifiedImageError`). Los esquemas de
  bloque viven como SVG en `brand/assets/blocks/` (la fuente portable: sirve para
  web o Figma) y se rasterizan a PNG transparente con `scripts/make_blocks.py`
  (Edge headless; no hay cairosvg ni inkscape aqui). Los SVG los ESCRIBE
  `scripts/gen_blocks.py`: no editarlos a mano. Flujo: editar `gen_blocks.py` ->
  `python scripts/gen_blocks.py` -> `python scripts/make_blocks.py`.
- **Un bloque nuevo debe tener SILUETA PROPIA**: el esquema se lee a 2 cm, donde
  solo comunica su geometria gruesa. Si dibuja lo mismo que otro, sobra (da igual
  que se venda distinto). Y un bloque es una SECCION, no una pagina: un 404 o un
  panel de usuario no entran. Ninguna de las dos reglas se puede automatizar:
  hay que RASTERIZAR y mirar la hoja de contactos antes de darlo por bueno. La
  lista de descartes esta en `docs/superpowers/specs/2026-07-10-bloques-v2-design.md`.
- **Cajas de alto/ancho <= 0 corrompen el .pptx**: `python-pptx` las escribe sin
  quejarse y luego PowerPoint dice "no puede abrir el archivo" (python-pptx si lo
  abre, lo que despista). Suele venir de restar dos posiciones y que salga
  negativo. `_rect` y `_text` llaman a `_check_box`, que revienta el build con la
  medida culpable en pulgadas. NO desactivarlo.
- **PowerPoint NO recarga solo**: tras regenerar, hay que cerrar y reabrir para ver
  los cambios (si el usuario "no ve" el cambio, suele ser esto o el bloqueo).
- `add_bullets` pinta como maximo 4 items; `add_process` es 2x2 (4). Para mas
  elementos, usar `add_service_grid` (hasta 9) o dividir.
- **Glassmorphism** (tarjeta translucida): solo funciona SOBRE FOTO, con
  `_glass_card` (simula backdrop-blur recortando la foto de fondo y aplicando
  `a:blur`). Sobre fondo solido queda lavado: no usar.
- `python-pptx` 1.x NO tiene `pptx.enum.line`; el dash se pone via XML crudo.

## Verificacion visual

- El build solo escribe el `.pptx`; abrirlo en PowerPoint es la comprobacion real.
- En Windows con PowerPoint se puede exportar a PNG via COM (PowerShell) para
  revisar sin abrir; en Linux/cloud (p.ej. Cowork) usar LibreOffice headless
  (`soffice --headless --convert-to pdf output/<archivo>.pptx`) tras instalar las
  fuentes de `brand/assets/fonts/` en el sandbox.
- Para fidelidad tipografica, las 4 familias de marca deben estar instaladas en la
  maquina que ABRE el deck (ver `brand/assets/fonts/README.md`). Sin ellas,
  PowerPoint sustituye y el deck sigue funcionando.

## Crear un deck nuevo

1. Crea `content/mi_deck.py` con `OUTFILE` y `build(prs)` (copia `content/nereidas.py`
   como referencia).
2. Registra el alias en el dict `DECKS` de `build/build.py`.
3. Genera con `python build/build.py mi_deck`.

## Flujo "documento -> deck" (para decks de cliente)

**Usa el skill `propuesta-a-deck`** (`.claude/skills/propuesta-a-deck/SKILL.md`):
lleva el proceso entero y, sobre todo, las preguntas que NO se pueden saltar. En
resumen:

1. Preguntar primero si hay documento de partida (`.md`, `.txt`, `.pdf`) y leerlo
   ENTERO antes de nada. No se copia al repo: lleva tarifas y datos de cliente.
2. Valorar si el documento sostiene el arco **problema -> solucion -> propuesta ->
   presupuesto -> proximos pasos**, y entregar ese juicio (cubierto / flojo /
   ausente por acto) ANTES de escribir codigo.
3. Elegir los layouts por la FORMA del contenido, no por su titulo, buscando
   variedad. No hay guion fijo: `content/nereidas.py` es un ejemplo, no la plantilla.
4. UNA sola ronda de preguntas, antes de generar nada: (a) que diapositivas FIJAS
   se incluyen (checkbox; `python content/fijas.py --list`); (b) idioma, por
   defecto el del documento; (c) tono, ofreciendo 2-3 deducidos del documento y
   marcando por defecto "el del documento"; (d) tarifa y contacto. Las fijas se
   importan de `content/fijas.py`, no se copian, y se traducen en la llamada.
5. Elegir los bloques de pagina que el documento justifica, uno a uno
   (`python scripts/gen_blocks.py --list`). Nunca los 106, nunca por sector.
6. Si el documento trae HORAS, preguntar la tarifa: nunca inventarla. Y horas y
   euros no conviven en el mismo deck (se deduce la tarifa dividiendo).
7. Los huecos: preguntar cuando el dato existe y el usuario lo tiene (un telefono);
   cambiar de layout cuando el dato no existe (no hay testimonio -> no `add_quote`).
   Nunca inventarlo. Todas las preguntas, en una sola ronda.

Imagenes: `brand/assets/img/` es la biblioteca PROPIA de NaranjaTec (mockups de
webs del estudio, fotos de la oficina). Es material legitimo del documento, no
relleno provisional: se elige la que encaje y no hay nada que disculpar. Nunca se
piden logos ni fotos al usuario. Si el cliente aporta material suyo, mejor, pero
no es requisito para generar el deck.

## Marca (resumen)

Amarillo `#FFCD33`, azul `#1099ED`, azul profundo `#0B3D66`, acento naranja
`#FF9E2C`. Tipografia: titulos Google Sans (enfasis Playfair Display italica),
cuerpo Instrument Sans, mono/botones Geist Mono, iconos Material Symbols Outlined 300. Fondo
blanco calido `#FAF9F6`, tarjetas blancas con sombra suave que "flotan". Todo
centralizado en `brand/theme.py`.
