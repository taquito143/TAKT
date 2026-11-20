// Lo que TAKT usa de Firebase. `npm run vendor:firebase` lo empaqueta en www/vendor/firebase.js
// (un solo archivo local: la app no depende de un CDN y sigue abriendo sin internet).
// Firestore "lite" alcanza: la sincronización la maneja la app y no hace falta escuchar cambios en vivo.
export { initializeApp } from 'firebase/app';
export { getAuth, GoogleAuthProvider, signInWithPopup, signInWithCredential, signOut, onAuthStateChanged } from 'firebase/auth';
export { getFirestore, collection, doc, getDocs, setDoc } from 'firebase/firestore/lite';
