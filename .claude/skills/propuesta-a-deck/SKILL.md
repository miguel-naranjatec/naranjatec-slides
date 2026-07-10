---
name: propuesta-a-deck
description: Use when creating or filling in a client deck (content/*.py) for this repo - from a proposal document, a budget, a brief, or from notes. Reads the source document FIRST, judges whether it sustains a commercial argument, derives the slide plan from its content, and asks only what the document cannot contain.
---

# De documento a deck

El documento manda. La IA decide el guion. Se pregunta lo que el documento no
puede contener, y solo eso.

Los dos errores simetricos que este skill evita: **inventarse** una tarifa, una
cifra o un dato de contacto; e **interrogar** al usuario sobre lo que el documento
ya contesta, o pedirle logos y fotos como si esto fuese un presupuesto. Esto genera
una PRESENTACION.

## Paso 1. El documento, siempre lo primero

Antes de cualquier otra pregunta:

> "Antes de nada: tienes un documento de partida (propuesta, presupuesto, brief)?
> Pasame la ruta y lo analizo."

- Ruta a `.md`, `.txt` o `.pdf` -> leerlo ENTERO antes de preguntar nada mas
  (el `.pdf` con la herramienta Read). Un `.docx`: pedir que lo exporten.
- Texto pegado en el chat -> igual.
- No hay documento -> entrevista breve sobre el proyecto, y desde ahi el mismo flujo.

El documento del cliente NO se copia al repo: lleva tarifas internas y datos de
cliente, y este repositorio se distribuye. Se lee donde este.

## Paso 2. El arco, y si el documento lo sostiene

Un deck comercial no es un volcado del documento: es un argumento. La estructura
que se persigue siempre es la misma, aunque los layouts cambien:

**problema -> solucion -> propuesta -> presupuesto -> proximos pasos**

Antes de elegir una sola diapositiva, **valora la viabilidad**: recorre el
documento y decide, acto por acto, si hay material para sostenerlo.

| Acto | Que necesita | Si falta |
|---|---|---|
| Problema | Un dolor concreto del cliente, mejor con una cifra | Casi siempre se puede invertir la solucion ("hacemos X" -> "hoy no tienes X"). Si ni eso, preguntarlo en una frase. |
| Solucion | Que se propone y por que resuelve ese dolor | Es el nucleo. Si falta, el documento no es una propuesta: avisar al usuario y parar. |
| Propuesta | El alcance: que se construye, con que piezas | Si el documento solo trae generalidades, el deck sale flojo. Decirlo, no maquillarlo. |
| Presupuesto | Partidas con importe (o con horas + tarifa) | Se omite el acto. Un deck sin precio es legitimo. |
| Proximos pasos | Que pasa despues de decir que si | Casi nunca esta en el documento. Proponer el proceso estandar (aprobacion, descubrimiento, desarrollo, contenidos, lanzamiento) con `add_next_steps`, y marcarlo como propuesto por la IA. |

**Entrega este juicio ANTES de escribir codigo**, con un veredicto por acto:
cubierto / flojo / ausente. Es lo primero que el usuario ve, y donde se decide si
la propuesta se sostiene o le falta un pilar.

Los actos se separan con `add_section` numerado.

## Paso 3. De contenido a layout

Dentro de cada acto **no hay guion fijo**. `content/nereidas.py` es UN ejemplo, no
la plantilla. El criterio es la FORMA del contenido, no su titulo:

| Lo que hay en el documento | Layout |
|---|---|
| Una idea rotunda, una frase que duele | `add_statement` |
| 5-9 items cortos y paralelos | `add_service_grid` |
| 2-4 items con titular + detalle | `add_bullets`, `add_solution` |
| Dos mundos enfrentados (antes/despues, ellos/nosotros) | `add_two_column`, `add_comparison` |
| Secuencia de hasta 4 pasos | `add_process` |
| Secuencia con fechas | `add_timeline` |
| Cifras que hablan solas | `add_stats`, `add_stats_feature` |
| Un argumento largo con una imagen | `add_image_feature`, `add_mission` |
| Partidas con importe | `add_pricing` |
| Ampliaciones opcionales con precio | `add_extras` |
| Un extra que merece su propia slide | `add_spotlight` |
| Una cita atribuida | `add_quote` |
| Un mensaje del fundador | `add_message` |
| Cambio de tema | `add_section` |
| Cierre con contacto | `add_cta`, `add_thanks` |

Los limites del layout deciden el troceado: 12 servicios no caben en un
`add_service_grid` (max 9), asi que o se agrupan o van en dos slides.

Propon el guion resultante y **ensenaselo al usuario para que lo confirme de un
vistazo** antes de escribir codigo. Confirmar un guion no es interrogar: es una
sola pantalla.

### Variedad

Un deck que repite `add_bullets` seis veces esta mal montado aunque cada slide sea
correcta. Hay mas de 30 layouts en `lib/slides.py`: **el mismo no deberia
repetirse sin una razon**. Alterna el ritmo: denso / respiro (un `add_section`, un
`add_statement`), texto / imagen, claro / navy.

Si dos secciones piden el mismo layout, mira si una admite su primo:
`add_service_grid` / `add_numbered_grid`; `add_stats` / `add_stats_feature`;
`add_bullets` / `add_solution`; `add_image_feature` / `add_mission`;
`add_two_column` / `add_comparison`; `add_cta` / `add_thanks`.

Primero encaja, luego varia. La variedad nunca justifica un layout que no case con
la forma del contenido.

## Paso 4. Los bloques de pagina (el acto "propuesta")

Cuando el documento describe una WEB, la propuesta debe ensenar con que bloques se
va a construir. Es la respuesta visual a "que se construye exactamente".

Ejecuta:

```
python scripts/gen_blocks.py --list
```

Imprime el catalogo (categorias -> slugs) sin escribir nada. **Selecciona los
bloques que el documento justifica**, uno a uno: cada bloque elegido tiene que
poder senalarse en una frase del documento. Nunca los 106. Nunca por sector "a
ojo": no existe la plantilla "inmobiliaria".

| Lo que menciona el documento | Bloques |
|---|---|
| Reservas, citas, disponibilidad | `booking-calendar`, `time-slots`, `multi-step-form` |
| Horario, local fisico | `opening-hours`, `map` |
| Carta, platos, menu | `menu-carta` |
| Tienda, carrito, pago | `shop-catalog`, `product-detail`, `cart`, `checkout` |
| Propiedades, inmuebles | `property-map-list`, `floor-plan`, `cpt-list`, `cpt-detail` |
| Buscador, filtros | `search-featured`, `shop-catalog` |
| Presupuesto en linea, configurador | `price-calculator`, `product-configurator` |
| Cursos, formacion | `lesson-player`, `quiz` |
| Eventos | `event-countdown`, `event-agenda` |
| Blog, noticias | `latest-news`, `news-list` |
| Testimonios, resenas | `testimonials`, `google-reviews`, `ratings-breakdown` |
| Equipo, sobre nosotros | `team-showcase`, `why-us`, `timeline` |
| Preguntas frecuentes | `faq-accordion` |
| Tarifas, planes | `pricing-plans`, `comparison-table` |

Y los que lleva casi cualquier web, salvo que el documento diga lo contrario:
`hero-banner`, `page-header`, `text-image`, `cta-banner`, `footer-columns`,
`contact-methods`, `dynamic-form`, `cookie-consent`.

`add_blocks_grid` pinta 12 por diapositiva y pagina sola: elige 12 o 24, no 17.
El slug debe existir en `brand/assets/blocks/png/`, o el deck revienta al
construirse (no al abrirse).

## Paso 5. La pregunta que nunca se salta: la tarifa

**Solo si el documento trae las partidas en horas, jornadas o puntos.** Entonces:
a que tarifa se convierten a euros? NUNCA inventarla.

Y la regla que la acompana: **horas y euros no conviven en el mismo deck**. Si en
una slide aparecen las horas y en otra los euros, basta dividir para deducir la
tarifa. Ver `content/nereidas.py:210-212`.

El total de `add_pricing` lo suma el layout a partir de las filas, asi que nunca
puede contradecir al desglose. No lo pases a mano.

Si el documento ya viene en euros, aqui no hay nada que preguntar.

## Paso 6. Los huecos: preguntar o cambiar de layout

Nunca inventar el dato. Entre las otras dos salidas, mira de que tipo es el hueco:

**Pregunta** cuando el dato EXISTE y el usuario lo tiene en la cabeza: el telefono
y el email del cierre, una cifra que el documento da por sabida, el nombre de quien
firma una cita. Es un dato, no una tarea.

**Cambia de layout** cuando el dato NO existe: no hay testimonio de cliente, no hay
hitos con fecha, no hay presupuesto. Ahi preguntar es pedirle al usuario que se
invente material.

| Falta | En vez de | Usa |
|---|---|---|
| Testimonio con autor | `add_quote` | `add_statement` |
| Hitos con fecha | `add_timeline` | `add_process` |
| Precios | `add_pricing` | omitir la slide |
| Cifras duras | `add_stats` | `add_bullets`, `add_service_grid` |

Todas las preguntas de los pasos 5 y 6 van **juntas, en una sola ronda**, al
terminar el analisis. Nunca goteando.

La imagen es la excepcion: **no se pide nunca**. `brand/assets/img/` es la
biblioteca de imagenes PROPIAS de NaranjaTec (mockups de webs del estudio, fotos
de la oficina): son material legitimo del documento, no relleno provisional. Se
elige de ahi la que encaje y no hay nada que disculpar ni que avisar.

Distinto es que el cliente aporte material suyo (fotos de sus propiedades, de sus
platos, de su equipo): entonces vende mas y se usa. Pero eso lo trae el, no se
pide como requisito para generar el deck.

## Paso 7. Escribir el deck

`content/<alias>.py` con `OUTFILE`, `TITULO` y `build(prs)`, con el contador
`p = [0]` / `n()`. Registra el alias en el dict `DECKS` de `build/build.py`.

Copy de presentacion, no parrafos del documento. **UTF-8 con acentos y ene
reales**: es un entregable para cliente. El codigo y los comentarios, ASCII puro.

Limites duros que hacen perder contenido en silencio:

- `add_bullets` pinta 4 como maximo: trunca sin avisar.
- `add_process` es 2x2 (4). `add_service_grid` llega a 9.
- `add_pricing` acepta 10 partidas (mas -> `ValueError`) y recibe el CONTADOR
  (`page=n`), no su valor. Igual `add_blocks_grid`.
- `add_timeline`, `add_pricing` y `add_blocks_grid` devuelven una LISTA de slides.
- `add_next_steps` admite de 3 a 5 pasos. `add_extras`, de 2 a 4.

## Paso 8. Verificar

```
python build/build.py <alias>
python -m pytest tests/ -q
```

Y mirar las diapositivas: exportar a PNG (PowerPoint COM en Windows, LibreOffice
headless en Linux). El build solo escribe el fichero; que el deck se lea bien no
lo comprueba nadie mas.

Al terminar, di que imagenes de la biblioteca has elegido y por que, por si alguna
no encaja con el cliente.
