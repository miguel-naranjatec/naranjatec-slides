# Presentaciones NaranjaTec

Sistema para generar presentaciones PowerPoint (`.pptx`) editables con la marca de
NaranjaTec. Los archivos se producen con `python-pptx`, aplicando de forma
consistente la paleta, la tipografia y el logo de la empresa.

> Para asistentes de IA (Claude Code / Claude Cowork) hay un manual operativo
> detallado en [`CLAUDE.md`](CLAUDE.md): catalogo de layouts, convenciones,
> codificacion y gotchas.

## Requisitos

- Python 3.10 o superior (probado con 3.14).
- Dependencias (solo dos):

```
pip install -r requirements.txt
```

Tipografia de marca (4 familias, todas gratuitas OFL, `.ttf` incluidos en
`brand/assets/fonts/`): titulos **Google Sans** (con enfasis en **Playfair
Display** italica), cuerpo **Instrument Sans**, botones/mono **Geist Mono**. Los
iconos usan **Material Icons Outlined** (Google, multiplataforma Windows/Mac). Para
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
output/                 Presentaciones generadas (no se versionan)
```

## Tipos de diapositiva

`lib/slides.py` ofrece ~25 layouts: portada, indice, separadores, statement,
vinetas, dos columnas, rejilla de servicios, proceso, texto+imagen, cifras,
timeline (multipagina), comparativa, galerias, banda de features, mision, rejilla
numerada, testimonio, valores, resumen, producto, hero, cierres/CTA, etc. El
catalogo completo con la firma de cada uno esta en [`CLAUDE.md`](CLAUDE.md).

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
