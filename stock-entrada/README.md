# stock-entrada/

**Suelta aqui las fotos que descargues.** Tal cual vengan: sin renombrar, sin
optimizar, con el nombre feo que traigan del banco de imagenes.

Esta carpeta es un buzon, no una biblioteca. Su contenido esta en `.gitignore`:
lo que dejes aqui NO se sube al repo. Lo que se sube es el resultado de
procesarlo, que va a `brand/assets/img/stock/`.

## De donde bajarlas

- **Burst** (Shopify): https://www.shopify.com/stock-photos
  Uso comercial libre, sin atribucion. Orientado a e-commerce y producto, que es
  justo el agujero de nuestra biblioteca. No tiene API: se descarga a mano.
- **Pexels**: https://www.pexels.com
  Mas volumen y mejor fotografia. Uso comercial libre.

## Como procesarlas

    python scripts/add_stock.py

El script coge lo que haya aqui, lo optimiza, lo renombra con criterio, te
pregunta el SECTOR de cada foto, la registra en `brand/imagenes.py` y anota el
credito en `brand/assets/img/stock/CREDITS.md`. Despues, vacia el buzon.

## Por que eliges tu la foto y no un script

`brand/imagenes.py` existe porque elegir imagenes por palabra clave es como acabas
poniendo pulseras en una propuesta de chocolate (`pighen-store.jpg` no es una
tienda: son pulseras). Un script que busca "chocolate" en una API y se baja los
diez primeros resultados repite ese error, solo que contra un catalogo de
millones. Un deck necesita seis u ocho fotos: elegirlas bien es un juicio, y lo
haces tu. El script se encarga de lo mecanico, que es lo que hace bien.
