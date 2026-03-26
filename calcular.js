function calcular(valores) {
  const { a, b, h, p, e, v } = valores;

  const x = a / 2;
  const y = b / 2;

  const D = (e * Math.pow(h, 3)) / (12 * (1 - Math.pow(v, 2)));

  const N = 15;
  let w = 0;
  let Mx = 0;
  let My = 0;

  for (let m = 1; m <= N; m += 2) {
    for (let n = 1; n <= N; n += 2) {

      const termo = Math.pow(m / a, 2) + Math.pow(n / b, 2);

      const seno = Math.sin(m * Math.PI * x / a) * Math.sin(n * Math.PI * y / b);
      const cosseno = Math.cos(m * Math.PI * x / a) * Math.cos(n * Math.PI * y / b);

      // Flecha
      w += (16 * p) / (D * Math.pow(Math.PI, 6)) *
        (seno / (m * n * Math.pow(termo, 2)));

      // Momentos
      Mx += (16 * p) / Math.pow(Math.PI, 4) *
        (((Math.pow(m / a, 2)) + v * Math.pow(n / b, 2)) /
        (m * n * Math.pow(termo, 2))) * seno;

      My += (16 * p) / Math.pow(Math.PI, 4) *
        ((v * Math.pow(m / a, 2) + Math.pow(n / b, 2)) /
        (m * n * Math.pow(termo, 2))) * seno;
    }
  }

  // ======================
  // TABELA MARCUS
  // ======================

  const rel = b / a;

  const tabela = {
    1.0: [0.00406, 0.0479, 0.0479, 0.338, 0.338, 0.420, 0.420, 0.065],
    1.5: [0.00772, 0.0812, 0.0498, 0.424, 0.363, 0.486, 0.480, 0.085],
    2.0: [0.01013, 0.1017, 0.0464, 0.465, 0.370, 0.503, 0.496, 0.092],
    3.0: [0.01223, 0.1189, 0.0406, 0.493, 0.372, 0.505, 0.498, 0.093],
    4.0: [0.01282, 0.1235, 0.0384, 0.498, 0.372, 0.502, 0.500, 0.094],
    5.0: [0.01297, 0.1246, 0.0375, 0.500, 0.372, 0.501, 0.500, 0.095]
  };

  // achar valor mais próximo
  const chave = Object.keys(tabela)
    .map(Number)
    .reduce((prev, curr) =>
      Math.abs(curr - rel) < Math.abs(prev - rel) ? curr : prev
    );

  const [alpha, beta, beta1, gamma, gamma1, delta, delta1, nCoef] = tabela[chave];

  // cálculos tabela
  const w_tab = alpha * p * Math.pow(a, 4) / D;
  const Mx_tab = beta * p * Math.pow(a, 2);
  const My_tab = beta1 * p * Math.pow(a, 2);
  const Qx = gamma * p * a;
  const Qy = gamma1 * p * a;
  const Vx = delta * p * a;
  const Vy = delta1 * p * a;
  const R = nCoef * p * Math.pow(a, 2);

  return `
Flecha: ${w.toExponential(4)} m
Flecha (cm): ${(w * 100).toFixed(4)} cm
Mx: ${Mx.toFixed(4)} kN.m/m
My: ${My.toFixed(4)} kN.m/m
Qx: ${Qx.toFixed(2)} kN/m
Qy: ${Qy.toFixed(2)} kN/m
Vx: ${Vx.toFixed(2)} kN/m
Vy: ${Vy.toFixed(2)} kN/m
R: ${R.toFixed(2)} kN

Rigidez D: ${D.toExponential(2)}
`;
}

export { calcular };