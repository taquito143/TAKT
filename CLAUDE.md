# Estudio·Bolsillo — contexto para Claude Code

Estudio musical mobile-first inspirado en Audiotool, pero propio (no copiamos código ni assets de Audiotool). Objetivo: publicarlo como APK de Android con Capacitor y, más adelante, monetizarlo. El dueño del proyecto es Mariano; la UI y los comentarios van en **español rioplatense**.

## Estado actual (v0.1)

Todo vive en `www/index.html`, un solo archivo con HTML, CSS y JS vanilla. Sin build step, sin dependencias en runtime.

- **Ritmo:** 6 pistas (kick, snare, clap, hat, ohat con choke, tom). Pasos con 3 estados: 0 apagado, 1 normal, 2 acento. Cada paso tiene además redoble (`P.rat[pista][paso]`, 1–4 golpes repartidos en el paso) y probabilidad (`P.prob`, 100/75/50/25 %). El editor tiene tres modos (`dmode`: golpe, redoble, probabilidad).
- **Largo de patrón:** cada patrón guarda siempre 32 pasos (`NS`) y `P.len` (8/16/32) dice cuántos suenan; lo que queda afuera se conserva. `normPattern()` completa los patrones de versiones viejas (16 pasos, sin `rat`/`prob`) al cargar o abrir un archivo.
- **Biblioteca de sonidos:** 150 sonidos sintetizados (`LIB`), cada uno es un motor de `ENG` (kick, snare, clap, hat, tone, bell, nz) más parámetros. 10 categorías y 12 kits (`KITS`, un sonido por pista en el orden de `DRUMS`). Cada pista puede cargar cualquier sonido; la elección vive en `state.snd` (pista → id de sonido) y se toca con `playDrum(gr, pista, t, vel)`, que también maneja el choke del hat. Cero archivos de audio: no suma peso a la APK.
- **Bajo:** monofónico tipo 303 (sierra/cuadrada → lowpass resonante con envolvente → waveshaper). Acento (`a`) y ligado/slide (`s`) por paso. Los ligados encadenan notas en una sola voz con glide.
- **Synth:** polifónico, 2 osciladores desafinados → lowpass → ADSR. Varias filas por paso = acorde.
- **Notas como grados de escala:** el bajo y el synth guardan el *índice de fila* (0–11), no la nota MIDI. `rowMidi(base, fila)` lo convierte según `state.root` y `state.scale`. Cambiar la tonalidad re-afina todo sin desafinar.
- **Voz (micrófono):** pestaña propia con una línea de tiempo de 4/8/16 compases, independiente de los patrones (`state.voice.bars`; el transporte lleva el compás actual en `tlPos` y vuelve a 0 al final). Se elige el compás, suena 1 compás de cuenta (`click()`) y se graba encima del beat; la toma corta sola al final de la línea de tiempo o con ■. Captura con un AudioWorklet inline (`CAP_SRC`, con ScriptProcessor de respaldo) que manda bloques con su `currentTime`; `finishRec()` alinea compensando latencia de salida + entrada + el ajuste manual `state.voice.lat` (ms). El audio va a IndexedDB (`IDB`, base `estudio-bolsillo`, store `takes`); el proyecto solo guarda `state.clips` = `{id, bar, dur, n}`. `scheduleVoices()` agenda las tomas en vivo y en el export. El .json del proyecto **no** lleva el audio de las tomas.
- **Idiomas:** español e inglés. Todos los textos de la UI salen de `I18N` vía `t('clave', ...args)`; los nombres de sonidos, categorías y kits en inglés están en `SND_EN`, `CAT_EN` y `KIT_EN`. El idioma es una preferencia del dispositivo, no del proyecto (`localStorage` clave `estudio-bolsillo-lang`). La primera vez se abre un selector que no se puede cerrar sin elegir; después se cambia desde el menú ⋯. Al agregar UI nueva, sumar la clave en los dos idiomas.
- **Mezcla:** 4 canales (drums/bass/synth/voice) con volumen, mute, envío a eco y a reverb (convolver con impulso generado). Cada canal es `g` (volumen) → `duck` (sidechain) → master y envíos. Sidechain: `pump()` baja el `duck` de bajo y synth en cada bombo, según `state.mix.sc`. Master: compresor → limitador (-1 dB). El osciloscopio se pone rojo si la salida satura.
- **Deshacer:** `checkpoint(clave)` guarda una foto JSON del estado antes de cada cambio (máx. 80). Cambios seguidos con la misma clave en menos de 1 s se agrupan (un arrastre de deslizador o mantener BPM = un paso). Las tomas de voz no entran: `restore()` conserva `state.clips`. Toda acción nueva que cambie el proyecto tiene que llamar a `checkpoint()` antes (en el área principal alcanza con sumar su `data-k` a `MUT`).
- **Patrones:** 4 (A–D). Modo cadena toca en orden los que tienen contenido.
- **Persistencia:** `localStorage` (clave `estudio-bolsillo-v1`), con try/catch.
- **Exportar:** render con `OfflineAudioContext` → WAV 16-bit estéreo → empaquetado en .zip (store, sin compresión) porque el visor de artifacts de claude.ai no deja bajar .wav. En la APK hay que guardar el WAV directo.

