---
id: metodo-imprimir-encadernar
type: metodo
title: "Imprimir para encadernar (costura japonesa)"
ferramenta: "Pandoc + XeLaTeX"
escopo: vault
status: revisado
project: ufrgs
related:
  - "[[Metodo - MOC]]"
  - "[[Markdown para PDF com grego]]"
---

# Imprimir para encadernar

```powershell
pandoc arquivo.md -d caderno        -o arquivo.pdf   # frente e verso
pandoc arquivo.md -d caderno-frente -o arquivo.pdf   # só frente
```

## O problema que isso resolve

Margem simétrica serve para folha solta. Num caderno costurado ela erra por dois motivos ao mesmo tempo:

1. **A costura come margem.** Furos a 15 mm da borda, mais o fio, mais o fato de a costura japonesa **não abrir totalmente plana** — o texto perto da lombada fica escondido na curva.
2. **O lado da costura troca a cada página.** Numa folha impressa dos dois lados, a lombada está à esquerda na frente e à **direita** no verso. Margem fixa acerta metade das páginas e erra a outra metade.

## As medidas

| | Valor | Por quê |
|---|---|---|
| interna (costura) | **32 mm** | 15 mm somem na costura + 17 mm de respiro |
| externa | **22 mm** | enxuta, aproveita o papel |
| superior | 22 mm | |
| inferior | 25 mm | maior que a superior: convenção tipográfica, o bloco fica acima do centro óptico |

Resultado medido no PDF: mancha de **156 × 250 mm**, cerca de **74 caracteres por linha**. A faixa confortável de leitura é 60–75, então está no limite bom. Testei também 30/18 (77 caracteres — largo demais) e 36/28 (71, mas gasta uma página a mais a cada nove).

Verificação da alternância, medida com `pdftotext -bbox`:

```
pag 1: esq 31.9mm | dir 21.1mm   -> costura na ESQUERDA
pag 2: esq 21.8mm | dir 31.2mm   -> costura na DIREITA
pag 3: esq 31.8mm | dir 21.1mm   -> costura na ESQUERDA
```

## Escolher entre os dois perfis

**Isto importa mais que as medidas.** Usar o perfil errado estraga metade das páginas.

- Imprimindo **frente e verso** → `-d caderno`. Usa `twoside`, e a margem larga alterna de lado sozinha.
- Imprimindo **só na frente** → `-d caderno-frente`. Margem larga sempre à esquerda.

Usar `caderno` para impressão só-frente é o erro mais provável: metade das folhas sairia com a margem larga no lado errado, e você só descobre depois de furar.

## Duas armadilhas de sintaxe

Ambas custaram build quebrado no teste:

**`oneside` não existe no geometry.** É opção da classe do documento, não do pacote. Escrever `geometry: "...,oneside"` falha com `Package keyval Error: oneside undefined`. Como a classe `article` já é oneside por padrão, basta omitir. Já `twoside` o geometry aceita.

**`classoption` tem que ficar dentro de `variables`.** Solto no topo do defaults file, o Pandoc rejeita com `Error parsing ... line N column 0`. Assim funciona:

```yaml
variables:
  classoption:
    - twoside
```

## Links pretos

Os dois perfis usam `linkcolor: black`. Link azul em papel não leva a lugar nenhum e só suja a página. No `academico.yaml`, que serve para leitura em tela, eles seguem coloridos.

## Antes de mandar imprimir

- **Confira a paridade.** Em frente e verso, PDF com número ímpar de páginas deixa a última folha com o verso em branco. Nem sempre incomoda, mas é bom saber antes.
- **Imprima uma folha de teste** e meça a margem interna com régua. Impressoras domésticas costumam deslocar 1–2 mm, e esse deslocamento se acumula visivelmente perto da costura.
- **Capa em gramatura maior**, impressa à parte com `-d academico` — a capa não tem corpo de texto e não precisa da margem de costura.
