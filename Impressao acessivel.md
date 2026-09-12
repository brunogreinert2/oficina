---
id: metodo-impressao-acessivel
type: metodo
title: "Impressão acessível"
ferramenta: "Pandoc + XeLaTeX"
escopo: vault
status: revisado
project: ufrgs
related:
  - "[[Metodo - MOC]]"
  - "[[Imprimir para encadernar]]"
  - "[[Markdown para PDF com grego]]"
---

# Impressão acessível

Um perfil por necessidade, no mesmo formato de sempre:

```powershell
pandoc arquivo.md -d caderno-presbiopia   -o arquivo.pdf
pandoc arquivo.md -d caderno-baixa-visao  -o arquivo.pdf
pandoc arquivo.md -d caderno-astigmatismo -o arquivo.pdf
pandoc arquivo.md -d caderno-dislexia     -o arquivo.pdf
```

Escolhe-se pela **necessidade**, não pelo parâmetro — mesma lógica do Pedra Angular.

Para combinações fora dos perfis existe o `Novo-Caderno.ps1`, que pergunta corpo, entrelinha, espaço entre letras e fonte. É opcional: os perfis cobrem os casos comuns.

---

## O que não se traduz da tela para o papel

Os ajustes do app não migram um a um. Quatro diferenças mudam o desenho.

### Não há zoom

Na tela, corpo errado se conserta em dois toques. No papel é reimprimir. Por isso o script avisa para **imprimir a página 1 e conferir no papel** antes de mandar o caderno inteiro.

### Cor de fundo não existe

*Branco sobre preto*, *sépia*, *azul-noite* viram chapado de tinta: caro, encharca a folha, ondula, e o toner preto reflete a luz do ambiente — o oposto do que a fotofobia precisa.

**O equivalente real é comprar papel colorido.** Papel creme e amarelo-claro custam pouco em papelaria, e funcionam melhor que qualquer coisa que a impressora faça. Papel creme é o análogo do *sépia*.

### Corpo grande custa espessura

Medido no Barnes, mesma mancha:

| Corpo | Páginas | Caracteres por linha |
|---|---|---|
| 11 pt | 9 | 74 |
| 12 pt | 12 | 68 |
| 14 pt | 17 | 56 |
| 17 pt | 26 | 46 |
| 20 pt | 35 | 39 |

A costura japonesa comporta uns 15 mm de bloco. Um caderno em 20 pt vira dois ou três volumes — restrição física que a tela não tem.

### A costura japonesa não abre plana

Para baixa visão isso atrapalha: a pessoa precisa achatar o livro com a mão enquanto lê de perto, e a margem interna some na curva.

**Para baixa visão, espiral ou wire-o é superior.** Abre 180°, deita na mesa e libera as duas mãos. Menos bonito, mas é o que a pessoa precisa. A costura é para quem enxerga bem.

### O verso vira fantasma

Frente e verso em papel de 75 g deixa a página de trás transparecer. Em leitura comum ninguém nota; com baixa visão isso come contraste justamente onde ele é escasso.

Para esse caso: **só na frente**, em papel de gramatura maior (90 g ou mais). Gasta o dobro de papel e é o certo.

---

## O que o papel ganha

Vale dizer, porque é fácil esquecer: tinta preta em papel branco tem **contraste maior que a maioria das telas**, e não emite luz. Para fotofobia, papel é melhor que qualquer tema escuro — o que incomoda é a emissão, não o texto.

---

## As receitas

| Perfil | Corpo | Entrelinha | Entre letras | Fonte | Páginas* |
|---|---|---|---|---|---|
| `caderno` | 11 pt | 1.2 | normal | Cardo | 9 |
| `caderno-presbiopia` | 12 pt | 1.35 | normal | Cardo | 12 |
| `caderno-astigmatismo` | 12 pt | 1.35 | **amplo** | Atkinson Hyperlegible | 10 |
| `caderno-dislexia` | 12 pt | 1.6 | amplo | OpenDyslexic | 13 |
| `caderno-baixa-visao` | 17 pt | 1.6 | normal | Cardo, **só frente** | 30 |

\* medido no Barnes *Ciência e especulação*, que tem 9 páginas no perfil padrão.

No astigmatismo o borrão tem direção, e aumentar o corpo ajuda menos do que se espera — quem resolve é o espaço entre letras. Vale para o papel como vale para a tela.

São pontos de partida, não prescrição.

---

## A armadilha: fontes acessíveis não têm grego

**Atkinson Hyperlegible e OpenDyslexic não cobrem grego politônico.** Usá-las sem tratamento faria o grego sumir do PDF, com apenas um `Missing character` na saída — a mesma falha silenciosa de sempre.

O `preambulo-grego-cardo.tex` resolve: o português sai na fonte acessível e **a Cardo entra sozinha nos trechos gregos**, via `ucharclasses`, que observa o bloco Unicode de cada caractere. O `Scale=MatchLowercase` iguala a altura-x, para o grego não parecer menor que o texto ao redor.

O script carrega esse preâmbulo automaticamente quando a fonte escolhida não é a Cardo. Verificado no Handout 01: zero caracteres perdidos, com `θαυμασία`, `θαῦμα` e `φιλοσοφία` presentes no PDF.

Para saber o que a sua máquina tem, o `Testar-Fontes.ps1` agora sonda as fontes de acessibilidade e diz quais precisam do fallback.

---

## Uma armadilha de LaTeX

**A classe `article` só aceita 10, 11 e 12 pt.** Pedir `fontsize: 14pt` não dá erro — o valor é **ignorado em silêncio** e o texto sai em 10 pt. Foi assim que apareceu no teste: 13 pt e 14 pt produzindo o mesmo número de páginas que 11 pt.

Para corpos maiores é preciso trocar a classe:

```yaml
variables:
  documentclass: extarticle
  fontsize: 17pt
```

`extarticle` (pacote *extsizes*) aceita 8, 9, 10, 11, 12, 14, 17 e 20 pt. O script troca a classe sozinho quando o corpo passa de 12.
