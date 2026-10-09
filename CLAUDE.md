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

- **O DOCUMENTO DIGITAL NASCE AQUI (2026-10-07).** Até 2026-10-06 a edição
  era escolha do Gerador, no momento de compor. Errado, e o Bruno mostrou por
  quê: num documento digital **as margens mudam**. Não há lombada, não há lado
  de dentro, não há costura comendo a margem interna — e se as margens mudam,
  não é o mesmo objeto. A decisão é de quem projeta o objeto.

  **A margem dos dois lados é a MÉDIA de interna e externa.** Pela média, e não
  por uma das duas, porque assim a **largura da mancha não muda**: mesma medida
  de linha, mesmas linhas por página, mesma contagem de páginas. O documento só
  desliza para o centro, e as duas versões continuam comparáveis. Medido (A4,
  nonos, copta): físico 23,33 / 46,67 e digital 35 / 35 — mancha 140 × 198 mm
  nas duas, 58 páginas nas duas.

  **A assimetria VERTICAL fica.** Ela não é da encadernação, é óptica: o olho
  põe o centro de uma página acima do centro geométrico, e um bloco centrado de
  verdade parece estar caindo.

  **A folga da costura japonesa some**, e aí a mancha alarga 20 mm — é a única
  largura que muda, e muda porque a costura deixou de existir. E a espessura do
  miolo vai a zero: um arquivo não tem folha nem lombada, e zero aqui faz a
  lista de corte e o peso do papel calarem sozinhos.

  O campo entra no FIM do hash (`edicao`) e na especificação (`edicao`), e o
  Gerador o põe no menu dele. Especificação antiga, sem o campo, é livro
  físico. Aceite: `gerador/teste_edicao.py`, que usa as duas bancadas.

- **A TIPOGRAFIA VIAJA NA ESPECIFICAÇÃO (2026-10-06).** Até aqui a
  especificação levava o `perfil` e não o corpo: o Bruno escolhia Cardo 12 e o
  Gerador compunha Cardo 11, porque lá o corpo é o do perfil. A medida de linha
  e as linhas por página que esta bancada calcula SÃO com o corpo escolhido —
  exportar um sem o outro faz dos dois números uma mentira. Agora
  `composicao.tipografia` leva fonte, corpo e entrelinha.

- **A ENTRELINHA DO PERFIL É PARA O CORPO DO PERFIL.** O padrão compõe 11/14,85
  (razão 1,35); mantendo 14,85 com corpo 12 a razão cai para 1,24 e o texto
  aperta. A entrelinha passou a escalar na MESMA RAZÃO que o perfil escolheu —
  não é conta nova, é a decisão do perfil aplicada ao corpo que se pediu.
  Medido: corpo 12 no perfil padrão dá 16,20 pt.

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

- **Fonte sem arquivo vendorizado é aviso, não silêncio.** O Gerador RECUSA
  compor numa família que não tenha `.woff2` em `gerador/fontes/`, e esta
  bancada diz isso na tela — antes deixava projetar um volume inteiro numa
  fonte que não compõe. **O caso que originou a regra saiu do catálogo em
  2026-10-06** (a EB Garamond, a pedido do Bruno: «nunca usei e gosto muito da
  Cardo»). A regra fica de pé para a próxima.

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

- **A COSTURA DO ATELIÊ (2026-09-19).** Dentro da casca
  (`atelie/index.html`), esta bancada atende `postMessage` com `pa:'atelie'` e
  aplica o papel pelas MESMAS funções do arrasto — nada de segunda porta de
  leitura. Ela se apresenta sozinha («ola, aceito ...»), porque a casca so
  entrega a quem cumprimenta: `<iframe>` recem-criado tem um `about:blank` com
  `readyState` 'complete', e postar para ele perde o papel sem erro nenhum
  (medido: o .md sumia e a especificacao entrava). Aberta sozinha, por duplo
  clique, `window.parent === window` e nada disso roda.

- **O CORPO É A ESCADA INTEIRA; OS CINCO SÃO ATALHO (2026-10-08).** Pedido do
  Bruno: «uma caixa com os números e eu só clico», como no Writer. O catálogo
  `dados-corpos` passou de cinco a **21 degraus**, do aparato crítico (6 pt) ao
  cartaz (48 pt); os cinco de sempre levam `data-atalho` e **são eles que viram
  cartão**, o resto mora na caixa ao lado (`#sel-corpo`).

  **Um catálogo só, e não dois**: duas listas seriam duas verdades, e no dia em
  que alguém acrescentasse o 13 a uma delas a outra continuaria sem. `CORPOS` é
  a escada; `CORPOS_ATALHO` são os cinco, e é deles que o «surpreenda-me»
  sorteia — sortear 48 pt não seria surpresa, seria defeito.

  Nada mais precisou mudar: a entrelinha já escalava na razão do perfil desde
  2026-10-06, então 13 pt compõe a 17,55 pt sozinho. MEDIDO de ponta a ponta
  (11 · 12 · 13 · 15), e `teste_tipografia.py` cobre 13 e 15 **por não serem
  atalho**.

