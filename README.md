# Oficina — Pedra Angular

Ferramenta de bancada para montar edições físicas do corpus Pedra Angular.
Escolhe-se o texto, a tipografia, o formato, a encadernação e o acabamento;
a Oficina calcula a mancha gráfica pelo cânone dos nonos, estima a extensão,
desenha capa, página e lombada, e devolve a **ficha técnica com a lista de
corte** — o papel que se leva para a bancada.

Um arquivo. Sem build, sem framework, sem npm, sem rede em tempo de execução.
Abre com duplo clique.

## Como abrir

Duplo clique em `index.html` resolve para olhar. Para usar de verdade
(o navegador restringe `localStorage` e área de transferência em `file://`),
sirva a pasta:

```bash
python -m http.server 4180 --directory .
```

Depois abra `http://localhost:4180`.

## O que ela calcula

| Saída | Como |
| --- | --- |
| Mancha gráfica | cânone dos nonos, mais 20 mm de folga quando a costura é japonesa |
| Medida de linha | largura da mancha ÷ (0,3528 × corpo × largura média do caractere) |
| Extensão | palavras da obra ÷ palavras por página, arredondado para par |
| Espessura do miolo | número de folhas × espessura do papel, por família de costura |
| Comprimento do fio | soma do caminho real da agulha + 30% — não regra de bolso |
| Lista de corte | tapas, lombada, revestimento, guardas, cabeceado, estojo |

As constantes da casa — cerceta 3 mm, virada 15 mm, cava 7 mm, furo a 15 mm
da dobra — estão reunidas e nomeadas no topo do bloco de corte. Mudou ali,
a ficha inteira acompanha.

## Duas coisas que ela faz e não são óbvias

**O catálogo mora no `<body>`, não em JavaScript.** As listas de textos,
formatos, encadernações e materiais são HTML visível, e o configurador é
montado a partir delas. Sem JavaScript, a página entrega o catálogo inteiro
em texto — que é o que uma IA, um buscador ou um `curl` recebem. Com
JavaScript, o botão Φ mostra e esconde essa mesma seção. O dado existe uma
vez só no arquivo.

**A configuração inteira cabe na URL.** O endereço vira
`#encheiridion/garamond/11/folio-phi/azul/yotsume/branco/mole/phi`. Copiar o
link é salvar o projeto; colar é abri-lo. Sem servidor, sem cadastro, sem
banco.

## Estrutura

```
oficina/
├── index.html          ← tudo: dados, estilo, cálculo, desenho
├── fontes/
│   ├── Atkinson-*.woff2    interface (vendorizado do app-leitura)
│   ├── Atkinson-OFL.txt
│   └── LEIAME.md           EB Garamond e Cardo: onde baixar e como instalar
├── CLAUDE.md           instruções de projeto
└── README.md
```

## Limites conhecidos

- **EB Garamond e Cardo não estão no repositório.** Enquanto não estiverem,
  a prévia da capa cai em Georgia e o console loga 404. Ver `fontes/LEIAME.md`.
- A extensão em páginas é **estimativa**, não composição real. O número
  definitivo sai do LuaTeX.
- Não há cor de material com código: cor de papel e de tecido se fecha no
  mostruário físico, sob luz de dia, nunca na tela. A ficha tem campo em
  branco para o código do fornecedor.

## Versão para cliente

Esta é a ferramenta do ateliê e deve ficar cada vez mais técnica. A versão
voltada ao cliente é outra superfície, ainda não construída: mesma engrenagem,
linguagem amigável, nome e e-mail, e botão de enviar que leva ao pagamento.
Regra já decidida para ela: **se a opção está no site, dá para fazer** — opção
impossível some, não vira aviso técnico.

## Normas

Este projeto segue `NORMAS.md` do ecossistema (uma pasta acima). Em conflito,
a norma vence. Ver `CLAUDE.md`.

Ὁ Διαφορεύς παρῆν
