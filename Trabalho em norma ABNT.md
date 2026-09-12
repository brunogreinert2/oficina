---
id: metodo-abnt
type: metodo
title: "Trabalho em norma ABNT"
ferramenta: "Pandoc + XeLaTeX"
norma: "NBR 14724"
escopo: vault
status: revisado
project: ufrgs
related:
  - "[[Metodo - MOC]]"
  - "[[Markdown para PDF com grego]]"
---

# Trabalho em norma ABNT

```powershell
pandoc arquivo.md -d abnt -o arquivo.pdf
```

## O que o perfil entrega

Tudo medido no PDF gerado, não presumido:

| Item da norma | Exigido | Medido |
|---|---|---|
| Margem superior | 3 cm | 3,0 |
| Margem esquerda | 3 cm | 2,99 |
| Margem inferior | 2 cm | 2,0 |
| Margem direita | 2 cm | 2,0 |
| Corpo do texto | 12 | 12 |
| Entrelinha | 1,5 | 21,5 pt |
| Recuo de primeira linha | 1,25 cm | **12,5 mm** |
| Citação longa: recuo | 4 cm | **40,0 mm** |
| Citação longa: corpo | 10, simples | 10, simples |
| Nota de rodapé | 10, simples | 10, simples |
| Número de página | canto sup. direito, 2 cm da borda | **20,4 mm** |
| Seções | numeração progressiva | 1, 1.1, 1.1.1 |
| Alinhamento | justificado | justificado |

## Quatro coisas que só apareceram medindo

**O primeiro parágrafo depois de um título não recuava.** É comportamento padrão do LaTeX — tradição tipográfica anglo-saxã, em que o parágrafo de abertura não leva recuo. A convenção brasileira e o Word recuam todos. Resolvido com o pacote `indentfirst`.

**O número de página caía a 1,6 cm da borda, não a 2.** A posição do cabeçalho depende de `headsep`, a distância entre ele e o texto. Com `top=3cm` e `headsep=1cm`, o número ficava alto demais. Com `headsep=0.6cm`, bate os 2 cm da norma.

**A entrelinha do LaTeX não é a do Word.** `linestretch: 1.5` multiplica o *baselineskip*, que já parte de 1,2 — então o resultado é 21,5 pt, contra os ~20,7 pt do "1,5 linhas" do Word. Diferença de 4%, invisível a olho nu e dentro do que qualquer professor aceita. Ficou 1.5 porque é a convenção; quem quiser bater exato usa 1.44.

**O esticamento vazava para as notas de rodapé.** `linestretch` é global: sem tratamento, as notas saem com 1,5 também, contra a norma. O preâmbulo redefine `\footnote` para forçar espaçamento simples.

## Citação longa

No Markdown, o bloco iniciado por `>` vira citação recuada. O preâmbulo redefine o ambiente `quote` para o formato da norma: recuo de 4 cm, corpo 10, entrelinha simples e **sem aspas** — a norma dispensa as aspas justamente porque o recuo já marca a citação.

```markdown
> Aqui vai a citação com mais de três linhas, que sai
> recuada quatro centímetros da margem esquerda.
```

Citação curta (até três linhas) fica no corpo do texto, entre aspas, e não usa `>`.

## A fonte

A norma recomenda Arial ou Times New Roman. O perfil usa **Times New Roman**, que é o que a maioria dos professores de humanidades espera. Para trocar por Arial, mude só a linha `mainfont`.

O grego sai em **Cardo automaticamente**, pelo `preambulo-grego-cardo.tex`: a cobertura politônica da Times é incompleta, e sem isso os termos gregos sumiriam do PDF. Numa monografia de filosofia antiga isso seria fatal e silencioso.

## O que o perfil não faz

Capa, folha de rosto, sumário, resumo, lista de referências. Não são formatação: são partes do trabalho, e cada instituição tem exigências próprias. Escreva-as no próprio `.md` ou monte à parte.

Para referências automáticas a partir de um `.bib`, o Pandoc tem `--citeproc` com estilo ABNT — assunto para quando houver um trabalho real com bibliografia.

## Antes de entregar

Confira o que o **seu** professor pede. A NBR 14724 é a base, mas cada programa costuma ter um guia próprio que a estende ou contraria em detalhes — sobretudo em capa, numeração e citação. O perfil acerta a norma; o guia do curso vence a norma.