- **O NOME É O PRIMEIRO YAML DE UM ARQUIVO (2026-10-09).** Decisão do Bruno:
  «os arquivos têm de ser reconhecíveis antes mesmo de abrir — em algum momento
  alguém tira da pasta e nunca mais sabe o que é aquilo sem abrir». Os dois
  exportadores batizam pela CONVENÇÕES 1.1, com a OBRA primeiro:
  `especificacao.<obra>.<formato-perfil-canone>.json` e `retorno.<obra>.json`.

  **`nomeDoAcervo()` é COPIADO nas duas bancadas** — não há módulo partilhado
  num arquivo só (LEI 3), é a solução do `extensaoDaObra()` — e o
  `oficina/conferir.py` compara os dois trechos **caractere a caractere**.
  Testado quebrando.

  **Elas já divergiam:** com `author: null` nos Salmos a Oficina devolvia vazio
  e o Gerador devolvia «null_Salmos_…», porque um leitor de YAML descarta o
  nulo e o outro o entrega como a palavra. Campo vazio e campo nulo são a mesma
  coisa, e isso se decide num lugar só (`campoDe`).

  **Sem autor não há nome de acervo:** devolver só o título seria um nome que
  não cumpre a regra e parece cumprir. Devolve vazio, e o exportador fica com o
  nome de sempre. Aceite: `gerador/teste_nome.py`.

- **NAO SE ENCADERNA UM ARQUIVO (2026-10-09).** Pedido do Bruno, e ele tinha
  achado o defeito ao vivo: a especificação do Fédon saiu com `edicao: digital`
  **e** `encadernacao: yotsume`, com a folga da costura japonesa zerada — uma
  costura que não existe comendo uma folga que não existe.

  A edição digital e a encadernação «nenhuma» são **a mesma decisão vista de
  dois lados**: qualquer um basta, e `sincronizarDigital()` acende o outro.
  Desligar devolve a encadernação ao padrão, porque um objeto físico precisa de
  uma. **E arquivo não tem folha** — as folhas vão a zero como a espessura já
  ia, senão o colofão publicaria «6 folhas» de uma coisa que não é papel. O
  sorteio do «surpreenda-me» não a tira: o botão promete um volume.

- **O FIO GOLDEN ENTROU, O VERMELHO SAIU (2026-10-09).** O Golden é a mesma
  Círculo Linho do Anil Profundo (tex 369, 75 % algodão e 25 % linho), noutra
  cor; o vermelho cinábrio não tem nada a ver com a identidade visual da casa.

  **O Golden fica em `dados-fios` e NÃO em `dados-estoque`:** aquela é a lista
  do que SERVE, esta é a gaveta — um item por uso, e o Bruno ainda não o tem. O
  `conferir.py` reprovou a tentativa em dez segundos, corretamente.

- **A SÉTIMA DECISÃO DA CAPA: ONDE ELA SAI (2026-10-09).** «O pdf da capa tem
  como ficar junto no arquivo completo? Eu pretendo fazer duas versões, a
  digital para enviar, e depois para imprimir e encadernar.» `capaJunto`, no
  FIM da tabela como toda decisão nova (LEI 6).

  **A exportação repetia a tabela à mão, e a decisão nova não chegou ao
  Gerador** — decisão exportada e não lida não dá erro: a capa sai sem aquilo e
  ninguém desconfia. Agora o bloco `capa` da especificação **percorre a
  tabela**.

  **E a NBR não legisla sobre em que arquivo a capa vive:** ela fala do
  documento, não da entrega. `norma: null` significa «a norma cala aqui», e
  `capaForaDaNorma()` pula quem não tem norma — **uma norma que acusa o que não
  legisla ensina a ignorar os avisos dela.**

