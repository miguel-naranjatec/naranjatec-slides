# Distribucion: como dar esto a un companero

Guia para repartir la herramienta dentro del equipo. Si solo quieres *usar* el
generador, lee [`README.md`](README.md). Si eres el asistente de IA que trabaja
en el repo, lee [`CLAUDE.md`](CLAUDE.md).

## Estado del repositorio

- Remoto: `https://github.com/miguel-naranjatec/naranjatec-slides.git`
- Visibilidad: **PUBLICO**, por decision deliberada.
- Rama por defecto: `main`.

Que se publica con el repo, y conviene tener presente: las capturas de proyectos
de cliente de `brand/assets/img/`, la carpeta `avatars/` con fotos de personas
reales y 18 fotos de la oficina. No hay credenciales ni secretos, y NO se publica
ningun deck de cliente: solo el muestrario de disenos (`content/muestrario.py`).
Los decks con datos reales (presupuestos, tarifas, nombres) se generan fuera del
repo y su `.pptx` no se versiona (`output/` esta ignorado).

Las 4 familias tipograficas son OFL y Material Symbols es Apache-2.0:
redistribuirlas dentro del repo es legitimo. La fuente de iconos es una instancia
estatica a peso 300 generada con `scripts/make_icon_font.py`; ademas, los `.pptx`
llevan dentro la GEOMETRIA de sus 29 iconos, derivada de esa fuente
(`brand/icon_paths.py`). Apache-2.0 permite obras derivadas sin friccion (no hay
reserved font name de por medio, al contrario que en OFL).

## Mensaje para el companero

Copiar y pegar tal cual:

> **Generador de presentaciones de NaranjaTec**
>
> Genera los `.pptx` con la marca ya aplicada. Tu no maquetas: le das el
> contenido a Claude y el arma el deck.
>
> **Preparacion (una sola vez)**
>
> 1. Clona el repo en la carpeta donde trabajes con Claude:
>    `git clone https://github.com/miguel-naranjatec/naranjatec-slides.git`
> 2. `cd naranjatec-slides` y luego `pip install -r requirements.txt`
> 3. **Instala las fuentes** (recomendado, no imprescindible). Sin ellas el deck
>    se ve y funciona igual, solo que PowerPoint sustituye la tipografia por otra
>    sans. Los iconos NO dependen de esto: son formas, no texto.
>    - Windows: abre `brand/assets/fonts/`, selecciona todos los `.ttf` de las
>      subcarpetas `static/`, clic derecho -> Instalar. (`Material_Icons/` no hace
>      falta: no se instala en ninguna parte.)
>    - Mac: `python scripts/preview.py --install-fonts`
>
> **Compruebalo**
>
> Ejecuta `python build/build.py test` y abre
> `output/NaranjaTec-Test-Disenos.pptx`. Veras una diapositiva de cada tipo
> disponible. Si los iconos se ven bien, esta todo listo.
>
> **Como se usa**
>
> Abres Claude en esa carpeta y le dices, literalmente:
>
> *"Lee CLAUDE.md. Con este documento montame un deck de NaranjaTec"* -- y le
> pasas el brief o la propuesta.
>
> Claude escribe el modulo de contenido, lo registra y genera el `.pptx`. A
> partir de ahi le pides los cambios hablando: "la slide 4 tiene demasiado
> texto", "pon una foto de oficina en el separador".
>
> **La unica regla que importa**
>
> El `.pptx` es el resultado, no la fuente. Si lo abres en PowerPoint y retocas
> un titulo a mano, ese cambio desaparece la proxima vez que se regenere. Pide
> los cambios a Claude y que lo reconstruya. Retoca a mano solo cuando ya sea la
> version definitiva.
>
> Todo lo demas esta en el `README.md`.

## Los tres fallos que va a cometer todo el mundo

**1. Saltarse la instalacion de fuentes.** Es el mas comun. El sintoma --
cuadrados negros en vez de iconos, tipografia que no es la de marca -- parece un
bug de la herramienta, no un problema de su maquina. Siempre es esto.

**2. No hacer que Claude lea `CLAUDE.md`.** Ese fichero es el manual: catalogo
de layouts con sus firmas, convenciones y gotchas. Sin leerlo, el asistente
improvisa y se salta limites reales, como que `add_bullets` solo pinta 4
elementos y `add_process` es una rejilla 2x2. Si alguien dice "Claude no lo hace
bien", empieza preguntando si lo leyo.

**3. Editar el `.pptx` a mano y perder el trabajo.** El contenido vive en
`content/*.py`. Regenerar sobrescribe el deck. Ademas PowerPoint bloquea el
fichero mientras esta abierto (al reconstruir da `PermissionError`) y no recarga
solo: hay que cerrar y reabrir para ver los cambios.

## Revisar decks sin PowerPoint

En Claude Cowork, Linux o CI no hay PowerPoint. Para eso esta
`scripts/preview.py`, que convierte a PDF con LibreOffice headless y rasteriza
una imagen por pagina:

```
python scripts/preview.py --install-fonts   # una vez (Linux/macOS)
python scripts/preview.py test              # genera el deck y lo previsualiza
```

Los PNG quedan en `output/preview/<nombre-del-deck>/`.

Requiere LibreOffice y poppler en la maquina. En un sandbox limpio:

```
sudo apt-get install -y libreoffice-impress poppler-utils
```

Si falta poppler, el script se queda en el PDF y lo avisa. LibreOffice no es
PowerPoint: sirve para revisar composicion, recortes y desbordes de texto, pero
puede desviarse en detalles finos. La verificacion definitiva sigue siendo abrir
el `.pptx`.

## Para quien mantiene el repo

**Que NO subir.** Los `.pptx` generados (`output/` esta ignorado) y los zips de
fuentes (`*.zip` ignorado: los `.ttf` ya estan sueltos en
`brand/assets/fonts/`). Los dos zips duplicados pesaban 46,7 MB cada uno y se
retiraron del historial antes del primer push; el repo son ~78 MB.

**Anadir un deck.** Crear `content/mi_deck.py` con `OUTFILE` y `build(prs)`,
registrar el alias en el dict `DECKS` de `build/build.py`, generar con
`python build/build.py mi_deck`. `content/muestrario.py` es la referencia de
layouts. Un deck de cliente con datos reales NO se commitea: el repo es publico.

**Codificacion.** El codigo, los comentarios y el deck de test van en ASCII
puro. Los decks de cliente llevan acentos y ene reales, porque son entregables.
Verificar un fichero de codigo:

```
python -c "print(sum(1 for b in open('lib/slides.py','rb').read() if b>127))"
```

Debe dar 0.

**Cambios de marca.** `brand/theme.py` es la fuente de verdad (paleta,
tipografia, iconos, medidas). Un cambio ahi afecta a todos los decks de todo el
mundo: es una decision deliberada, no un ajuste al vuelo. Lo mismo para
`lib/slides.py`, que es maquetacion compartida.
