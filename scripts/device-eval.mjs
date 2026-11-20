// Evalúa una expresión JS dentro de la WebView de TAKT en el celular (vía adb forward tcp:9222 + DevTools).
// Uso: node cdp.mjs "<expresión>"   — la expresión puede usar await; se devuelve como JSON.
const list = await (await fetch('http://localhost:9222/json')).json();
const page = list.find(p => p.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
const expr = process.argv[2];
ws.onopen = () => ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: `(async()=>JSON.stringify(await (async()=>(${expr}))()))()`, awaitPromise: true, returnByValue: true, userGesture: true } }));
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id === 1) { const r = d.result; console.log(r.exceptionDetails ? 'ERROR: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text) : r.result.value); ws.close(); process.exit(0); } };
setTimeout(() => { console.log('timeout'); process.exit(1); }, 30000);
