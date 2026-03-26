function calcular(valores) {
  const { a, b, h, p, e, v } = valores;

  const x = a / 2;
  const y = b / 2;

  const D = (e * Math.pow(h, 3)) / (12 * (1 - Math.pow(v, 2)));

  const N = 15;
  let w = 0;
  let Mx = 0;
  let My = 0;
  let Mxy = 0;

  for (let m = 1; m <= N; m += 2) {
    for (let n = 1; n <= N; n += 2) {

      const termo = Math.pow(m / a, 2) + Math.pow(n / b, 2);

      const seno = Math.sin(m * Math.PI * x / a) * Math.sin(n * Math.PI * y / b);
      const cosseno = Math.cos(m * Math.PI * x / a) * Math.cos(n * Math.PI * y / b);

      w += (16 * p) / (D * Math.pow(Math.PI, 6)) * (seno / (m * n * Math.pow(termo, 2)));

      My += (16 * p) / Math.pow(Math.PI, 4) *
        (((Math.pow(m / a, 2)) + v * Math.pow(n / b, 2)) / (m * n * Math.pow(termo, 2))) * seno;

      Mx += (16 * p) / Math.pow(Math.PI, 4) *
        ((v * Math.pow(m / a, 2) + Math.pow(n / b, 2)) / (m * n * Math.pow(termo, 2)) * seno);

      Mxy += -(16 * (1 - v) * p) / (Math.pow(Math.PI, 4) * a * b) *
        (cosseno / Math.pow(termo, 2));
    }
  }

  return `
Flecha máxima: ${w.toExponential(4)} m
Mx: ${Mx.toFixed(4)}
My: ${My.toFixed(4)}
Mxy: ${Mxy.toFixed(4)}
Rigidez D: ${D.toExponential(2)}
`;
}

export { calcular }