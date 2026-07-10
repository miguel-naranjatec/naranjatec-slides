# Biblioteca de bloques v2: 43 esquemas nuevos

Fecha: 2026-07-10
Estado: aprobado, pendiente de implementar

## Problema

`brand/assets/blocks/` tiene 64 esquemas de bloque de pagina (SVG generados por
`scripts/gen_blocks.py`, rasterizados a PNG por `scripts/make_blocks.py`). Cubren
el esqueleto de una web corporativa con tienda: portada, contenido base, confianza,
contenidos gestionables (CPT), WooCommerce, multimedia, blog, conversion y
organizacion de la informacion.

Faltan familias enteras que NaranjaTec vende de hecho y que hoy no se pueden
ensenar en un deck: reservas y calendarios, calculadoras y configuradores,
inmobiliaria, restauracion, formacion, eventos, y los patrones de maquetacion
modernos (bento, masonry, marquee).

## El criterio: silueta unica

Un esquema se lee a 2 cm de ancho. A ese tamano solo comunica su SILUETA: la
geometria gruesa, no el detalle. De ahi salen las dos reglas que ordenan este
trabajo:

1. **Un bloque es una seccion de pagina, no una pagina.** Un 404, una pagina de
   gracias o un panel de usuario no son bloques: son el sitio donde se meten
   bloques. Quedan fuera.
2. **Si dos bloques dibujan la misma silueta, sobra uno.** No importa que se
   vendan distinto. `speakers-grid` dibuja exactamente `team-showcase`;
   `event-list` dibuja `news-list`; `ticket-tiers` dibuja `pricing-plans`. Un
   catalogo visual con entradas que se confunden entre si es peor que un catalogo
   mas corto.

Aplicando el filtro a una lista inicial de 64 candidatos, sobreviven 43. No se
fuerza el numero: mejor 43 distinguibles que 64 con relleno.

Descartes por colision con los 64 existentes, para memoria futura:
`filters-sidebar` es `shop-catalog`; `sticky-scroll` es `text-image`;
`parallax-band` es `full-width-band`; `reservation-form` es `dynamic-form`;
`virtual-tour` es `gallery-carousel`; `staff-picker` y `staff-directory` son
`team-showcase`; `dish-grid` y `pagination-grid` son `card-grid`;
`metrics-cards` es `kpis`; `breadcrumbs-bar` es `page-header`; `menu-tabs` es
`tabs-accordion`; `curriculum` es `faq-accordion`; `course-grid` es
`latest-news`; `specialties-grid` es `why-us`; `instructor-profile` es
`text-image`; `roi-chart` es `stats-chart`; `mortgage-simulator` es
`price-calculator`; `daily-menu` es `menu-carta`; `sticky-cta-bar` es
`cookie-consent`; `empty-state` no llega a tener maquetacion.

## Los 43 bloques

Entre parentesis, la geometria que lo hace inconfundible.

### Navegacion y chrome (5)
- `nav-bar` - logo + menu + boton, cintado arriba
- `mega-menu` - nav + panel desplegado a columnas con foto
- `footer-columns` - 4 columnas + barra legal
- `table-of-contents` - indice fino con marca activa + cuerpo
- `cookie-consent` - pagina atenuada + barra inferior con dos botones

### Reservas y horarios (4)
- `booking-calendar` - rejilla 7x5 de dias, uno en dorado
- `time-slots` - columnas de pildoras por dia
- `opening-hours` - filas dia/hora con reloj, hoy en dorado
- `multi-step-form` - barra de pasos numerada + formulario + resumen lateral

### Configuracion y precio (2)
- `price-calculator` - sliders + cifra grande
- `product-configurator` - preview + muestras de color + tallas

### Datos (5)
- `stats-chart` - barras verticales + eje
- `donut-stats` - anillos parciales
- `progress-bars` - barras horizontales etiquetadas
- `data-table` - cabecera navy + zebra + paginacion
- `comparison-table` - checks + columna destacada

### Inmobiliaria (3)
- `property-map-list` - listado izq + mapa der
- `property-features` - iconos con cifra (m2, habitaciones, banos)
- `floor-plan` - plano de estancias

### Restauracion (1)
- `menu-carta` - dos columnas unidas por puntos de precio

### Formacion (2)
- `lesson-player` - video + lista lateral de lecciones con progreso
- `quiz` - pregunta + opciones con radio + barra de progreso

### Eventos (2)
- `event-countdown` - 4 cajas de cuenta atras
- `event-agenda` - columna de horas + franjas

### Comercio (3)
- `product-zoom` - miniaturas verticales + imagen + lupa
- `size-guide` - tabla + silueta
- `seat-picker` - filas curvas de asientos + pantalla

### Comunidad y conversacion (4)
- `comments-thread` - burbujas indentadas
- `chat-panel` - burbujas alternas + campo de entrada
- `ratings-breakdown` - 5 barras, una por estrella
- `ai-search` - barra + bloque de respuesta + chips de fuente

### Medios e interaccion (3)
- `audio-player` - onda de sonido + play
- `hotspot-image` - puntos numerados sobre foto
- `file-upload` - zona punteada con flecha

