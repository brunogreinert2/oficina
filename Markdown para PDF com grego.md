---
id: metodo-md-pdf-grego
type: metodo
title: "Markdown para PDF com grego"
ferramenta: "Pandoc + XeLaTeX"
escopo: vault
status: revisado
project: ufrgs
related:
  - "[[Metodo - MOC]]"
  - "[[Converter DOCX para Markdown]]"
---

# Markdown para PDF com grego

## O problema, com nome

`pandoc arquivo.md -o arquivo.pdf` falha com grego por **dois motivos diferentes**, e o segundo é o perigoso.

**Modo 1 — erro barulhento.** Sem `--pdf-engine`, o Pandoc usa **pdfLaTeX**, um motor de 1985 que não entende Unicode. Ele para com:

```
! LaTeX Error: Unicode character φ (U+03C6) not set up for use with LaTeX.
```

Chato, mas honesto: você sabe que deu errado.

**Modo 2 — falha silenciosa.** Com `--pdf-engine=xelatex` mas sem declarar fonte, o XeLaTeX usa Latin Modern, que não tem glifos gregos. O PDF **é gerado com sucesso** e o grego simplesmente não está lá. No teste com o Barnes: o PDF saiu com zero caracteres gregos, e o único aviso foi um `[WARNING] Missing character` perdido no meio da saída.

Este é o modo que produz a "surpresinha". Você imprime, entrega, e só descobre depois.

## A causa raiz

Três camadas, e cada uma pode falhar sozinha:

1. **O motor** precisa entender Unicode → XeLaTeX ou LuaLaTeX, nunca pdfLaTeX.
2. **A fonte** precisa ter os glifos → e "ter grego" não basta: o grego **politônico** (bloco U+1F00–U+1FFF, os `ᾶ ῥ ἐ ὕ ῶ`) é um bloco separado do grego moderno (U+0370–U+03FF). Muitas fontes cobrem o segundo e falham no primeiro.
3. **O idioma** precisa dos padrões de hifenização → `lang: pt-BR` exige o pacote `hyphen-portuguese` instalado no TeX.

O corpus da disciplina usa os três blocos. Levantamento nos textos do Barnes e nos 23 handouts:

| Bloco | Ocorrências | Exemplos |
|---|---|---|
| Latim acentuado | 8.654 | ã ç é ô ü |
| Pontuação tipográfica | 1.239 | – — “ ” … |
| Grego básico | 623 | φ λ ω μ σ |
| **Grego politônico** | **80** | ἀ ῥ ἐ ὕ ῶ ᾶ |
| Subscritos | 28 | ₀ ₁ ₂ ₃ |
| Colchetes angulares | 34 | ⟨ ⟩ |
| Sinais editoriais | 2 | ⸫ |

Oitenta caracteres politônicos num corpus de 300 mil. Basta um para a página sair errada.

## A solução: defaults file

O Pandoc lê um arquivo de configuração nomeado, e isso elimina o YAML por arquivo. O comando passa a ser, para sempre:

```powershell
pandoc arquivo.md -d academico -o arquivo.pdf
```

### Instalação

Rode, de dentro de `Metodo/pandoc/`:

```powershell
powershell -ExecutionPolicy Bypass -File .\Instalar.ps1
```

