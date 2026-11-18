# Estudio·Bolsillo — contexto para Claude Code

Estudio musical mobile-first inspirado en Audiotool, pero propio (no copiamos código ni assets de Audiotool). Objetivo: publicarlo como APK de Android con Capacitor y, más adelante, monetizarlo. El dueño del proyecto es Mariano; la UI y los comentarios van en **español rioplatense**.

## Estado actual (v0.1)

Todo vive en `www/index.html`, un solo archivo con HTML, CSS y JS vanilla. Sin build step, sin dependencias en runtime.

- **Ritmo:** 6 voces sintetizadas (kick, snare, clap, hat, ohat con choke, tom). Pasos con 3 estados: 0 apagado, 1 normal, 2 acento.
- **Bajo:** monofónico tipo 303 (sierra/cuadrada → lowpass resonante con envolvente → waveshaper). Acento (`a`) y ligado/slide (`s`) por paso. Los ligados encadenan notas en una sola voz con glide.
- **Synth:** polifónico, 2 osciladores desafinados → lowpass → ADSR. Varias filas por paso = acorde.
- **Notas como grados de escala:** el bajo y el synth guardan el *índice de fila* (0–11), no la nota MIDI. `rowMidi(base, fila)` lo convierte según `state.root` y `state.scale`. Cambiar la tonalidad re-afina todo sin desafinar.
- **Mezcla:** 3 canales (drums/bass/synth) con volumen, mute, envío a eco y a reverb (convolver con impulso generado). Master con compresor.
- **Patrones:** 4 (A–D). Modo cadena toca en orden los que tienen contenido.
- **Persistencia:** `localStorage` (clave `estudio-bolsillo-v1`), con try/catch.
- **Exportar:** render con `OfflineAudioContext` → WAV 16-bit estéreo → empaquetado en .zip (store, sin compresión) porque el visor de artifacts de claude.ai no deja bajar .wav. En la APK hay que guardar el WAV directo.

## Arquitectura del audio

- `buildGraph(ctx, live)` arma el grafo de mezcla para cualquier contexto (en vivo u offline). Las voces (`VOICES`, `vBass`, `vSynth`) reciben el grafo y un tiempo, así que el mismo código sirve para tocar en vivo y para exportar.
- `scheduleStep(gr, patrón, paso, inicioCompás, duraciónPaso, live)` agenda un paso completo. El swing desplaza los pasos impares.
- Transporte en vivo: scheduler con lookahead (`setInterval` cada 25 ms, agenda 120 ms adelante). Una cola (`queue`) sincroniza el playhead visual en `requestAnimationFrame`.
- `applyMix(gr)` aplica `state.mix` al grafo (en vivo con `setTargetAtTime`, offline con `.value`).

## Integración con claude.ai (a reemplazar en la APK)

`saveFile()` primero intenta `window.claude.use('downloads')`, que solo existe en el visor de artifacts de claude.ai. Si no está, cae a un `<a download>`. **En Android WebView `<a download>` no funciona:** hay que detectar Capacitor (`window.Capacitor?.isNativePlatform()`) y usar `@capacitor/filesystem` (escribir en Documents/Music) más `@capacitor/share` para compartir. Ahí se puede exportar `.wav` directo, sin zip.

## Próximos pasos (roadmap)

1. **APK:** `npx cap add android`, guardar archivos de forma nativa (ver arriba), ícono y splash, orientación vertical, pantalla siempre encendida mientras suena.
2. **Audio en Android:** probar la latencia en equipos de gama media. Si el scheduler con `setInterval` se atrasa en segundo plano, pasarlo a un AudioWorklet o a un Worker con reloj.
3. **Funciones:** más sonidos o kits, longitud de patrón variable (8/16/32), editor de canción (secuencia de patrones), grabar el micrófono, deshacer.
4. **Calidad del código:** cuando crezca, separar en módulos (`audio/`, `ui/`, `state/`) con Vite, sin romper que funcione offline.

## Cómo probar

- `npm run dev` y abrir en un celular o en las devtools en modo móvil (390×844).
- El audio necesita un toque del usuario antes de arrancar (`ensureAudio()`), por la política de autoplay.
- Para verificar el export: `renderOffline([0], 1)` en la consola devuelve un AudioBuffer.

## Convenciones

- Mobile-first: botones de 34–48 px de alto mínimo, sin hover como única pista.
- Textos de la UI en español (vos), cortos.
- No agregar dependencias de runtime salvo que haga falta de verdad; la app tiene que andar offline.
