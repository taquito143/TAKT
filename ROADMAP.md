# Roadmap — TAKT

Prioridad: primero lo que hace que la app se sienta completa y confiable, después lo que agrega sonido nuevo. Todo se sintetiza o se calcula en el dispositivo, así que nada de esto debería sumar peso a la APK (salvo donde se indica).

Leyenda: ✅ hecho · 🚧 en curso · ⬜ pendiente · esfuerzo **B** bajo / **M** medio / **A** alto

## Fase 1 — Base

| | Función | Esf. | Notas |
|---|---|---|---|
| ✅ | Deshacer / rehacer | B | Botones ↶ ↷ en la cabecera y Ctrl+Z / Ctrl+Y. Los deslizadores agrupan un arrastre en un solo paso. Las tomas de voz no se deshacen (el audio se borra de verdad). |
| ✅ | Largo de patrón 8 / 16 / 32 pasos | B | Por patrón. Los pasos que quedan fuera del largo se conservan por si se vuelve a alargar. |
| ✅ | Redobles ×2 ×3 ×4 por paso | B | Modo "Redoble" en el editor de ritmo. |
| ✅ | Probabilidad por paso (100 / 75 / 50 / 25 %) | B | Modo "Probabilidad". |
| ✅ | Sidechain (bombo → bajo y synth) | B | Una perilla en Mezcla. |
| ✅ | Limitador en el master + aviso de saturación | B | El osciloscopio se pone rojo si satura. |
| ✅ | Varios proyectos | B | Menú ⋯ → Proyectos: crear, renombrar, duplicar, abrir y borrar. El proyecto único anterior se migró solo. |
| ✅ | Editor de canción | M | Pestaña Canción: una línea de 4–32 compases con fila de patrones y fila de voz. Reemplaza al modo cadena. |

## Fase 2 — Expresión y mezcla

| | Función | Esf. | Notas |
|---|---|---|---|
| ✅ | Velocidad fina y nudge por paso | M | Modos Volumen (5–100 %) y Corrimiento (±50 % de un paso) en el editor de ritmo. |
| ✅ | Largo distinto por pista (polirritmos) | M | "Largo de pista": la pista da vueltas sola, independiente del patrón. |
| ✅ | Humanizar | B | En Mezcla → Tonalidad y groove: hasta ±12 ms y -30 % de volumen al azar. |
| ✅ | Tocar en vivo | M | Modo "En vivo": 6 pads; con la grabación encendida cada golpe va al paso más cercano. |
| ✅ | Efectos por canal | M | Botón FX en cada canal: EQ 3 bandas, filtro, distorsión, bitcrusher, chorus. |
| ✅ | Plantillas por género | B | Menú ⋯ → Plantillas: trap, house, reggaetón, lo-fi, techno, drum & bass, boom bap. |
| ✅ | Medidores de nivel por canal | B | En Mezcla, en dB. |
| ⬜ | Automatización | A | Grabar el movimiento de una perilla a lo largo del patrón o la canción. |

| ✅ | Pantalla de carga y título TAKT | B | Título con contorno y extrusión (luz desde la derecha). La línea del costado engorda y brilla con el sonido. |
| ✅ | Íconos propios en SVG (sin emojis) | B | Set de íconos de línea en `ICONS`. |
| ✅ | Inglés por defecto | B | El español se elige en el selector inicial o en Configuración. |
| ✅ | Configuración (⚙) | B | Idioma y calidad de exportación (44,1/48 kHz, 16/24 bits). Acá irán la cuenta y la carpeta de guardado. |
| ✅ | Inicio de sesión con Google y proyectos en la nube (web) | A | Firebase `takt-28243`: Auth con Google + Firestore con `firestore.rules`. Probado con la cuenta real: sube, baja y sincroniza ediciones. |
| ⬜ | Inicio de sesión con Google en la APK | M | Plugin `@capacitor-firebase/authentication`, SHA-1 de la llave de firma, `google-services.json` de `com.taquiro.takt`. |
| ⬜ | Audio de las tomas en la nube | M | Firebase Storage (requiere plan Blaze). |

## Fase 3 — Instrumentos

| | Función | Esf. | Notas |
|---|---|---|---|
| ✅ | Piano roll | A | Notas con duración, más octavas, velocidad. Reemplaza la grilla fija de bajo y synth. |
| ✅ | Synths nuevos | M | FM (campanas, piano eléctrico), pad de cuerdas, pluck. |
| ✅ | Arpegiador y acordes por grado | M | Progresiones I–V–vi–IV que siguen la escala. |
| ✅ | Sampler propio | M | Cargar audios del usuario o cortar una toma de voz en pads. |

## Fase 4 — Voz

| | Función | Esf. | Notas |
|---|---|---|---|
| ⬜ | Efectos de voz | M | Compuerta de ruido, compresor, eco/reverb preparados, cambio de tono. |
| ⬜ | Editar tomas | M | Recortar, mover, varias tomas por compás y elegir la mejor. |
| ⬜ | Afinación automática | A | Detección de tono + corrección hacia la escala del proyecto. |

## Fase 5 — Exportar y compartir

| | Función | Esf. | Notas |
|---|---|---|---|
| ⬜ | Exportar MP3 | B | Suma ~150 KB (encoder). |
| ⬜ | Stems (un WAV por canal) | B | |
| ⬜ | Exportar MIDI | B | |

## Fase 6 — APK

Ver "Próximos pasos" en `CLAUDE.md`: Capacitor, guardar archivos nativo, permisos de micrófono, ícono, latencia en equipos reales.
