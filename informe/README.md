# Informe de entretiempo · ICCAN

Réplica del molde usado en las fechas 4 y 5 (`Entretiempo_Iccan_vs_*_1T.pdf`),
armada para poder completarse con los números del primer tiempo y salir en PDF
dentro de la ventana del descanso.

## Uso

```bash
NODE_PATH=/opt/node22/lib/node_modules node render.js datos-fecha6.json Entretiempo_Iccan_vs_Andes_1T.pdf
```

## Archivos

| archivo | qué es |
|---|---|
| `plantilla.html` | las 3 páginas del informe; se dibuja sola a partir de `window.DATOS` |
| `render.js` | carga el JSON en la plantilla y exporta el PDF con Chromium |
| `datos-fecha5.json` | los datos reales del partido vs Ambato Soldiers, para verificar contra el molde original |
| `datos-fecha6.json` | esqueleto vacío para cargar el entretiempo de la fecha 6 |
| `escudos/` | escudos de los clubes |
| `fonts/` | Lato (OFL), embebida para que el PDF no dependa de la red |

## Las tres páginas

1. **Informe de entretiempo** — marcador con parciales, los cuatro factores, rebote,
   transición (contraataques a favor y en contra) y el partido en una línea.
2. **Dónde y a quién** — mapa de tiro de los dos equipos, fichas de las rivales más
   peligrosas y fortalezas / debilidades / a mejorar.
3. **Box del 1er tiempo** — box tradicional con eFG y TS por jugadora, más las
   avanzadas de equipo con su glosario.

## Cargar los datos

Todo sale de `datos-*.json`. Notas de formato:

- **Cuatro factores**: `mejor` vale `"alto"` salvo en TOV%, donde conviene el número
  más bajo. La barra llena marca quién ganó el factor y se escala sola.
- **Mapa de tiro**: cada tiro es `{"x":0-1, "y":0-1, "metido":true|false}`, con
  `x` de izquierda a derecha y `y` desde la línea de fondo hacia el medio de la cancha.
  Si en vez de coordenadas hay una captura, se puede pasar `"imagen":"ruta.png"`
  y la cancha dibujada se reemplaza por esa imagen.
- **Rebote**: se carga ofensivo y defensivo; el total lo suma la plantilla.
- Cualquier dato que no haya llegado se deja en `null` y sale impreso como `s/d`
  en vez de inventarse.
