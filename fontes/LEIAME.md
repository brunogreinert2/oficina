# Fontes da Oficina

Nada aqui vem da internet em tempo de execução (NORMAS.md, LEI 3). Toda fonte
usada pela Oficina é arquivo nesta pasta.

## O que já está aqui

| Arquivo | Família | Licença |
| --- | --- | --- |
| `Atkinson-Regular.woff2` | Atkinson Hyperlegible 400 | OFL — `Atkinson-OFL.txt` |
| `Atkinson-Bold.woff2` | Atkinson Hyperlegible 700 | OFL — `Atkinson-OFL.txt` |

A Atkinson é a fonte da **interface**. Ela veio de
`app-leitura/scripts/rolo/fontes/` — é cópia vendorizada, não editar aqui.

## O que falta, e por que importa

EB Garamond e Cardo são as tipografias que os **volumes impressos** usam. A
Oficina desenha a prévia da capa com a fonte escolhida: sem os arquivos, as
três opções caem em Georgia e a prévia mostra sempre a mesma letra. O
configurador funciona; a prévia é que deixa de ser fiel.

Nenhuma das duas está nesta máquina — procurei em `node_modules`, nos
projetos e nas fontes do Windows.

### Onde baixar

As duas são OFL (livres, inclusive para uso comercial):

- **EB Garamond** — Georg Duffner e Octavio Pardo · `github.com/octaviopardo/EBGaramond12`
- **Cardo** — David Perry · `scholarsfonts.net/cardofnt.html`

Ou, para as duas, os pacotes prontos em `fontsource.org` (procurar por
`eb-garamond` e `cardo`), que já entregam `.woff2` subsetado.

### Como instalar

Solte os `.woff2` nesta pasta **com estes nomes exatos** — o
`@font-face` da Oficina já aponta para eles e acendem sozinhos, sem tocar em
código:

```
EBGaramond-Regular.woff2
EBGaramond-Italic.woff2
EBGaramond-SemiBold.woff2
Cardo-Regular.woff2
Cardo-Italic.woff2
Cardo-Bold.woff2
```

Baixe também o `OFL.txt` de cada uma e deixe ao lado, como a Atkinson tem
(N23: toda família embutida tem a licença junto).

### Como conferir que pegou

Abra a Oficina e rode no console:

```js
document.fonts.check('16px "EB Garamond"')
document.fonts.check('16px "Cardo"')
```

Duas vezes `true` e a prévia passa a mostrar a letra certa.

## Por que estas duas, e não outras

- **EB Garamond** tem grego politônico completo. É a razão de ela existir aqui:
  metade do acervo é grego antigo, e um Garamond sem politônico obriga a
  trocar de fonte no meio da página.
- **Cardo** foi desenhada para filologia clássica — grego, hebraico com pontos
  massoréticos, latim epigráfico. É a escolha certa para o Eclesiastes.
- **Atkinson Hyperlegible** não é uma terceira opção estética: é a linha
  acessível do catálogo. Larga de propósito, por isso a Oficina avisa quando
  ela não cabe no formato escolhido.
