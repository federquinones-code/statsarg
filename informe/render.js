// Render del informe de entretiempo a PDF.
//   node render.js datos.json salida.pdf
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [, , archivoDatos, salida] = process.argv;
  if (!archivoDatos || !salida) {
    console.error('uso: node render.js <datos.json> <salida.pdf>');
    process.exit(1);
  }

  const datos = JSON.parse(fs.readFileSync(archivoDatos, 'utf8'));
  const plantilla = path.resolve(__dirname, 'plantilla.html');

  const navegador = await chromium.launch();
  const pagina = await navegador.newPage();

  const errores = [];
  pagina.on('pageerror', e => errores.push(e.message));
  pagina.on('console', m => { if (m.type() === 'error') errores.push(m.text()); });

  await pagina.addInitScript(d => { window.DATOS = d; }, datos);
  await pagina.goto('file://' + plantilla, { waitUntil: 'load' });
  await pagina.evaluate(() => document.fonts.ready);

  if (errores.length) {
    console.error('errores en la página:\n  ' + errores.join('\n  '));
    await navegador.close();
    process.exit(1);
  }

  await pagina.pdf({
    path: salida,
    format: 'A4',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });

  await navegador.close();
  console.log('listo: ' + salida);
})();
