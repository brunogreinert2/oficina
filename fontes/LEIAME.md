# Fontes da Oficina

Nada aqui vem da internet em tempo de execução (NORMAS.md, LEI 3). Toda fonte
usada pela Oficina é arquivo desta pasta.

## O que está instalado

| Arquivo servido | Família / peso | Licença |
| --- | --- | --- |
| `Atkinson-Regular.woff2` · `Atkinson-Bold.woff2` | Atkinson Hyperlegible 400 / 700 | `Atkinson-OFL.txt` |
| `EBGaramond-Regular.woff2` · `-Italic` · `-SemiBold` | EB Garamond 400 / 400 itálico / 600 | `EBGaramond-OFL.txt` |
| `Cardo-Regular.woff2` · `-Italic` · `-Bold` | Cardo 400 / 400 itálico / 700 | `Cardo-OFL.txt` |

Atkinson é a fonte da **interface** (vendorizada de
`app-leitura/scripts/rolo/fontes/` — não editar aqui). EB Garamond e Cardo são
as tipografias dos **volumes**, usadas na prévia da capa e da lombada.

## Cobertura de escrita — medida, não suposta

Lida dos arquivos com `fontTools`, não do que a documentação promete:

| Família | Latim | Grego politônico | Hebraico com niqud |
| --- | --- | --- | --- |
| Atkinson Hyperlegible | sim | **não** | **não** |
| EB Garamond | sim | sim | **não** |
| Cardo | sim | sim | sim |

**Cardo é a única das três que compõe as três escritas.** É por isso que a
Oficina avisa quando se escolhe o Eclesiastes com EB Garamond: o hebraico
cairia numa fonte de sistema e o livro sairia com dois desenhos de letra na
mesma página. Esse aviso é gerado a partir do atributo `data-escritas` de cada
fonte no catálogo — se um dia entrar uma família nova, medir antes de declarar.

Reproduzir a medição:

```bash
python -c "
from fontTools.ttLib import TTFont
f = TTFont('Cardo-Regular.woff2', lazy=True)
cmap = set()
for t in f['cmap'].tables: cmap |= set(t.cmap.keys())
print([hex(o) for o in (0x5D0, 0x1F00, 0xE7) if o not in cmap] or 'cobre tudo')
"
```

## Procedência

**EB Garamond 12 v1.002, de Georg Duffner e Octavio Pardo — original, sem
modificação de terceiro.** Verificado pela tabela `name` do binário, por
identidade byte a byte com o clone de `github.com/octaviopardo/EBGaramond12`,
e pela ausência de glifos de fork.

Há uma armadilha nesse repositório, documentada em
`EBGaramond-PROVENIENCIA.md`: o `OFL.txt` e o `README.md` que se baixa hoje
descrevem um fork ("EB Garamond RCS") cujos binários já foram removidos do
próprio repositório. Por isso o `EBGaramond-OFL.txt` desta pasta é a versão
anterior a essa alteração — a que corresponde a estes arquivos.

**Regra que ficou:** a tabela `name` do binário manda; `OFL.txt` e `README.md`
ao lado, não. Texto solto viaja entre pastas e sobrevive a forks; a declaração
que viaja dentro do arquivo é a que vale.

## De onde vieram e como reconverter

Os originais chegaram em `.otf` (EB Garamond) e `.ttf` (Cardo). O que se serve
é `.woff2`: metade do peso, mesmo desenho.

```
total  1 984 KB  →  915 KB   (−54%)
```

Os `.otf` e `.ttf` continuam no disco mas **não** vão para o repositório
(`.gitignore`) — são 2 MB que ninguém baixa e que se recuperam do pacote
original. Para reconverter, ou para acrescentar um peso novo:

```bash
python -m pip install fonttools brotli
python -c "
from fontTools.ttLib import TTFont
f = TTFont('EBGaramond-Regular.otf'); f.flavor = 'woff2'
f.save('EBGaramond-Regular.woff2')
"
```

## Se acrescentar uma família

1. Converter para `.woff2`.
2. **Medir a cobertura de escrita** e pôr o resultado em `data-escritas` no
   catálogo, dentro do `index.html`.
3. Trazer o `OFL.txt` e renomear para `<Familia>-OFL.txt` (N23: toda família
   embutida tem a licença ao lado).
4. Declarar o `@font-face` no topo do `index.html`.

## Por que estas três, e não outras

- **EB Garamond** — grego politônico completo. Metade do acervo é grego
  antigo, e um Garamond sem politônico obriga a trocar de fonte no meio da
  página.
- **Cardo** — desenhada para filologia clássica. A única com hebraico
  apontado, portanto a única possível para o Eclesiastes e para qualquer
  interlinear.
- **Atkinson Hyperlegible** — não é uma terceira opção estética: é a linha
  acessível do catálogo. Larga de propósito, e por isso a Oficina avisa quando
  ela não cabe no formato escolhido.