**A pasta de configuração não existe até você criá-la.** O Pandoc lê `%APPDATA%\pandoc\defaults\`, mas nunca a cria — nem o instalador do Pandoc cria. Numa máquina recém-instalada ela simplesmente não está lá, e é por isso que o caminho parece errado quando você vai conferir.

O `Instalar.ps1` faz as quatro coisas: descobre a pasta real (via `pandoc --version`, que a informa em `User data directory` — não confie no caminho decorado, ele muda conforme o tipo de instalação), cria as pastas, copia os arquivos e corrige o caminho absoluto do preâmbulo. No fim ele gera um PDF de sonda com grego politônico e avisa se algum glifo se perdeu.

Para fazer à mão, é isto:

```powershell
$dir = (pandoc --version | Select-String 'User data directory:') -replace '.*directory:\s*',''
New-Item -ItemType Directory -Force -Path "$dir\defaults"
Copy-Item .\academico.yaml, .\academico-neohellenic.yaml "$dir\defaults"
Copy-Item .\preambulo-grego.tex $dir
```

### Os arquivos

| Arquivo | Destino | Para quê |
|---|---|---|
| `Instalar.ps1` | rodar uma vez | cria as pastas e instala tudo |
| `academico.yaml` | `<userdir>\defaults\` | o padrão — uma fonte cobre tudo |
| `caderno.yaml` | `<userdir>\defaults\` | imprimir **frente e verso** e costurar |
| `caderno-frente.yaml` | `<userdir>\defaults\` | imprimir **só na frente** e costurar |
| `academico-neohellenic.yaml` | `<userdir>\defaults\` | quando quiser o grego em GFS NeoHellenic |
| `preambulo-simbolos.tex` | `<userdir>\` | setas, subscritos, angulares — usado por **todos** os perfis |
| `preambulo-grego.tex` | `<userdir>\` | usado só pelo neohellenic |
| `Testar-Fontes.ps1` | rodar quando precisar | descobre quais fontes suas servem |

O que o `academico.yaml` fixa: XeLaTeX como motor, fonte com cobertura politônica, A4 com margem de 2,5 cm, entrelinha 1.15, links coloridos, hifenização em português.

Para conferir se o Pandoc está mesmo lendo o arquivo: `pandoc --version` mostra a pasta, e `pandoc -d academico --print-default-data-file=x 2>&1` falha de forma diferente se o defaults não for encontrado. O teste honesto é gerar um PDF e ver se saiu em Palatino e não em Latin Modern.

## Símbolos que a fonte não tem

Nenhuma fonte de texto cobre tudo. A Palatino Linotype tem latim e grego politônico, mas **não tem setas, subscritos nem colchetes angulares** — e esses aparecem no corpus:

| Caractere | Ocorrências | De onde vem |
|---|---|---|
| ⟨ ⟩ | 34 | inserção editorial nos handouts (era `<...>` no Word) |
| → ↓ ↔ | 22 | diagramas dos handouts |
| ₀ ₁ ₂ ₃ | 28 | fórmulas do Barnes |
| ★ ≥ ∙ | 10 | notas próprias |
| ⸫ | 2 | artefato de conversão |

O sintoma é o aviso `Missing character: There is no → (U+2192)` — e, se você não olhar, o caractere some do PDF.

**A solução é o `preambulo-simbolos.tex`**, já incluído nos perfis. Ele desvia caractere por caractere para uma fonte que os tenha (Segoe UI Symbol, que vem com o Windows), mantendo o resto do texto na fonte principal.

Para acrescentar um caractere novo, copie uma linha e troque o código — que o próprio aviso do Pandoc informa:

```latex
\newunicodechar{→}{\FBsym{"2192}}
```

**Uma armadilha de sintaxe:** a forma intuitiva quebra o build.

```latex
% NÃO faça — quebra com "Argument of \MT@is@char has an extra }"
\newcommand\FB[1]{{\symbolfont #1}}
\newunicodechar{→}{\FB{→}}
```

O conflito é com o **microtype**, que o Pandoc carrega por padrão: passar o caractere como argumento de macro confunde o processamento dele. A forma que funciona usa o código hexadecimal em vez do caractere, dentro de `\bgroup...\egroup`:

```latex
\newcommand\FBsym[1]{\bgroup\symbolfont\symbol{#1}\egroup}
```

Verificado nos handouts reais: **zero caracteres perdidos**, setas e angulares presentes no PDF.

### Por que não é fallback automático

XeLaTeX não tem fallback de fonte — é preciso mapear um a um. LuaLaTeX tem (via `luaotfload.add_fallback`, ou `mainfontfallback` no Pandoc 3.1.11+), e resolveria tudo de uma vez. Não foi adotado aqui porque exige trocar o motor e depende de versão; se um dia a lista de mapeamentos ficar grande demais, vale reconsiderar.

Também tentei o `ucharclasses` (o mesmo pacote do preâmbulo grego) com os blocos `Arrows` e `SuperscriptsAndSubscripts`. Funciona para setas, mas deixou os subscritos passarem e as transições entre blocos adjacentes geram `Extra \endgroup`. Menos confiável que o mapeamento explícito.

## A fonte: Cardo

Todos os perfis usam **Cardo**, a mesma da identidade visual dos apps. É boa escolha por mérito próprio: David Perry a desenhou para classicistas e medievalistas, e ela cobre latim, grego politônico, hebraico e sinais filológicos — o que dispensa fallback justamente onde as outras falham.

A romana da Cardo deriva do tipo que Francesco Griffo cortou para **Aldo Manuzio em 1495**. Coincidência que vale registrar: o Handout 20 do Zillig, sobre a ontologia aristotélica, abre com a imagem da *Editio Princeps* das obras completas de Aristóteles — publicada por Aldo Manuzio em 1497. Imprimir os handouts em Cardo é imprimi-los na linhagem da primeira edição impressa de Aristóteles.

### Duas ressalvas práticas

**Cardo não tem Bold Italic.** Só Regular, Italic e Bold. Isso importa aqui: cinco handouts usam negrito+itálico (`***assim***`), justamente nas reconstruções de argumento com premissas numeradas. Sem tratamento, esses trechos caem numa fonte substituta. Os perfis resolvem assim:

```yaml
mainfontoptions:
  - "BoldItalicFont={Cardo Bold}"
  - "BoldItalicFeatures={FakeSlant=0.2}"
```

Usa o Bold e inclina artificialmente. Se o build reclamar que `Cardo Bold` não existe, o nome da família instalada pode ser outro (`Cardo-Bold`) — confira em Configurações → Fontes do Windows.

**Cardo roda pequena.** A x-height é menor que a da Palatino, então 11pt parece uns 10,5pt. Se no papel ficar miúdo, suba para 12pt — a mancha de 156 mm comporta sem estragar o número de caracteres por linha.

**Cardo não tem monoespaçada.** Os perfis mantêm Consolas para `código`.

### Alternativas

Rode `Testar-Fontes.ps1` para sondar o que a sua máquina tem. Outras que passam no teste de grego politônico: **Palatino Linotype** (vem com o Windows), **Libertinus Serif** ([releases](https://github.com/alerque/libertinus/releases)), **Cambria**, **DejaVu Serif**, **Liberation Serif**.

**GFS NeoHellenic** é excelente para grego mas fraca em latim. Use-a pelo `academico-neohellenic.yaml`, que a aplica só nos trechos gregos: o pacote `ucharclasses` detecta a entrada e saída do bloco Unicode e troca a fonte sozinho, sem você marcar nada no Markdown. O custo é compilação mais lenta.

## Se der errado, o diagnóstico é este

```powershell
pandoc arquivo.md -d academico -o teste.pdf 2>&1 | Select-String "Missing character"
```

Saída vazia significa que nenhum glifo se perdeu. Se aparecer algo, o caractere está no aviso: troque a fonte por outra da lista completa.

Erros por nome:

| Mensagem | Causa | Solução |
|---|---|---|
| `Unicode character ... not set up` | está usando pdfLaTeX | falta o `-d academico` |
| `Missing character: There is no φ` | fonte sem o glifo | trocar `mainfont` |
| `Undefined control sequence \l@portuges` | falta pacote de idioma | MiKTeX Console → instalar `hyphen-portuguese`, ou comentar `lang:` |
| `File 'ucharclasses.sty' not found` | falta o pacote | MiKTeX instala sozinho ao confirmar o prompt |
| PDF sai sem as imagens | caminhos relativos | rodar o pandoc **de dentro** da pasta do arquivo |

## O teste que vale

Antes de confiar num PDF com grego, extraia o texto de volta e conte:

```powershell
pdftotext teste.pdf - | Select-String -Pattern "[\u0370-\u1FFF]" | Measure-Object
```

Se o Markdown tem grego e a contagem der zero, você caiu no modo 2. Foi assim que a falha silenciosa apareceu no teste: PDF de 44 KB, gerado sem erro, com nenhum caractere grego dentro.
