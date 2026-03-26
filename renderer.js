import { calcular } from "./calcular.js";

const campos = [
  { key: "a", label: "Qual valor da largura da laje (a) em metros?" },
  { key: "b", label: "Qual valor do comprimento da laje (b) em metros?" },
  { key: "h", label: "Qual valor da espessura da laje (h) em metros?" },
  { key: "v", label: "Qual valor do coeficiente de Poisson (v)?" },
  { key: "e", label: "Qual valor do módulo de elasticidade (E)?" },
  { key: "p", label: "Qual valor da carga em kN/m² (p₀)?" }
];

let passoAtual = 0;
let valores = {};
let resultado = "";

const imagens = {
  a: "./img/img_a.jpeg", // largura
  b: "./img/img_b.jpeg", // comprimento
  h: "./img/img_h.jpeg"  // espessura
};

const titulo = document.getElementById("titulo");
const input = document.getElementById("input");
const progress = document.getElementById("progress");
const resultadoEl = document.getElementById("resultado");
const btnVoltar = document.getElementById("btnVoltar");
const btnProximo = document.getElementById("btnProximo");
const imagem = document.getElementById("imagem");

function atualizarTela() {
  progress.value = passoAtual;

  if (passoAtual < campos.length) {
    const campo = campos[passoAtual];

    titulo.innerText = campo.label;
    input.style.display = "block";

    input.value = valores[campo.key] ?? "";

    resultadoEl.innerText = "";

    btnVoltar.style.display = passoAtual > 0 ? "inline-block" : "none";
    btnProximo.innerText = passoAtual === campos.length - 1 ? "Calcular" : "Próximo";

    const campoKey = campo.key;

    if (imagens[campoKey]) {
      imagem.src = imagens[campoKey];
      imagem.style.display = "block";
    } else {
      imagem.style.display = "none";
    }

  } else {
    titulo.innerText = "Resultado";
    input.style.display = "none";
    resultadoEl.innerText = resultado;

    btnVoltar.style.display = "none";
    btnProximo.innerText = "Reiniciar";
  }
}

window.proximo = function () {
  if (passoAtual < campos.length) {
    const valor = parseFloat(input.value);

    if (isNaN(valor)) {
      alert("Digite um número válido!");
      return;
    }

    valores[campos[passoAtual].key] = valor;
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