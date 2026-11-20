# Roadmap — Estudio·Bolsillo

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
| ⬜ | Varios proyectos | B | Lista para crear, renombrar, duplicar, abrir y borrar. Migrar el proyecto único actual. |
| ⬜ | Editor de canción | M | Línea de compases con los patrones A–D (intro A, estrofa B×4…). Unificar con la línea de tiempo de voz: una sola línea con fila de patrones y fila de voz. Reemplaza al modo cadena. |

## Fase 2 — Expresión y mezcla

| | Función | Esf. | Notas |
|---|---|---|---|
| ⬜ | Velocidad fina y nudge por paso | M | Volumen 1–127 y corrimiento ± medio paso. |
| ⬜ | Largo distinto por pista (polirritmos) | M | |
| ⬜ | Humanizar | B | Pequeñas variaciones de tiempo y volumen. |
| ⬜ | Tocar en vivo | M | Pads que suenan al tocarlos y graban en el patrón con cuantizado. |
| ⬜ | Efectos por canal | M | EQ 3 bandas, filtro, distorsión, bitcrusher, chorus. |
| ⬜ | Plantillas por género | B | Trap, house, reggaetón, lo-fi, techno: patrones + kit + tempo. |
| ⬜ | Medidores de nivel por canal | B | |
| ⬜ | Automatización | A | Grabar el movimiento de una perilla a lo largo del patrón o la canción. |

## Fase 3 — Instrumentos

| | Función | Esf. | Notas |
|---|---|---|---|
| ⬜ | Piano roll | A | Notas con duración, más octavas, velocidad. Reemplaza la grilla fija de bajo y synth. |
| ⬜ | Synths nuevos | M | FM (campanas, piano eléctrico), pad de cuerdas, pluck. |
| ⬜ | Arpegiador y acordes por grado | M | Progresiones I–V–vi–IV que siguen la escala. |
| ⬜ | Sampler propio | M | Cargar audios del usuario o cortar una toma de voz en pads. |

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