- **O ATALHO NÃO GUARDA ESTADO, MAS TEM DE SE VER (2026-10-09).** «Clica em
  cima e nada acontece, não fica mais escura como se estivesse marcada» —
  Bruno, no dia seguinte à entrega, com o aceite todo verde.

  Era verdade: nada acontecia mesmo. O cartão nascia com `ativo:false` fixo
  (atalho não é estado, foi a exigência dele) **e as seis decisões do `obra`
  SÃO as de fábrica** — numa tela recém-aberta não havia o que mudar. Eu tinha
  confundido *não guardar estado* com *não mostrar nada*.

  O aceso é **LIDO das decisões**, não guardado: `atalhoDaCapaAceso(a)` compara
  os valores do atalho com o estado. Aceso quer dizer «as decisões na tela são
  exatamente estas», e mexer numa delas apaga o cartão sozinho. Continua sem
  estado, e agora se vê.

  **Cada atalho declara TODAS as decisões da capa, a norma inclusive.** Medido:
  `obra` e `apostila` calavam sobre a norma, e clicar em «Trabalho em norma» e
  depois em «Obra» deixava a ABNT ligada — a tela acusava «fora da norma» em
  três decisões de uma capa de obra, que não tem norma nenhuma. Atalho que
  escreve seis decisões de sete não é atalho: é resíduo.

  **E o aceite não pegava porque media o estado, não o gesto:** ele punha o
  `estado` à mão e exportava, sem nunca passar por onde o dedo passa. A prova
  nova CLICA no cartão e lê o `aria-pressed`, que é o que a folha de estilo lê
  para escurecer (`.ficha[aria-pressed=true]`).

- **A CAPA É DECIDIDA AQUI (2026-10-09), E NÃO TEM ESPÉCIES.** Decisão do
  Bruno: «a capa é integrante, são alguns metadados e perfis carregados» — e a
  ressalva que desenhou tudo: «não vamos deixar isso se tornar os perfis
  astigmatismo, vista cansada, que obrigavam a lembrar o que cada uma fazia».

  **Seis decisões independentes**, derivadas dos quatro modelos que ele
  desenhou no Writer em setembro: timbre · coleção · autor e atribuição ·
  lista das peças · adorno · pé. O título não é decisão — capa sem título não
  é capa. Tabela `CAPA`, irmã da `PAGINACAO`, e a ordem dela é a ordem no
  hash.

  **Os três atalhos (obra · apostila · trabalho em norma) NÃO SÃO ESTADO:**
  clicar escreve as seis e some. Depois de clicar, o que se vê são as
  decisões. É isso que os separa de um perfil — lá o pacote ficava, e era
  preciso saber de cor o que ele continha.

  **A ABNT não é espécie: é NORMA.** Distinção do Bruno. Norma é um fato sobre
  o objeto, não um preset: `capaNorma` é decisão de verdade, ela acende o que
  a NBR manda e `capaForaDaNorma()` lista o que diverge. A tela diz «FORA DA
  NORMA: a NBR pede X» e **não tranca** — e a especificação leva
  `fora_da_norma` para o Gerador e a ficha poderem repetir.

  **O timbre sai do front matter** (`instituicao`, `unidade`, `disciplina`),
  como tudo o mais: a capa é gerada, nunca digitada. Pedido e ausente, o
  Gerador conta quantas linhas faltam e a prensa avisa — calar seria o defeito
  da página de dados.

- **A PAGINAÇÃO É DAQUI, E O PERFIL VIROU ATALHO (2026-10-07).** Decisão do
  Bruno: «tudo tem que ser personalizável (…) os perfis têm de ser atalhos pra
  quem já sabe o que quer, de resto é teste na base do olhômetro».

  Seis decisões saíram da gaiola do perfil e viraram catálogo no `<body>`:
  notas, alinhamento do corpo, alinhamento do título, adorno, cabeçalho
  corrente e hifenização. **Uma TABELA (`PAGINACAO`) e não seis blocos
  copiados** — as seis têm o mesmo desenho, e seis cópias seriam seis lugares
  para esquecer um detalhe na sétima. **A ordem da tabela é a ordem no hash**,
  e por isso é eterna (LEI 6): decisão nova entra no fim, nunca no meio.

  `paginacaoEfetiva()` resolve o valor CONCRETO para a especificação — «como o
  perfil manda» é escolha de tela; na especificação seria pergunta sem
  resposta. O perfil declara o que SUGERE em `data-*`, propagado do
  `perfis.yaml`, e a tela mostra isso embaixo de «como o perfil manda», para a
  escolha não depender de memória — que foi a queixa que originou tudo.

