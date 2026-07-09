# Presentaciones NaranjaTec

Sistema para generar presentaciones PowerPoint (`.pptx`) editables con la marca de
NaranjaTec. Los archivos se producen con `python-pptx`, aplicando de forma
consistente la paleta, la tipografia y el logo de la empresa.

> Para asistentes de IA (Claude Code / Claude Cowork) hay un manual operativo
> detallado en [`CLAUDE.md`](CLAUDE.md): catalogo de layouts, convenciones,
> codificacion y gotchas.
>
> Para dar la herramienta a un companero de equipo, ver
> [`DISTRIBUTION.md`](DISTRIBUTION.md).

## Empezar aqui

**El `.pptx` no es la fuente, es el resultado.** La fuente es el modulo de
`content/`. Si abres el deck en PowerPoint, retocas un titulo a mano y despues se
regenera, ese retoque se pierde. Los cambios se piden en el contenido y se
vuelve a generar; el deck se edita a mano solo cuando ya es la version final.

Puesta a punto, una sola vez:

```
git clone https://github.com/miguel-naranjatec/naranjatec-slides.git
cd naranjatec-slides
pip install -r requirements.txt
```

Instala ademas las 4 familias de marca y la fuente de iconos (ver
`brand/assets/fonts/README.md`). Sin ellas el deck se genera igual, pero la
tipografia se sustituye y **los iconos salen como cajas**.

Despues, genera el muestrario para ver de que dispones:

```
python build/build.py test
```

Trabajando con IA (Claude Cowork), el ciclo habitual es: le das el brief o el
`.md` de la propuesta, pide "monta un deck de NaranjaTec con esto", y el
asistente escribe el modulo de `content/` siguiendo [`CLAUDE.md`](CLAUDE.md).
Revisas el resultado y pides los cambios en lenguaje natural.

Que tocar y que no:

- `content/` es tuyo: son datos, no logica.
- `lib/slides.py` es maquetacion compartida y `brand/theme.py` es la marca. Un
  cambio ahi afecta a TODOS los decks: es una decision deliberada.
- Topes que sorprenden: `add_bullets` pinta como maximo 4 elementos y
  `add_process` es una rejilla 2x2 (tambien 4). Si el contenido no cabe, fusiona
  o cambia de layout (`add_service_grid` admite 9).
- Un tercer tope que revienta en vez de recortar: `add_pricing` admite un maximo
  de 10 partidas; mas alla lanza `ValueError` en lugar de truncar en silencio.
- Codificacion: el codigo y el deck de test van en ASCII puro; los decks de
  cliente llevan acentos y ene reales, porque son entregables.

## Requisitos

- Python 3.10 o superior (probado con 3.14).
- Dependencias (solo dos):

```
pip install -r requirements.txt
```

Tipografia de marca (4 familias, todas gratuitas OFL, `.ttf` incluidos en
`brand/assets/fonts/`): titulos **Google Sans** (con enfasis en **Playfair
Display** italica), cuerpo **Instrument Sans**, botones/mono **Geist Mono**. Los
iconos usan **Material Symbols Outlined 300** (Google, multiplataforma Windows/Mac). Para
ver el deck con la tipografia correcta, instala las fuentes en la maquina que lo
ABRE (ver `brand/assets/fonts/README.md`). Si no estan, PowerPoint sustituye por
otra sans y las presentaciones siguen funcionando (los iconos si necesitan la
fuente instalada para verse).

## Generar presentaciones

```
python build/build.py test       # muestrario: un ejemplo de cada tipo de slide
python build/build.py nereidas   # deck de cliente (propuesta de web, ejemplo real)
python build/build.py            # genera TODOS los decks registrados
python build/build.py --list     # lista los alias disponibles
```

Los `.pptx` se guardan en `output/` y se abren y editan en PowerPoint o Google
Slides como cualquier presentacion normal.

> Nota: PowerPoint bloquea el archivo mientras lo tienes abierto (al regenerar da
> `PermissionError`) y no recarga solo: cierra y reabre para ver los cambios.

## Previsualizar sin PowerPoint

En entornos sin PowerPoint (Claude Cowork, Linux, CI) se puede revisar el deck
con LibreOffice headless: convierte a PDF y rasteriza una imagen por pagina.

```
python scripts/preview.py --install-fonts   # una vez (Linux/macOS)
python scripts/preview.py test              # genera el deck y lo previsualiza
python scripts/preview.py nereidas --dpi 120
python scripts/preview.py output/Otro.pptx --pdf-only
```

