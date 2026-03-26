import { calcular } from "./calcular.js";

const campos = ["a", "b", "h", "p", "e", "v"];

let passoAtual = 0;
let valores = {};
let resultado = "";

const titulo = document.getElementById("titulo");
const input = document.getElementById("input");
const progress = document.getElementById("progress");
const resultadoEl = document.getElementById("resultado");

function atualizarTela() {
  progress.value = passoAtual;

  if (passoAtual < campos.length) {
    const campo = campos[passoAtual];

    titulo.innerText = `Digite ${campo}`;
    input.style.display = "block";

    input.value = valores[campo] ?? "";

    resultadoEl.innerText = "";
  } else {
    titulo.innerText = "Resultado";
    input.style.display = "none";
    resultadoEl.innerText = resultado;
  }
}

window.proximo = function () {
  if (passoAtual < campos.length) {
    const valor = parseFloat(input.value);

    if (isNaN(valor)) {
      alert("Digite um número válido!");
      return;
    }

    valores[campos[passoAtual]] = valor;
    passoAtual++;

    if (passoAtual === campos.length) {
      try {
        resultado = calcular(valores);
      } catch (e) {
        resultado = "Erro no cálculo!";
      }
    }
  } else {
    // reset
    passoAtual = 0;
    valores = {};
    resultado = "";
  }

  atualizarTela();
};

window.voltar = function () {
  if (passoAtual > 0) {
    passoAtual--;
  }
  atualizarTela();
};

atualizarTela();