// Configuración de Firebase para TAKT.
// Mientras esté en null, la app funciona igual pero sin cuenta ni nube (la sección "Cuenta" no aparece).
// Para activarla: Firebase console → Configuración del proyecto → Tus apps → App web → copiar el objeto firebaseConfig acá.
// Estos datos no son secretos (identifican el proyecto); la seguridad la dan las reglas de firestore.rules.
window.TAKT_FIREBASE = null;
/* Ejemplo:
window.TAKT_FIREBASE = {
  apiKey: "…",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto",
  storageBucket: "tu-proyecto.firebasestorage.app",
  messagingSenderId: "…",
  appId: "…"
};
*/
