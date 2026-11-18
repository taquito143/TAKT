# Estudio·Bolsillo

Estudio musical pensado para el celular: caja de ritmos de 6 sonidos, bajo tipo 303 con acento y ligado, synth de acordes, mezcla con eco y reverb, 4 patrones encadenables y exportación a WAV. Todo el audio se sintetiza en el navegador con Web Audio, sin samples ni librerías.

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
- `CLAUDE.md` — contexto para trabajar el proyecto con Claude Code
