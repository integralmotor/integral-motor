# Integral Motor — notas para Claude

App de una rectificadora (presupuestos, órdenes, pagos/caja, cheques, clientes, proveedores, stock, precios). Usuario: habla en español rioplatense (voseo); respuestas cortas, sin tecnicismos.

## Dónde vive cada cosa
- **App real**: `index.html` de este repo, publicado con GitHub Pages en https://integralmotor.github.io/integral-motor/ (rama `main`, carpeta raíz, `.nojekyll`).
- **Datos reales**: Firebase, proyecto `integral-motor` (Firestore + login con Google). Mismas colecciones que antes: `presupuestos`, `clientes`, `salidas`, `proveedores`, `stock`, `stockmov`, `egresos`, `config/precios`, `config/contador`, `config/lock_num`; usuarios habilitados en `config/usuarios {emails:[]}`. Los arrays anidados se guardan como `{_a_:[...]}` (Firestore no los acepta); el adaptador `fbEnc/fbDec` de la app lo resuelve solo.
- **Versión de prueba**: el artifact de Claude https://claude.ai/artifact/2KBh1YBBxHYJ52hhdPuBCs. Es el MISMO código; dentro de Claude usa la base del artifact (copia vieja de los datos) y muestra el cartel "VERSIÓN DE PRUEBA".
- `firestore.rules`: copia de las reglas cargadas en la consola de Firebase. El mail del administrador está en dos lugares: `tools/firebase.json` (→ `FB_ADMIN`) y las reglas en la consola (los cambia el usuario).

## Cómo trabajamos (acordado con el usuario)
1. Cada cambio se hace primero en el artifact de Claude (leerlo con la acción `read`, editar, probar, publicar ahí) y se le muestra al usuario.
2. **Solo cuando el usuario dice "publicalo"** se actualiza la app real:
   `python3 tools/build_web.py <archivo del artifact>` → commit → push a `main`.
3. Si GitHub Pages no se actualiza, empujar un commit vacío (`git commit --allow-empty`).
4. Si se cambia `sw.js`, subir el nombre del caché (`im-v1` → `im-v2`).

## Detalles del código
- Fuera de Claude, `window.claude` no existe: la app crea uno propio (`window.claude.use('db')` → Firebase con login; `use('downloads')` → descarga normal). No cambiar la forma en que el resto de la app usa `db`.
- Respaldo tiene: "Descargar datos (JSON)" (todo), y fuera de Claude: Tu cuenta, Usuarios (solo admin) e Importar datos.
