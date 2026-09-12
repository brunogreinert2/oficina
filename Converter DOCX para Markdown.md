---
id: metodo-docx-markdown
type: metodo
title: "Converter DOCX para Markdown"
ferramenta: Pandoc
escopo: vault
status: revisado
project: ufrgs
related:
  - "[[Metodo - MOC]]"
---

# Converter DOCX para Markdown

## O que é um .docx, afinal

Um arquivo `.docx` é um **ZIP**. Renomeie para `.zip`, descompacte, e você encontra:

```
word/document.xml       ← o texto
word/footnotes.xml      ← as notas de rodapé
word/media/image1.jpeg  ← as imagens
docProps/core.xml       ← autor, datas de criação e edição
```

O "documento" é uma pasta de XML compactada. Toda ferramenta de conversão apenas lê esse XML. Não há mágica em lugar nenhum.

## Por que regex não resolve

A tentação natural é arrancar as tags com uma expressão regular e ficar com o texto. Funciona para espiar o conteúdo, mas quebra em conversão séria — e o motivo é instrutivo.

O Word fragmenta o texto por **formatação**, não por sentido. No handout de 11/08/2025 do Zillig, a palavra grega θαυμασία está partida em três pedaços no XML:

```xml
maravilhamento [θα</w:t></w:r>
<w:proofErr w:type="spellStart"/>
<w:r ...><w:t>υμ</w:t></w:r>
<w:proofErr w:type="spellEnd"/>
<w:r ...><w:t xml:space="preserve">ασία] que os seres humanos...
```

O corretor ortográfico marcou `υμ` como erro de grafia e criou um bloco separado para sublinhar de vermelho. Do ponto de vista do arquivo, são três textos independentes que só por acaso ficam lado a lado na tela.

Consequência prática: buscar a string `θαυμ` dentro do `document.xml` **não encontra nada**. Ela não existe no arquivo.

## O que o Pandoc faz de diferente

O Pandoc não converte docx→markdown diretamente. Ele traduz para uma **representação intermediária** — uma árvore (AST) que descreve o documento em conceitos, não em formato. O mesmo trecho vira:

```json
{"t": "Str", "c": "maravilhamento"},
{"t": "Space"},
{"t": "Str", "c": "[θαυμασία]"}
```

Os três fragmentos remontados numa palavra só. Depois um "escritor" pega essa árvore e emite Markdown, HTML, LaTeX, o que for pedido.

É por isso que o Pandoc converte entre dezenas de formatos sem ter centenas de conversores: são **N leitores e M escritores** conversando por um meio comum, não N×M pares. Para ver a árvore: `pandoc arquivo.docx -t json | python -m json.tool`.

## A receita

```powershell
$src = "...\PASTA_COM_OS_DOCX"
$out = "...\PASTA_DESTINO"

New-Item -ItemType Directory -Force -Path $out | Out-Null
Push-Location $out

Get-ChildItem -Path $src -Filter *.docx | ForEach-Object {
    $slug = $_.BaseName -replace ' ','_'
    pandoc $_.FullName `
        -f docx `
        -t markdown_strict+footnotes+pipe_tables-raw_html `
        --wrap=none `
        --extract-media="$slug" `
        -o "$slug.md"

    (Get-Content "$slug.md" -Raw -Encoding UTF8) -replace '\\\[','[' -replace '\\\]',']' |
        Set-Content "$slug.md" -Encoding UTF8
}

Pop-Location
```

### Por que cada flag

| Flag | Motivo |
|---|---|
| `-raw_html` | Sem ela, imagens saem como `<img style="width:5.9in">` com a largura do Word embutida. Com ela, viram `![](caminho)` limpo. |
| `+footnotes` | Preserva as `[^1]` do autor. Sem isso, as notas de rodapé são perdidas ou viram texto solto. |
| `+pipe_tables` | Sem isso o Pandoc escreve literalmente `[TABLE]` e descarta o conteúdo. |
| `--wrap=none` | Evita quebra automática em 72 colunas, que polui o diff quando você editar depois. |
| `--extract-media` | Salva as imagens em disco. Sem isso elas ficam presas dentro do docx. |
| `-replace '\\\['` | O Pandoc escapa colchetes como `\[1\]`. O replace devolve `[1]` legível sem afetar footnotes nem links. |

## As três armadilhas

**Colisão de imagens.** O `--extract-media` sempre cria uma subpasta `media` dentro do caminho dado, e todo docx nomeia suas imagens `image1`, `image2`… Se todos os arquivos apontarem para o mesmo destino, o último sobrescreve as imagens do primeiro. Use uma pasta por documento, ou renomeie com prefixo.

**Espaço no caminho.** Link markdown com espaço no caminho quebra. Na primeira tentativa com os handouts, 41 de 51 links saíram inválidos por isso. O `-replace ' ','_'` no nome resolve.

**Tabelas de layout.** Quando o autor usa tabela invisível só para pôr duas imagens lado a lado, mesmo com `+pipe_tables` o Pandoc às vezes desiste e emite `[TABLE]`, perdendo as imagens. Solução: converter o mesmo arquivo também para `gfm`, que preserva a tabela em HTML, e recuperar de lá os `<img src>` e as legendas.

## O que o Pandoc não faz

Ele resolve o **formato**. Você resolve o **sentido**.

O Pandoc entrega o texto íntegro, com as notas de rodapé no lugar e as imagens extraídas. O que ele não sabe é que aquele bloco é uma definição, que aquela citação é de Estrabão, que aquele parágrafo em itálico era um título de seção. Nada disso está marcado semanticamente no docx — o autor deixou em itálico, e itálico é itálico.

Por isso toda conversão em lote precisa de uma segunda passada, e essa passada é leitura. Heurísticas ajudam (linha isolada, curta, em itálico, sem verbo conjugado, sem ponto final ≈ título), mas erram: na conversão dos handouts, a primeira versão promoveu legendas de museu e setas "↓" a cabeçalhos.

## Só espiar o conteúdo

Quando a intenção não é converter, mas apenas descobrir de que trata cada arquivo, regex serve e é instantâneo:

```python
import zipfile, re
xml = zipfile.ZipFile("arquivo.docx").read("word/document.xml").decode("utf8")
texto = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", xml)).strip()
print(texto[:300])
```

Leitura suja e descartável. Foi assim que os 23 handouts do semestre foram mapeados por assunto antes de qualquer conversão. Não guarde esse resultado — ele tem exatamente os defeitos descritos acima.

## Experimento

Renomeie um `.docx` que você conhece para `.zip`, descompacte, abra `word/document.xml` num editor de texto e procure uma palavra que você sabe que está lá. Ver um documento familiar virar sopa de tags é o momento em que a caixa preta deixa de ser preta.
