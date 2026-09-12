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

## Rodar

```
python conferir.py     # ANTES de recarregar a aba
```

O sintoma de um `<script>` quebrado aqui e o mesmo das outras bancadas: a
pagina abre inteira, bonita, com as secoes VAZIAS — porque o script nao
chegou a rodar. Aconteceu duas vezes em 2026-09-11. O `conferir.py` confere
sintaxe, catalogo do `<body>`, furos declarados por costura, os canones, o
CONTRATO com o Gerador (campo que o `deEspecificacao()` de la exige e a
exportacao daqui nao escreve), a contagem de CAPITULO nas duas bancadas e
vocabulario morto. Ele ja estreou pegando um "LuaTeX" esquecido no acervo.

```
python C:/Claude/conferir_capitulos.py --tudo   # quem mexer em contarCapitulos()
```

O `conferir.py` chama a forma rápida deste conferidor (as bancadas e os
`_teste`). Quem mexer no `contarCapitulos()` daqui ou no `seccionar()` de lá
roda o `--tudo`, que passa o acervo inteiro do app-leitura pelas duas
implementações — 1 139 arquivos em três segundos. É o N68: caminho raro só
existe no corpus inteiro.

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
- **A regra das margens é catálogo, não constante.** `dados-canones` no
  `<body>`: nonos (o livro), compacta (bíblia e apostila, os mesmos
  denominadores um degrau abaixo), ABNT NBR 14724 (3 e 2 cm) e personalizada
  (quatro valores em mm). `calcular()` continua sendo a ÚNICA conta de
  geometria do ecossistema — o Gerador lê, não recalcula (proposta, seção 8).

- **Impressão do miolo espelha as margens ou não.** `frente-verso` é o livro: a
  interna é a da costura e troca de lado. `so-frente` é o trabalho acadêmico
  entregue em papel e o fukuro-toji: margem igual em toda página. Sem isto, a
  ABNT sairia com 3 cm do lado errado em metade das folhas.

- **Campo novo no hash entra no FIM, e campo ausente volta ao PADRÃO.** O
  estado inteiro vive no endereço; link que um cliente salvou continua abrindo.
  Ausente tem de voltar ao padrão e **não** ao que está na tela: colar um link
  antigo numa Oficina já aberta deixava o cânone da montagem anterior valendo,
  e a pessoa veria margens que o link não pede. Medido em 2026-09-11.

- **A lista de perfis do Gerador é GERADA aqui dentro.** Bloco
  `PERFIS-OFICINA:INICIO/FIM`, escrito por
  `pandoc/conferir_perfis.py --propagar` a partir de `pandoc/perfis.yaml` — a
  mesma fonte que abastece a bancada. Escrever os perfis à mão aqui seria uma
  segunda verdade (N56).

- **«Exportar para o Gerador» é o contrato entre as duas bancadas.** Grava o
  `especificacao.*.json` com os mesmos campos do Marco 0, mais `canone`,
  `canone_frase` e `impressao`. O Gerador arrasta o arquivo e compõe. Mudou
  campo aqui, confere o `deEspecificacao()` de lá — os dois lados do contrato
  moram em arquivos diferentes.

- **A PONTE TEM DUAS MÃOS (2026-09-12).** A ida leva a geometria; a volta traz
  a contagem. `retorno.*.json`, arrastado aqui como qualquer arquivo, troca a
  estimativa de páginas pelo número CONTADO na composição — e com ele mudam
  folhas, espessura do miolo, lista de corte e o desenho da lombada. Medido no
  Encheirídion (Fólio Φ, padrão): estimativa 14, composição 23. A estimativa
  não conhece título que come meia página, fim de parágrafo que perde meia
  linha, nota, capítulo que abre folha nova — e em grego a palavra é bem mais
  longa que os 6 caracteres do modelo.

- **O retorno VENCE, mas só o desta configuração.** A assinatura (obra ·
  formato · cânone · impressão · perfil · colunas) é a mesma dos dois lados;
  divergiu, a bancada volta à estimativa e DIZ que voltou. Número de material
  trocado em silêncio é o pior defeito de uma lista de corte: quem corta não
  tem como saber. O placar diz «contadas» ou «estimadas» em toda troca.

- **A geometria não volta do Gerador.** Ele devolve só o que não dá para saber
  sem compor. Devolver margem ou mancha faria as duas bancadas discutirem a
  mesma conta (proposta, seção 8).

- **A aba chama-se «Grade», não «Página».** O que se desenha aqui é a página
  VAZIA nos milímetros do papel; página composta, com texto dentro, é do
  Gerador. Chamar as duas de «Página» era metade da confusão sobre quem faz o
  quê — a outra metade era as duas lerem o mesmo `.md` sem dizer para quê.

