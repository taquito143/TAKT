# Estudio·Bolsillo

Estudio musical pensado para el celular: caja de ritmos de 6 pistas con 150 sonidos y 12 kits, patrones de 8/16/32 pasos con redobles y probabilidad, bajo tipo 303 con acento y ligado, synth de acordes, grabación de voz con el micrófono en su propia línea de tiempo, mezcla con eco, reverb, sidechain y limitador, deshacer/rehacer, 4 patrones encadenables y exportación a WAV. En español e inglés. Todo el audio se sintetiza en el navegador con Web Audio, sin samples ni librerías.

## Probarlo en la compu

```bash
npm install
npm run dev        # abre http://localhost:5173
```

Para probarlo en el celular, abrí la IP de la compu en el mismo wifi (ej. `http://192.168.0.10:5173`).

## Armar la APK (Android)

Requisitos: Node 20+, Android Studio (trae el SDK y Java).

```bash
npm install
npm run android:add    # solo la primera vez: crea la carpeta android/
npm run android:sync   # copia www/ al proyecto Android
npm run android:open   # abre Android Studio → Build → Build APK(s)
```

Cada vez que cambies algo en `www/`, corré `npm run android:sync` de nuevo.

## Estructura

- `www/index.html` — la app completa (HTML + CSS + JS en un solo archivo)
- `capacitor.config.json` — configuración de la app Android
- `ROADMAP.md` — funciones hechas y pendientes, por fase
- `CLAUDE.md` — contexto para trabajar el proyecto con Claude Code