## Arquitectura del audio

- `buildGraph(ctx, live)` arma el grafo de mezcla para cualquier contexto (en vivo u offline). Las voces (`VOICES`, `vBass`, `vSynth`) reciben el grafo y un tiempo, así que el mismo código sirve para tocar en vivo y para exportar.
- `scheduleStep(gr, patrón, paso, inicioCompás, duraciónPaso, live)` agenda un paso completo. El swing desplaza los pasos impares.
- Transporte en vivo: scheduler con lookahead (`setInterval` cada 25 ms, agenda 120 ms adelante). `gStep` cuenta pasos desde `t0` (cada 16 = un compás de la línea de tiempo de voz) y `pStep` es el paso dentro del patrón, así los patrones de 8 o 32 pasos no desfasan la voz. Una cola (`queue`) sincroniza el playhead visual en `requestAnimationFrame`.
- `applyMix(gr)` aplica `state.mix` al grafo (en vivo con `setTargetAtTime`, offline con `.value`).

## Integración con claude.ai (a reemplazar en la APK)

`saveFile()` primero intenta `window.claude.use('downloads')`, que solo existe en el visor de artifacts de claude.ai. Si no está, cae a un `<a download>`. **En Android WebView `<a download>` no funciona:** hay que detectar Capacitor (`window.Capacitor?.isNativePlatform()`) y usar `@capacitor/filesystem` (escribir en Documents/Music) más `@capacitor/share` para compartir. Ahí se puede exportar `.wav` directo, sin zip.

## Próximos pasos (roadmap)

El roadmap de funciones está en `ROADMAP.md` (fases, estado y esfuerzo). Mantenerlo al día al terminar cada función. Lo de abajo es lo técnico pendiente.

1. **APK:** `npx cap add android`, guardar archivos de forma nativa (ver arriba), ícono y splash, orientación vertical, pantalla siempre encendida mientras suena. Para el micrófono, agregar `RECORD_AUDIO` y `MODIFY_AUDIO_SETTINGS` en `AndroidManifest.xml` (Capacitor pide el permiso en tiempo de ejecución cuando la WebView llama a `getUserMedia`). Probar en un equipo real el ajuste de latencia de la voz.
2. **Audio en Android:** probar la latencia en equipos de gama media. Si el scheduler con `setInterval` se atrasa en segundo plano, pasarlo a un AudioWorklet o a un Worker con reloj.
3. **Funciones:** más sonidos o kits, longitud de patrón variable (8/16/32), editor de canción (secuencia de patrones), grabar el micrófono, deshacer.
4. **Calidad del código:** cuando crezca, separar en módulos (`audio/`, `ui/`, `state/`) con Vite, sin romper que funcione offline.

## Cómo probar

- `npm run dev` y abrir en un celular o en las devtools en modo móvil (390×844).
- El audio necesita un toque del usuario antes de arrancar (`ensureAudio()`), por la política de autoplay.
- El micrófono solo anda en contexto seguro: `localhost` o https. Abriendo la IP de la compu desde el celular (`http://192.168...`) la grabación falla; para probar voz en el celular, usar la APK.
- Para probar la grabación sin micrófono: en la consola, reemplazar `navigator.mediaDevices.getUserMedia` por una función que devuelva el `stream` de un `ctx.createMediaStreamDestination()` con un oscilador conectado.
- Para verificar el export: `renderOffline([0], 1)` en la consola devuelve un AudioBuffer.
- Para verificar tiempos sin analizar audio: reemplazar `playDrum` (o `scheduleStep`) por un envoltorio que anote `t` y llamar a `renderOffline`.
- Antes de probar sobre el proyecto guardado, copiar `localStorage['estudio-bolsillo-v1']` y restaurarlo al final.

## Convenciones

- Mobile-first: botones de 34–48 px de alto mínimo, sin hover como única pista.
- Textos de la UI en español (vos), cortos.
- No agregar dependencias de runtime salvo que haga falta de verdad; la app tiene que andar offline.