Los PNG quedan en `output/preview/<nombre-del-deck>/`. Requiere LibreOffice
(`libreoffice-impress`) y, para los PNG, `pdftoppm` (`poppler-utils`); si falta
poppler, el script se queda en el PDF y lo avisa.

LibreOffice no es PowerPoint: la conversion es fiel para revisar composicion,
recortes y desbordes de texto, pero puede desviarse en detalles finos. La
verificacion definitiva sigue siendo abrir el `.pptx`.

## Estructura

```
brand/theme.py          Paleta, tipografia, iconos, medidas y helper de imagenes (fuente de verdad)
brand/assets/logo*.png  Logo de color y version blanca
brand/assets/fonts/     Las 4 familias de marca (.ttf) + README de instalacion
brand/assets/img/       Biblioteca de imagenes del proyecto (portable, optimizadas)
lib/slides.py           Libreria de maquetacion (layouts add_* + helpers)
content/                Contenido de cada deck (datos, no logica)
  muestrario.py         Muestrario con un ejemplo de cada tipo de diapositiva (alias: test)
  nereidas.py           Deck de cliente real: propuesta de web (alias: nereidas)
templates/              Plantillas de arranque (NO registradas en DECKS por defecto)
build/build.py          Generador: compone contenido + maquetacion y guarda el .pptx
scripts/preview.py      Previsualizacion sin PowerPoint (LibreOffice headless -> PNG)
output/                 Presentaciones generadas (no se versionan)
```

## Tipos de diapositiva

`lib/slides.py` ofrece ~32 layouts: portada, indice, separadores, statement,
vinetas, dos columnas, rejilla de servicios, proceso, texto+imagen, cifras,
timeline (multipagina), comparativa, galerias, banda de features, mision, rejilla
numerada, testimonio, cifras destacadas, valores, resumen, producto, desglose de presupuesto,
productos adicionales, extra destacado, solucion, mensaje destacado,
proximos pasos, hero,
cierres/CTA, etc. El catalogo completo con la firma de cada uno esta en
[`CLAUDE.md`](CLAUDE.md).

Algunos layouts se solapan A PROPOSITO: hay varias formas de contar lo mismo (tres
maneras de citar, dos de listar servicios). Elige la que encaje con el contenido,
no la primera que encuentres.

Genera el catalogo visual con: `python build/build.py test`.

## Biblioteca de imagenes

Las imagenes viven en `brand/assets/img/` (el proyecto es portable: no depende de
rutas externas). Para usar una imagen en el contenido:

```python
import brand.theme as T
s.add_cover(prs, title="...", image=T.img("naranjatec-web.jpg"))
s.add_image_feature(prs, "Titulo", ["parrafo"], image=T.img("ecco-working.jpg"),
                    stat=("+350", "proyectos"))
s.add_quote(prs, "cita", "Autor", avatar=T.img("avatars/avatar-canon.jpg"),
            image=T.img("accompany-meeting.jpg"))
```

Fotos reales de oficina en `T.img("oficina/naranjatec_XXXX.jpg")`.

## Como cambiar el contenido

El contenido son datos, separados de la maquetacion. Para cambiar textos edita el
modulo correspondiente en `content/` y vuelve a generar. No hace falta tocar
`lib/slides.py`. Convencion: el marcado `*enfasis*` en un titulo pone esa parte en
Playfair italica.

## Crear un deck nuevo

1. Crea `content/mi_deck.py` con `OUTFILE` y una funcion `build(prs)` (copia
   `content/nereidas.py` como referencia).
2. Anade su alias en el diccionario `DECKS` de `build/build.py`.
3. Genera con `python build/build.py mi_deck`.

## Trabajar con IA (Claude Cowork)

La forma mas rapida de montar un deck es conversando con el asistente: dale el
documento o brief (p.ej. un `.md` de propuesta), pide "monta un deck de NaranjaTec
con esto" y revisa el resultado. El asistente escribe el modulo de `content/` por
ti siguiendo las convenciones de [`CLAUDE.md`](CLAUDE.md). `content/nereidas.py` es
un ejemplo de un documento de propuesta convertido en presentacion.

## Marca (resumen)

- Amarillo dorado `#FFCD33` (wordmark "naranja")
- Azul `#1099ED` (wordmark "tec")
- Naranja de acento `#FF9E2C`
- Azul profundo `#0B3D66` (fondos de seccion)
- Fondo blanco calido `#FAF9F6`; tarjetas blancas con sombra suave
- Motivo grafico: hexagono del isotipo

Los colores estan muestreados del logo oficial y centralizados en `brand/theme.py`;
cambiarlos ahi los actualiza en todas las presentaciones.
