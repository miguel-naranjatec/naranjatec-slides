# Fuentes de marca (NaranjaTec)

Las presentaciones usan 5 familias. Deben estar **instaladas en el sistema** que
renderiza el .pptx (PowerPoint sustituye las que falten). Los `.ttf` estan
aqui para poder instalarlas en cualquier maquina.

| Rol en `brand/theme.py` | Familia | Carpeta |
|--------------------------|---------|---------|
| `FONT_TITLE`, `FONT_NUM` | Google Sans | `Google_Sans/static/` |
| `FONT_TITLE_EMPH`        | Playfair Display | `Playfair_Display/static/` |
| `FONT_BODY`, `FONT_BODY_MED` | Instrument Sans | `Instrument_Sans/static/` |
| `FONT_MONO`              | Geist Mono | `Geist_Mono/static/` |
| `FONT_ICON`              | Material Symbols Outlined 300 | `Material_Icons/` (`.ttf`) |

Las 4 primeras son OFL; Material Symbols es Apache-2.0 (ver `LICENSE` en su
carpeta). Es MULTIPLATAFORMA (Windows y Mac): sustituye a la antigua "Segoe Fluent
Icons" (solo Windows) para que los iconos se vean igual en Mac. El fichero
`.codepoints` mapea nombre de icono -> codigo.

La fuente de iconos NO es la que distribuye Google tal cual: Google la publica como
fuente variable y PowerPoint no sabe elegir un peso de un eje variable, asi que la
congelamos a peso 300 (mas fino que el 400 por defecto) con
`scripts/make_icon_font.py`. Por eso la familia se llama `Material Symbols Outlined
300` y no `Material Symbols Outlined`: si usara el nombre estandar y tuvieras
instalada la de Google, PowerPoint cogeria esa en silencio y el deck se veria con el
trazo grueso. Si la fuente falta, los iconos salen como cajas.

## Instalar

Usar los `.ttf` de las carpetas `static/` (no las versiones VariableFont: PowerPoint
no selecciona bien los pesos de una fuente variable).

### Windows (por usuario, sin admin)
```powershell
# Fuentes de marca (.ttf en */static/) + iconos (.ttf en Material_Icons/)
Get-ChildItem -Recurse -Include *.ttf brand/assets/fonts |
  Where-Object { $_.FullName -match 'static|Material_Icons' } |
  ForEach-Object { Copy-Item $_.FullName "$env:LOCALAPPDATA\Microsoft\Windows\Fonts\" }
# y registrar cada una en HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts
```
O mas simple: seleccionar los `.ttf`, clic derecho -> Instalar.

### macOS / Linux
Automatico:
```
python scripts/preview.py --install-fonts
```
O a mano: copiar los `.ttf` (de `*/static/` y de `Material_Icons/`) a
`~/Library/Fonts/` (macOS) o `~/.local/share/fonts/` (Linux) y ejecutar
`fc-cache -f` en Linux.

Tras instalar, reconstruir con `python build/build.py` y reexportar los PNG.
