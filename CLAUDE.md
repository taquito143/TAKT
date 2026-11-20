# TAKT — contexto para Claude Code

**TAKT** es un estudio musical mobile-first inspirado en Audiotool, pero propio (no copiamos código ni assets de Audiotool). Objetivo: publicarlo como APK de Android con Capacitor y, más adelante, monetizarlo. El nombre definitivo es **TAKT** (en todos los idiomas, siempre en mayúsculas); antes se llamaba "Estudio·Bolsillo" y ese nombre solo sobrevive en el código que migra datos viejos. El dueño del proyecto es Mariano; la UI y los comentarios van en **español rioplatense**.

## Estado actual (v0.1)

Todo vive en `www/index.html`, un solo archivo con HTML, CSS y JS vanilla. Sin build step, sin dependencias en runtime.

- **Ritmo:** 6 pistas (kick, snare, clap, hat, ohat con choke, tom). Pasos con 3 estados: 0 apagado, 1 normal, 2 acento. Cada paso tiene además redoble (`P.rat[pista][paso]`, 1–4 golpes repartidos en el paso) y probabilidad (`P.prob`, 100/75/50/25 %). También volumen (`P.vel`, 5–100 %) y corrimiento (`P.nud`, ±50 % de un paso). Las claves por paso están en `STEPK` con sus valores por defecto en `STEPDEF`. El editor tiene seis modos (`dmode`: golpe, redoble, probabilidad, volumen, corrimiento, en vivo); en volumen y corrimiento se elige un paso (`selStep`) y se ajusta con un deslizador que actualiza solo ese pad (`stepInput()`).
- **Largo por pista (polirritmo):** `P.tl[pista]` (0 = igual al patrón). La pista usa el paso `abs % tl`, donde `abs` son los pasos desde que arrancó la reproducción (último parámetro de `scheduleStep`), así da vueltas independiente del patrón.
- **En vivo:** modo con 6 pads que suenan en `pointerdown`. Con `liveRec` y el beat sonando, `liveHit()` busca en `hist` (últimos pasos agendados) el más cercano a lo que se estaba escuchando (`currentTime - outputLatency`) y lo escribe ahí.
- **Humanizar:** `state.hum` (0–1): hasta ±12 ms y -30 % de volumen al azar por golpe.
- **Plantillas:** `TPL` (menú ⋯ → Plantillas). Cada una crea un proyecto nuevo con `fromTemplate()`: patrón A del género, B con remate, arreglo A A A B.
- **Largo de patrón:** cada patrón guarda siempre 32 pasos (`NS`) y `P.len` (8/16/32) dice cuántos suenan; lo que queda afuera se conserva. `normPattern()` completa los patrones de versiones viejas (16 pasos, sin `rat`/`prob`) al cargar o abrir un archivo.
- **Biblioteca de sonidos:** 150 sonidos sintetizados (`LIB`), cada uno es un motor de `ENG` (kick, snare, clap, hat, tone, bell, nz) más parámetros. 10 categorías y 12 kits (`KITS`, un sonido por pista en el orden de `DRUMS`). Cada pista puede cargar cualquier sonido; la elección vive en `state.snd` (pista → id de sonido) y se toca con `playDrum(gr, pista, t, vel)`, que también maneja el choke del hat. Cero archivos de audio: no suma peso a la APK.
- **Bajo:** monofónico tipo 303 (sierra/cuadrada → lowpass resonante con envolvente → waveshaper). Acento (`a`) y ligado/slide (`s`) por paso. Los ligados encadenan notas en una sola voz con glide.
- **Synth:** polifónico, 2 osciladores desafinados → lowpass → ADSR. Varias filas por paso = acorde.
- **Notas como grados de escala:** el bajo y el synth guardan el *índice de fila* (0–11), no la nota MIDI. `rowMidi(base, fila)` lo convierte según `state.root` y `state.scale`. Cambiar la tonalidad re-afina todo sin desafinar.
- **Canción (arreglo):** pestaña Canción (`tab==='voice'` en el código). Una línea de 4/8/16/32 compases de 16 pasos (`state.voice.bars`) con dos filas: patrones (`state.song.seq`, un patrón 0–3 o -1 = silencio por compás) y voz. Con `state.song.on` el transporte toca el arreglo (`songStep()`): si un patrón ocupa varios compases seguidos avanza por ellos, así uno de 32 pasos usa 2 compases y uno de 8 se repite 2 veces por compás. Apagado, se repite el patrón elegido. Reemplazó al viejo modo cadena (`fixState()` convierte `chain:true` en un arreglo). El export usa `renderSong()` en modo canción.
- **Voz (micrófono):** se graba sobre la misma línea de compases (el transporte lleva el compás actual en `tlPos` y vuelve a 0 al final). Se elige el compás, suena 1 compás de cuenta (`click()`) y se graba encima del beat; la toma corta sola al final de la línea de tiempo o con ■. Captura con un AudioWorklet inline (`CAP_SRC`, con ScriptProcessor de respaldo) que manda bloques con su `currentTime`; `finishRec()` alinea compensando latencia de salida + entrada + el ajuste manual `state.voice.lat` (ms). El audio va a IndexedDB (`IDB`, base `takt`, store `takes`; `IDB.migrate()` copia una vez las tomas de la base vieja `estudio-bolsillo`); el proyecto solo guarda `state.clips` = `{id, bar, dur, n}`. `scheduleVoices()` agenda las tomas en vivo y en el export. El .json del proyecto **no** lleva el audio de las tomas.
- **Idiomas:** español e inglés. Todos los textos de la UI salen de `I18N` vía `t('clave', ...args)`; los nombres de sonidos, categorías y kits en inglés están en `SND_EN`, `CAT_EN` y `KIT_EN`. El idioma es una preferencia del dispositivo, no del proyecto (`localStorage` clave `takt-lang`). La primera vez se abre un selector que no se puede cerrar sin elegir; después se cambia desde ⚙ Configuración. Al agregar UI nueva, sumar la clave en los dos idiomas.
- **Mezcla:** 4 canales (drums/bass/synth/voice) con volumen, mute, envío a eco y a reverb (convolver con impulso generado). Cada canal es `g` (volumen) → EQ 3 bandas → filtro (`allpass` en neutro) → distorsión → bitcrusher (+ chorus) → `duck` (sidechain) → medidor (solo en vivo) → master y envíos. Los efectos viven en `state.fx[canal]` (`fxDefault()`) y los aplica `applyMix()`. El chorus se arma y desarma con `setChorus()` porque un retardo modulado consume CPU aunque esté en cero. Medidores por canal en dB (`drawMeters()`). Sidechain: `pump()` baja el `duck` de bajo y synth en cada bombo, según `state.mix.sc`. Master: compresor → limitador (-1 dB). El osciloscopio se pone rojo si la salida satura.
- **Deshacer:** `checkpoint(clave)` guarda una foto JSON del estado antes de cada cambio (máx. 80). Cambios seguidos con la misma clave en menos de 1 s se agrupan (un arrastre de deslizador o mantener BPM = un paso). Las tomas de voz no entran: `restore()` conserva `state.clips`. Toda acción nueva que cambie el proyecto tiene que llamar a `checkpoint()` antes (en el área principal alcanza con sumar su `data-k` a `MUT`).
- **Patrones:** 4 (A–D) por proyecto.
- **Proyectos y persistencia:** varios proyectos en `localStorage`: índice `takt-projects` (`[{id, name, upd}]`), abierto `takt-cur`, y cada proyecto en `takt-p:<id>`. `save()` escribe con 300 ms de demora (`flushSave()` lo fuerza; se llama al cambiar de proyecto y al ocultar la app). Menú ⋯ → Proyectos: abrir, nuevo, renombrar, duplicar (copia también el audio de las tomas con ids nuevos) y borrar (borra sus tomas). Abrir un .json crea un proyecto nuevo. Al arrancar, `migrateKeys()` pasa las claves viejas `estudio-bolsillo-*` a `takt-*`, y `initProjects()` convierte el proyecto único de antes (`takt-v1`) en el primero de la lista.
- **Título y pantalla de carga:** `.brand` usa Arial Black itálica con relleno oscuro, contorno claro y extrusión hacia abajo-izquierda (luz desde la derecha), todo con `text-shadow` en pasos de 1 px enteros (los fraccionarios dejan rayas). `#splash` muestra el título en grande ~1,3 s al abrir. Al lado del título, el osciloscopio (`drawScope()`) dibuja la salida y su grosor y brillo siguen el nivel RMS (sube rápido, baja suave). Las sombras se generan con un script; si cambia el tamaño de letra, regenerarlas.
- **Configuración (⚙):** preferencias del dispositivo, no del proyecto, en `localStorage` `takt-settings` (`settings`): calidad de exportación (44,1/48 kHz, 16/24 bits). El idioma también se cambia ahí (sigue en `takt-lang`). Lo que se sume a futuro (cuenta, carpeta de guardado) va en `settingsSheet()`.
- **Exportar:** render con `OfflineAudioContext` a `settings.sr` → WAV estéreo de `settings.bits` (`encodeWav(buf, bits)`) → empaquetado en .zip (store, sin compresión) porque el visor de artifacts de claude.ai no deja bajar .wav. En la APK hay que guardar el WAV directo.

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
- Para probar sin tocar los proyectos del usuario: crear uno temporal con `addProject(estado, 'PRUEBA')` y borrarlo al final con `delProject(id)`.

## Convenciones

- Mucho código está en líneas largas: **no usar comentarios `//` en medio de una línea**, porque comentan el resto del código de esa línea. Usar `/* */` o ponerlos en su propia línea.
- Medir rendimiento del export con el mismo patrón contra `main` antes de sumar nodos de audio por canal: los hats metálicos ya hacen que el render ande cerca de tiempo real en una compu cargada.

- Mobile-first: botones de 34–48 px de alto mínimo, sin hover como única pista.
- Textos de la UI en español (vos), cortos.
- No agregar dependencias de runtime salvo que haga falta de verdad; la app tiene que andar offline.
