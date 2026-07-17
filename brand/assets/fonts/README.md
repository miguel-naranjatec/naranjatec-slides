# Fuentes de marca (NaranjaTec)

Las presentaciones usan 4 familias de TEXTO. Conviene tenerlas **instaladas en el
sistema** que renderiza el .pptx: PowerPoint sustituye las que falten por otra
sans y el deck sigue funcionando, pero deja de ser fiel. Los `.ttf` estan aqui
para poder instalarlas en cualquier maquina.

| Rol en `brand/theme.py` | Familia | Carpeta |
|--------------------------|---------|---------|
| `FONT_TITLE`, `FONT_NUM` | Google Sans | `Google_Sans/static/` |
| `FONT_TITLE_EMPH`        | Playfair Display | `Playfair_Display/static/` |
| `FONT_BODY`, `FONT_BODY_MED` | Instrument Sans | `Instrument_Sans/static/` |
| `FONT_MONO`              | Geist Mono | `Geist_Mono/static/` |

Las 4 son OFL.

## `Material_Icons/` es un caso aparte: NO se instala

Los iconos **no son texto**: se dibujan como formas nativas con la geometria de
`brand/icon_paths.py`, que `scripts/make_icon_paths.py` extrae de este `.ttf` en
build-time. El `.ttf` (`ICON_TTF` en `theme.py`, Apache-2.0, ver `LICENSE`) es la
fuente de verdad del DIBUJO, no una dependencia de quien abre el deck. Se ve igual
en cualquier maquina sin instalar nada. El `.codepoints` mapea nombre -> codigo.

Fue asi por necesidad. Como texto, cada icono era un codepoint del area de uso
privado (U+E000-U+F8FF), y esos codepoints no pertenecen a ningun script:
PowerPoint tiene que adivinar a que ranura de fuente enrutarlos, y en PowerPoint
for Mac no siempre acertaba. Peor todavia, macOS tiene fuentes de sistema que
reclaman parte del rango PUA, asi que segun el codepoint salia un glifo ajeno o
no salia nada: fallaban unos iconos si y otros no.

Tampoco es la fuente que distribuye Google tal cual: Google la publica como fuente
variable, asi que la congelamos a peso 300 (mas fino que el 400 por defecto) con
`scripts/make_icon_font.py`. El nombre de familia lleva el `300` por un motivo que
ya no aplica (evitar que PowerPoint cogiera la de Google en silencio); hoy no lo
resuelve nadie por nombre. Instalarla solo sirve para depurar un glifo a mano.

## Instalar (las 4 de texto)

Usar los `.ttf` de las carpetas `static/` (no las versiones VariableFont: PowerPoint
no selecciona bien los pesos de una fuente variable).

### Windows (por usuario, sin admin)
```powershell
Get-ChildItem -Recurse -Include *.ttf brand/assets/fonts |
  Where-Object { $_.FullName -match 'static' } |
  ForEach-Object { Copy-Item $_.FullName "$env:LOCALAPPDATA\Microsoft\Windows\Fonts\" }
# y registrar cada una en HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts
```
O mas simple: seleccionar los `.ttf`, clic derecho -> Instalar.

### macOS / Linux
Automatico:
```
python scripts/preview.py --install-fonts
```
O a mano: copiar los `.ttf` de `*/static/` a `~/Library/Fonts/` (macOS) o
`~/.local/share/fonts/` (Linux) y ejecutar `fc-cache -f` en Linux.

Tras instalar, reconstruir con `python build/build.py` y reexportar los PNG.