- **A porta é «Arraste aqui o .md», como em todas as bancadas.** Foi pedido
  assim: o ecossistema inteiro abre pela zona de arrastar, e a Oficina não
  podia ser a exceção. O catálogo de oito obras desceu para EXEMPLOS,
  declarados como tal na tela — e nem tudo que se imprime é do acervo: um
  `.md` digitado à mão também vira volume. No dia em que houver um botão que
  abra a biblioteca do Pedra Angular inteira, o arrastar continua.

- **A Oficina LÊ um `.md` do acervo.** Até 2026-09-11 ela só conhecia oito
  obras escritas no catálogo, e a contagem de palavras delas movia tudo:
  páginas, folhas, espessura do miolo, lista de corte e a especificação
  exportada. Projetar um volume real com número de vitrine é projetar no
  escuro. Agora o arquivo entra por arrastar ou pelo botão da seção Texto,
  por `FileReader` (nunca `fetch`: a bancada abre em `file://`), e dele saem
  título, autor, licença, capítulos e palavras. **As palavras se contam como o
  Gerador conta** — `split` por espaço no arquivo inteiro —, porque duas
  contagens diferentes fariam as duas bancadas discordarem sobre o mesmo
  arquivo. Conferido: o Salmos do corpus dá 198 páginas estimadas, que é
  exatamente o número do contrato do Marco 0.

- **O CAPÍTULO também (2026-09-12), e a regra é UNIVERSAL.** Esta bancada
  contava `^## ` no arquivo cru; o Gerador contava as seções do `seccionar()`
  dele. Sobre o mesmo Encheirídion, «1 capítulos» aqui e «2 de 2 capítulos»
  lá; no Salmos, 150 e 151. Dois números na tela para a mesma coisa é o que o
  N56 proíbe.

  **E as duas estavam erradas**, o que só apareceu quando pararam de
  discordar: o Encheirídion tem 53 capítulos, e eles estão em `###`, porque o
  `## Texto` do corpus é invólucro. MEDIDO no acervo: 864 arquivos com o
  capítulo em `##`, 232 em `###`, 26 em `####`, 17 sem divisão nenhuma. Uma
  regra que conhece um nível de cor erra em 258 obras de 1 139.

  A regra que ficou não conhece nível nenhum: **o capítulo é o nível de
  cabeçalho que a obra MAIS REPETE** — título aparece uma vez, `## Texto`
  aparece uma vez, parte aparece poucas, capítulo aparece muitas. Empate,
  vence o mais fundo (`# Filemom` + `## Capítulo 1`). E **uma parte só não
  divide nada**: nível com um cabeçalho apenas é ZERO capítulos, a peça única.
  Profundidade não tem teto (N10) — `###`, `####` ou dezessete cerquilhas
  entram pela mesma porta.

  A prova de que é a regra certa não é argumento, é coincidência medida: ela
  devolve **53** para o Encheirídion e **peça única** para a Apologia, que é
  exatamente o que o catálogo desta bancada já dizia à mão, escrito antes de
  existir a conta.

- **A tela diz o NÚMERO e o NÍVEL: «53 capítulos em ###».** O nível é
  inferido, e inferência que não se mostra é adivinhação: quem olha tem de
  poder conferir contra o arquivo sem abrir o código. O `extensaoDaObra()`
  daqui e o do Gerador são a mesma função, e o conferidor compara as duas
  STRINGS — número igual dito com palavra diferente ainda faz quem lê achar
  que são coisas diferentes.

- **SEÇÃO é do Gerador, CAPÍTULO é da obra.** Ele secciona no nível do
  capítulo E em tudo mais raso (senão o `### Livro 2` das Diatribes ficaria
  pendurado no fim do capítulo anterior), então a folha de rosto e o
  `## Texto` também viram seção: Salmos 150 capítulos / 151 seções,
  Encheirídion 53 / 55. Esta bancada não calcula seção, porque não compõe —
  ela chega pelo `retorno.*.json`, junto com o nível.

- **Consequência medida, e vale saber antes de comprar papel:** com o nível
  certo, o Encheirídion no perfil Padrão (que abre capítulo em página nova)
  compõe **56 páginas**, não as 23 de quando ele era «um capítulo só». A
  estimativa desta bancada dizia 20. O caso extremo do acervo são as
  Meditações: 486 entradas numeradas em `####`, que viram 486 capítulos e
  ~500 seções — em perfil de página nova isso é meio milhar de páginas. O
  remédio existe e é o menu de abertura do Gerador (`corrido`); o que não
  pode é a bancada decidir isso sozinha e em silêncio.

- **O catálogo de textos é VITRINE, e a tela diz isso.** Enquanto o texto for
  de lá, um aviso lembra que a contagem é aproximada. PDF não entra na
  Oficina: PDF vira `.md` no Conversor, que é a bancada anterior.

