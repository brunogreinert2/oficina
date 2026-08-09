# Procedência do EB Garamond

Mesma disciplina que o corpus aplica a um texto — qual edição, de quem,
verificada como — aplicada ao arquivo da fonte.

## O que está nesta pasta

**EB Garamond 12, versão 1.002, de Georg Duffner e Octavio Pardo.** Original,
sem modificação de terceiro.

Verificado em 2026-08-09 por três caminhos independentes:

**1. A tabela `name` do próprio binário.** É a única declaração que viaja
dentro do arquivo e não pode ser trocada por engano de pasta:

```
copyright   Copyright 2017 The EB Garamond Project Authors
            (https://github.com/octaviopardo/EBGaramond12)
família     EB Garamond
versão      Version 1.002
fabricante  Georg Duffner
designer    Georg Duffner and Octavio Pardo
```

**2. Identidade byte a byte com o clone.** O `.otf` desta pasta e o
`fonts/otf/EBGaramond-Regular.otf` do clone de
`github.com/octaviopardo/EBGaramond12` têm o mesmo MD5
(`4932018ee4630991c73a04d76c05a09c`).

**3. Ausência de glifo de fork.** Nenhum glifo com nome contendo `rcs` ou
`citation`. Quatro pontos de código em área de uso privado, coerente com a
fonte original — não com um acréscimo de notação.

## O tropeço que vale registrar

O repositório `octaviopardo/EBGaramond12` passou, em 2026, por um período em
que um fork conviveu com o original dentro dele:

| Data | Autor | O que fez |
| --- | --- | --- |
| 2026-01-19 | Deborah Khodanovich | acrescentou `Copyright 2025 … (RCS citation glyphs)` ao `OFL.txt` |
| 2026-01-19 | Deborah Khodanovich | reescreveu o `README.md` descrevendo o "EB Garamond RCS" |
| 2026-02-21 | dvorit-ai | **apagou** os binários do fork (`fonts/RCS Garamond OTF/`) |

Os binários do fork saíram; **a linha na licença e o texto do README ficaram.**
Quem clonar hoje recebe um `OFL.txt` e um `README.md` que falam de glifos que
não estão em nenhum arquivo do repositório.

Por isso o `EBGaramond-OFL.txt` desta pasta é a versão **anterior** a
2026-01-19 — a que corresponde exatamente a estes binários e à declaração de
copyright que eles carregam por dentro. Não é edição de licença: é escolher,
entre duas versões que o próprio projeto publicou, a que descreve o arquivo
que está aqui.

## A lição, para a próxima família

**A tabela `name` do binário manda; arquivo de texto ao lado, não.** `OFL.txt`
e `README.md` são soltos: viajam entre pastas, sobrevivem a forks, ficam para
trás quando o binário sai. A declaração que viaja dentro do arquivo é a que
vale.

Foi exatamente esse o erro cometido aqui na primeira leitura: concluir que a
fonte era um fork porque o texto ao lado dizia isso. Ler a fonte teria
resolvido em um comando:

```bash
python -c "
from fontTools.ttLib import TTFont
f = TTFont('EBGaramond-Regular.otf', lazy=True)
for nid in (0,1,5,8,9): print(nid, f['name'].getDebugName(nid))
"
```

## Cardo

`Cardo-*.ttf` versão 1.0451, de David J. Perry (`scholarsfonts.net`), baixado
de `cardo104.zip`. Tabela `name` limpa, sem terceiros. Licença em
`Cardo-OFL.txt`.
