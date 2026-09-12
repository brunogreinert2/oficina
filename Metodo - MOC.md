---
id: metodo-moc
type: metodo
title: "Método — MOC"
escopo: vault
status: em_progresso
project: ufrgs
related:
  - "[[Converter DOCX para Markdown]]"
  - "[[Markdown para PDF com grego]]"
---

# Método — MOC

Notas sobre **como** o trabalho é feito, não sobre o conteúdo dele. Ferramentas, formatos, pipelines, decisões técnicas que valem para o vault inteiro — inclusive fora da graduação.

O critério para uma nota entrar aqui: se você fosse repetir o processo daqui a seis meses, precisaria redescobrir alguma coisa? Então é nota de método.

## Conversão e formatos

- [[Converter DOCX para Markdown]] — o que é um docx por dentro, por que Pandoc e não regex, receita testada e as três armadilhas
- [[Markdown para PDF com grego]] — por que `pandoc a.md -o a.pdf` falha (e por que às vezes falha em silêncio), defaults file, escolha de fonte
- [[Imprimir para encadernar]] — margens para costura japonesa, os dois perfis de caderno e as armadilhas de sintaxe do geometry
- [[Impressao acessivel]] — o que não se traduz da tela para o papel, receitas por necessidade e o fallback de grego nas fontes acessíveis
- [[Trabalho em norma ABNT]] — perfil `-d abnt` com margens, recuos e citações da NBR 14724, todos medidos no PDF

## Arquivos de configuração

`Metodo/pandoc/` guarda os arquivos prontos para instalar:

| Arquivo | Destino | Perfil |
|---|---|---|
| `academico.yaml` | `<userdir>\defaults\` | `-d academico` |
| `caderno.yaml` | `<userdir>\defaults\` | `-d caderno` |
| `caderno-frente.yaml` | `<userdir>\defaults\` | `-d caderno-frente` |
| `academico-neohellenic.yaml` | `<userdir>\defaults\` | `-d academico-neohellenic` |
| `preambulo-grego.tex` | `<userdir>\` | — |
| `Instalar.ps1` | rodar uma vez | instala tudo acima |
| `Testar-Fontes.ps1` | rodar de onde estiver | — |

## A fazer

- Transcrição de aula com faster-whisper — o `transcritor.py` está documentado no `CONVENCOES_UFRGS.md`, mas o processo de operação não
- OCR de PDF digitalizado
- Preparo de texto para o Pedra Angular (o que difere do fluxo acadêmico)

---

## Nota sobre a localização desta pasta

A intenção é que `Metodo/` viva na **raiz do Segundo Cérebro**, não dentro de `UFRGS/` — método serve ao vault inteiro, inclusive ao Pedra Angular. Está aqui provisoriamente porque `UFRGS/` era a única pasta acessível no momento da criação.

Ao mover, ajustar nas notas: `project: ufrgs` deixa de fazer sentido; trocar por `project: metodo` ou remover o campo.
