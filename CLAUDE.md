# Instruções do projeto — Oficina

Ferramenta de bancada para montar edições físicas do corpus Pedra Angular.
Quarta superfície do ecossistema, ao lado de app-leitura, app-infantil e o
kit do rolo.

## Antes de qualquer alteração

Leia `NORMAS.md` — uma pasta acima, em `C:\Claude\NORMAS.md`. Ele é
normativo: onde diverge do código, o código está errado. O Anexo B
("Para agentes de IA") lista o que nunca se viola. Em conflito entre este
arquivo e as NORMAS, **as NORMAS vencem** — relatar o conflito, não resolver
em silêncio.

## Stack

Um arquivo HTML. Sem build, sem framework, sem npm, sem pré-processador.
Não introduzir nenhum dos quatro.

## O que é específico daqui

- **O catálogo mora no `<body>`.** Textos, tipografias, formatos,
  encadernações, fios, capas, acabamentos e materiais são listas HTML com
  `data-*`; o JavaScript lê delas e monta o configurador. **Não mover dado
  para objeto JavaScript** — é a LEI 2 aplicada a uma ferramenta, e é o que
  faz a página ser legível sem JS.
- **Φ abre o acervo** (essas mesmas listas), **Ξ abre o sumário da página**.
  Barra angular completa, LEI 8.
- **O estado inteiro vive no hash da URL.** Mexeu no formato do hash, quebrou
  todo link que um cliente já tenha salvo. Os ids de item são eternos (LEI 6)
  — `folio-phi`, `bolso-phi` e companhia seguem escritos com "phi" mesmo
  depois de o glifo virar Φ maiúsculo na tela.
- **Constantes de bancada** (cerceta, virada, cava, furo) ficam nomeadas num
  bloco só, no topo da lista de corte. Não espalhar número mágico pelo código.
- **A espessura do miolo é calculada uma vez** em `calcular()` e usada tanto
  pelo desenho da lombada quanto pela lista de corte. Não recalcular.

## Tipografia

`fontes/` é vendorizada e local (LEI 3, zero rede). A Atkinson veio de
`app-leitura/scripts/rolo/fontes/` — não editar aqui. EB Garamond e Cardo
ainda faltam; o `@font-face` já as espera pelos nomes exatos listados em
`fontes/LEIAME.md`.

## Acessibilidade

Piso do ecossistema, medido e não estimado: contraste 7:1 em texto corrido e
4,5:1 em acento e alerta, nos **três** temas; foco de teclado sempre visível;
alvo de toque 2,75rem; corpo de fonte em multiplicador, nunca pixel;
`prefers-reduced-motion`; `lang` e `dir` em todo trecho grego, hebraico e
latino — inclusive dentro do SVG da capa.

Ao medir contraste no navegador, **desligue as transições antes** (N69).
Medir logo após trocar de tema devolve o valor da transição, não o do tema.

## Tokens locais

(vazio — a Oficina usa apenas tokens `--ui-*` do ecossistema)

Ὁ Διαφορεύς παρῆν