- **O PERFIL «PERSONALIZADO» (2026-10-07).** Ponto de partida neutro, no fim
  da lista. O que o distingue do Padrão: o Padrão é uma ESCOLHA EDITORIAL
  (grega no alto, justificado, cabeçalho corrente), feita por alguém que
  decidiu; o Personalizado não decide o que não precisa — sem adorno, sem
  cabeçalho. «Desses personalizados surgirão com o tempo novos nomes
  companheiros dos dislexia e astigmatismo»: combinação que provar que vale
  vira perfil com nome, no `perfis.yaml`, e passa a ser atalho também.

- **ONDE A NOTA CAI é decisão daqui (2026-10-07).** Estava presa ao perfil, e
  o perfil amarrava duas coisas sem relação: Padrão 11 pt / ao pé, Vista
  cansada 12 pt / **fim de capítulo**. Quem quisesse corpo 12 com nota ao pé
  tinha de saber de cor qual perfil não serve — foi o Bruno quem apontou.

  Está aqui pelo mesmo motivo da abertura: **muda a conta de papel**. Medido na
  Apologia em A4 corpo 12: 42 páginas com as notas no fim contra 34 ao pé.
  Lista `dados-notas` no `<body>`, campo no FIM do hash, e `composicao.notas`
  na especificação com valor CONCRETO, resolvido por `notasEfetivas()` — «como
  o perfil manda» é escolha de tela; na especificação seria pergunta sem
  resposta. O perfil declara a sua em `data-notas`, propagado do `perfis.yaml`.

- **A ABERTURA DE CAPÍTULO é decisão da Oficina (2026-09-18).** Menu novo
  («como o perfil manda» · página nova · corrido), lista `dados-aberturas` no
  `<body>`, campo no FIM do hash, e `composicao.abertura_de_capitulo` na
  especificação — sempre com valor CONCRETO, resolvido por `aberturaEfetiva()`.
  Está aqui porque é **a escolha que mais mexe na conta de papel** (medido nos
  Salmos: 300 páginas contra 244) e papel é o custo do objeto, que é o que esta
  bancada projeta. O perfil passou a declarar a sua abertura também aqui
  (`data-abertura`, gerado pelo `conferir_perfis.py --propagar`). A lista é
  FECHADA e o `conferir.py` a compara com o menu do Gerador (testado
  quebrando: id a mais, id trocado). **A ESTIMATIVA de páginas ainda não usa a
  abertura** — continua contando palavras por página, e é por isso que ela erra
  314 % no Encheirídion com página nova. Está declarado, e é trabalho da
  proposta, seção 8.

- **Materiais da bancada: o que se USA, declarado (2026-09-15).** Lista
  `dados-estoque` no `<body>`: Pólen 80 g/m² (Suzano) no miolo, Offset
  240 g/m² (Quinto Império) na capa, linha Círculo Linho cor Anil Profundo
  (75 % algodão, 25 % linho, tex 369), cera de abelha. As listas de materiais e
  insumos dizem o que SERVE; esta diz o que está na bancada, e vai na
  especificação (`materiais`) para o colofão do Gerador publicar papel, linha e
  peso. **Um item por uso**: dois papéis de miolo sem menu fariam a exportação
  levar o primeiro em silêncio, e o `conferir.py` reprova (testado quebrando:
  dois miolos, papel sem gramatura, uso desconhecido). No dia do papel Horller:
  acrescentar o item E fazer o menu.

- **A regra do miolo é UMA função: `regraDoMiolo()`.** Quantas páginas cabem
  numa folha de papel e de que tamanho é a folha — usada por folhas, espessura,
  lista de corte e peso do colofão. Escrever a regra num lugar só expôs dois
  defeitos: **só frente contava as folhas como frente e verso** (metade do
  papel; agora a japonesa leva 1 página por folha e o caderno 2 por folha
  dupla) e **o fukuro-toji saía na lista de corte com folha «l × a»**, quando
  a folha dele é dupla, dobrada na borda externa (a espessura já contava
  0,22 mm por folha dupla). Frente e verso não muda: conferido, japonesa 14
  páginas → 7 folhas, copta 12 → 3. Capa de papel só se pesa na japonesa
  (`pecasDaCapa()`): nas outras a peça depende da lombada.

- **A espessura do miolo é calculada uma vez** em `calcular()` e usada tanto
  pelo desenho da lombada quanto pela lista de corte. Não recalcular.

## Tipografia

`fontes/` é vendorizada e local (LEI 3, zero rede). A Atkinson veio de
`app-leitura/scripts/rolo/fontes/` — não editar aqui. A Cardo ainda falta; o
`@font-face` já a espera pelo nome exato listado em `fontes/LEIAME.md`.

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