- **Fonte sem arquivo vendorizado é aviso, não silêncio.** A EB Garamond está
  declarada e não tem `.woff2` em `gerador/fontes/`: o Gerador RECUSA compor
  com ela. A Oficina passou a dizer isso na tela — antes deixava projetar um
  volume inteiro numa fonte que não compõe.

- **O mesmo vale para as ESTAÇÕES das encadernações de caderno.** A lista de
  corte dizia «3 furos por caderno» para caderno único, copta e long stitch,
  e calculava o fio por uma fórmula que ignorava quantas estações existem.
  Agora `data-estacoes` (3 / 4 / 3) alimenta desenho, furação e fio, pela
  MESMA fórmula de alturas dos furos japoneses. Os desenhos deixaram de ser
  decorativos: a copta mostra a corrente que a faz abrir a 360°, o long stitch
  os pontos longos que atravessam a capa. **A capa dura ganhou o que não
  tinha**: ela é costurada em FITAS, e `fitasDaLombada()` diz quantas pela
  altura — antes quem fosse montar descobria na hora de costurar.

- **O número de furos é da COSTURA, não uma constante.** Yotsume e kōki são de
  quatro; asa-no-ha e kikkō pedem furos intermediários, e a lista de corte
  publicava "4 furos" para as quatro. Furar é irreversível. Agora o número
  vive no `<body>` (`data-furos`), e desenho, lista de corte e cálculo do fio
  saem todos dele. O desenho é esquemático — diz quantos furos e por onde o
  fio vai —, não é prancha de manual, e o texto diz isso.

- **A linha de produção da ficha dizia LuaTeX.** Nunca houve LuaTeX: quem
  compõe é o Gerador (Paged.js), quem imprime é a `prensa.py` e quem impõe é o
  `impor.py`. Ficha técnica que descreve um fluxo inexistente é pior que ficha
  nenhuma.

- **A entrelinha da estimativa vem do PERFIL, quando ele a declara.** As
  constantes por classe (1,35 serifada, 1,45 Atkinson) são de quando a Oficina
  não sabia qual perfil ia compor. O ABNT compõe a 1,725 (20,7 pt em corpo
  12): estimar por 1,35 daria 28 % de linhas a mais do que cabe — e a conta da
  Oficina é o contrato com o Gerador.

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

**Medido em 2026-09-11, pela primeira vez** (`python medir_contraste.py` — um
ADAPTADOR, não um segundo medidor: traduz os tokens `--ui-*` para os nomes que
a régua do app-leitura espera e entrega o trabalho a ela). Cada tema é medido
duas vezes: sobre o fundo da página e sobre a superfície dos cartões, que é
onde vive metade desta interface.

O resultado reprova em três pontos, e **dois deles são da casa inteira** — o
Gerador e o Corretor reprovam idêntico, medidos com a mesma régua:

| par | medido | piso | onde |
| --- | --- | --- | --- |
| contorno de componente (`--ui-linha`) | 1,7 a 2,4:1 | 3:1 (WCAG 1.4.11) | as três bancadas |
| acento dourado como TEXTO | 5,0 a 6,0:1 | 7:1 (da casa) | as três bancadas |
| alerta (`--ui-alerta`) | 5,3 a 6,3:1 | 7:1 | aqui e no Conversor (mesmo valor) |

Trocar o dourado, a linha ou o alerta é decisão de identidade visual do
ecossistema, não conserto de bancada — **não resolver em silêncio**. O alerta
(`#C87361`) tem um agravante: é um vermelho-salmão, e a casa não usa vermelho
como sinal por causa da protanomalia do Bruno (NORMAS). Ele vive aqui e no
Conversor, com o mesmo valor.

**A paleta tem uma verdade só, e um conferidor.** `C:/Claude/paleta.css` (8
tokens, 3 temas) e `python C:/Claude/conferir_paleta.py` — as quatro bancadas
têm de bater com ela. Cor nova se decide no laboratório, não aqui.

**O laboratório de cores JÁ cobre esta paleta** (desde 2026-09-11: seletor de
família, `Bancadas · --ui-*`). Antes disso, não: Ele é a bancada de temas do
app-leitura e mede a família `--color-*` (nove temas). As bancadas usam a
família `--ui-*` (três temas) — medido em 2026-09-11: Oficina, Gerador,
Corretor e Conversor têm valores IDÊNTICOS nos tokens que compartilham, então
elas são iguais entre si; o que difere de uma para outra é só quais tokens
extras cada uma declara. A paleta das bancadas é, portanto, uma segunda paleta
do ecossistema, que nunca passou pelo instrumento — e é por isso que as
reprovas acima só apareceram agora.

Ao medir contraste no navegador, **desligue as transições antes** (N69).
Medir logo após trocar de tema devolve o valor da transição, não o do tema.

## Tokens locais

(vazio — a Oficina usa apenas tokens `--ui-*` do ecossistema)

Ὁ Διαφορεύς παρῆν
