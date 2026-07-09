# Fuentes de marca (NaranjaTec)

Las presentaciones usan 5 familias. Deben estar **instaladas en el sistema** que
renderiza el .pptx (PowerPoint sustituye las que falten). Los `.ttf`/`.otf` estan
aqui para poder instalarlas en cualquier maquina; el .zip original tambien se conserva.

| Rol en `brand/theme.py` | Familia | Carpeta |
|--------------------------|---------|---------|
| `FONT_TITLE`, `FONT_NUM` | Google Sans | `Google_Sans/static/` |
| `FONT_TITLE_EMPH`        | Playfair Display | `Playfair_Display/static/` |
| `FONT_BODY`, `FONT_BODY_MED` | Instrument Sans | `Instrument_Sans/static/` |
| `FONT_MONO`              | Geist Mono | `Geist_Mono/static/` |
| `FONT_ICON`              | Material Icons Outlined | `Material_Icons/` (`.otf`) |

Las 4 primeras son OFL; Material Icons Outlined es Apache-2.0 (ver `LICENSE` en su
carpeta). Material Icons es MULTIPLATAFORMA (Windows y Mac): sustituye a la antigua
"Segoe Fluent Icons" (solo Windows) para que los iconos se vean igual en Mac. El
fichero `.codepoints` mapea nombre de icono -> codigo.

## Instalar

Usar los `.ttf` de las carpetas `static/` (no las versiones VariableFont: PowerPoint
no selecciona bien los pesos de una fuente variable).

### Windows (por usuario, sin admin)
```powershell
# Fuentes de marca (.ttf en */static/) + iconos (.otf en Material_Icons/)
Get-ChildItem -Recurse -Include *.ttf,*.otf brand/assets/fonts |
  Where-Object { $_.FullName -match 'static|Material_Icons' } |
  ForEach-Object { Copy-Item $_.FullName "$env:LOCALAPPDATA\Microsoft\Windows\Fonts\" }
# y registrar cada una en HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts
```
O mas simple: seleccionar los `.ttf`/`.otf`, clic derecho -> Instalar.

### macOS / Linux
Copiar los `.ttf` (de `*/static/`) y el `.otf` de `Material_Icons/` a
`~/Library/Fonts/` (macOS) o `~/.local/share/fonts/` (Linux) y ejecutar
`fc-cache -f` en Linux.

Tras instalar, reconstruir con `python build/build.py` y reexportar los PNG.