### Estructuras (8)
- `bento-grid` - celdas de tamanos desiguales
- `masonry-grid` - columnas de alturas desiguales
- `marquee-band` - cinta de pildoras cortada por ambos bordes
- `timeline-vertical` - linea vertical con hitos alternos
- `split-screen` - mitad foto a sangre, mitad panel
- `horizontal-scroll` - tarjetas cortadas + barra de arrastre
- `org-chart` - arbol con conectores
- `roadmap-gantt` - carriles con barras

### Directorio (1)
- `directory-az` - indice A-Z + columnas de nombres

Total biblioteca: 64 + 43 = **107**.

## Cambios en el codigo

### `scripts/gen_blocks.py`

Primitivas nuevas, en el mismo bloque de primitivas compartidas y con el mismo
lenguaje visual (NAVY de trazo, GOLD para el elemento activo, MUTE para texto
sugerido, LIGHT para rellenos):

| Primitiva | Dibuja | La usan |
|---|---|---|
| `bar(x, y, w, h, fill)` | barra vertical de grafico | `stats-chart` |
| `donut(cx, cy, r, frac)` | anillo parcial via `<path>` con arco | `donut-stats` |
| `slider(x, y, w, frac)` | rail + tirador dorado | `price-calculator` |
| `checkbox(x, y, on)` | casilla, marcada o no | `comparison-table`, `size-guide` |
| `radio(cx, cy, on)` | circulo de opcion | `quiz` |
| `avatar(cx, cy, r)` | circulo de persona | `comments-thread`, `chat-panel` |
| `chip(x, y, w)` | pildora de filtro / etiqueta | `marquee-band`, `ai-search` |
| `cal_grid(x, y, w, h, active)` | rejilla 7xN de dias | `booking-calendar` |
| `wave(x, y, w, h)` | onda de audio (barras de alturas variables) | `audio-player` |
| `pin(cx, cy)` | chincheta de mapa | `property-map-list` |
| `chevron(cx, cy, dir)` | punta de flecha | `horizontal-scroll`, `mega-menu` |

`donut` necesita un arco SVG de verdad (`A rx ry 0 laf 1 x y`), calculado con
`math` a partir de la fraccion. Es la unica primitiva con trigonometria ademas de
`star`.

### Categorias como dato

Hoy las categorias son comentarios dentro del dict `BLOCKS`. Pasan a ser dato,
para poder filtrar ("solo inmobiliaria") al montar un deck de cliente:

```python
CATALOGO = [
    ("Portada y cabeceras", {"hero-banner": _hero, ...}),
    ("Reservas y horarios", {"booking-calendar": _booking_calendar, ...}),
    ...
]
BLOCKS = {slug: fn for _, grupo in CATALOGO for slug, fn in grupo.items()}
```

`BLOCKS` sigue existiendo con la misma forma, asi que `main()` y todo lo que lo
consuma no cambia. `CATALOGO` es aditivo.

### `scripts/make_blocks.py`

Sin cambios: rasteriza lo que encuentre en `brand/assets/blocks/*.svg`.

### `brand/theme.py`

Sin cambios: `T.block(slug)` ya resuelve cualquier PNG.

### `content/muestrario.py`

Correccion de un supuesto: el muestrario NO pinta los 64 bloques, pasa 12
seleccionados a `add_blocks_grid` (una sola diapositiva). No tiene sentido volcar
107 en el deck de test.

Se anade UNA segunda llamada con 24 bloques nuevos representativos, que ademas
ejercita la paginacion (24 / 12 = 2 diapositivas) con datos reales, no solo en el
test unitario. Nombres y descripciones en ASCII puro: es el deck de test.

### Tests (`tests/test_layouts.py`)

El test de paridad SVG/PNG cuenta dinamicamente, asi que cubre los 43 nuevos sin
tocarlo. Se anaden dos:

- `test_slugs_unicos`: ningun slug repetido entre grupos de `CATALOGO` (un dict
  por grupo no lo impide; el `BLOCKS` derivado se comeria el duplicado en
  silencio y perderiamos un bloque sin que nadie se entere).
- `test_todo_bloque_tiene_categoria`: `len(BLOCKS) == sum(len(g) for _, g in CATALOGO)`.

## Riesgos y como se mitigan

- **Rasterizado**: `make_blocks.py` usa Edge headless. 43 PNG mas es mas tiempo,
  no mas riesgo. Si un SVG sale vacio, el test de paridad no lo detecta (el PNG
  existe, transparente). Mitigacion: comprobar a ojo la hoja de contactos en el
  deck, que es justo para lo que sirve `add_blocks_grid`.
- **Colision de silueta no detectada**: no hay forma automatica de comprobarlo.
  La lista de descartes de arriba queda escrita para que el proximo que anada un
  bloque compare antes.
- **`python-pptx` no acepta SVG**: ya resuelto por el pipeline SVG -> PNG. Un
  bloque nuevo sin rasterizar revienta el build, no la apertura del `.pptx`.

## Fuera de alcance

- Soporte, chat flotante, redes sociales e IA como *widgets*: casi todos son
  elementos flotantes, no layouts. `chat-panel` y `ai-search` entran porque su
  esquema si es una seccion con geometria propia.
- Filtrar el catalogo por categoria al construir un deck: `CATALOGO` deja la
  puerta abierta, pero no se implementa ningun helper hasta que haga falta.
