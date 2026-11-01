"""Arma index.html (la app real, fuera de Claude) a partir del archivo de la app que se edita en Claude.

Uso:  python3 tools/build_web.py ruta/al/fragmento.html
El fragmento es el archivo del artifact de Claude (empieza en <title>, sin <!doctype>).
Agrega la cabecera web (manifest, íconos, colores), el registro del service worker,
y pone la configuración de Firebase y el mail del administrador que están en tools/firebase.json.
"""
import sys, json, os
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
out = os.path.join(here, '..', 'index.html')
s = open(src, encoding='utf-8').read()
c = json.load(open(os.path.join(here, 'firebase.json'), encoding='utf-8'))
assert "const FB_CFG=null;" in s and "const FB_ADMIN='';" in s, 'el fragmento no tiene FB_CFG/FB_ADMIN vacíos'
s = s.replace("const FB_CFG=null;", "const FB_CFG=" + json.dumps(c['config'], ensure_ascii=False) + ";", 1)
s = s.replace("const FB_ADMIN='';", "const FB_ADMIN=" + json.dumps(c['admin']) + ";", 1)
head = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b1630">
<meta name="description" content="Presupuestos, órdenes, pagos y stock de Rectificaciones Integral Motor">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Integral Motor">
<style>html,body{background:#0b1630}</style>
</head>
<body>
'''
tail = '''
<script>if('serviceWorker' in navigator&&location.protocol=='https:')addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>
</body>
</html>
'''
open(out, 'w', encoding='utf-8').write(head + s + tail)
print('index.html listo:', len(head + s + tail), 'bytes')
