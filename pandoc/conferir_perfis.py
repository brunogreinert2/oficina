# -*- coding: utf-8 -*-
"""
conferir_perfis.py — denuncia divergência entre as três coisas que dizem os
mesmos números tipográficos:

  1. perfis.yaml            (a verdade, nesta pasta)
  2. os *.yaml do pandoc    (consumidor 1, nesta pasta)
  3. gerador/perfis.yaml    (consumidor 2, cópia vendorizada)

Existe por causa do N56. O gerador_rolo.py bifurcou em 538 linhas e nada
avisou; a única defesa barata contra isso é um script que grita.

Não conserta nada sozinho, exceto com --propagar, que reescreve a cópia
vendorizada do Gerador a partir desta pasta. O caminho contrário nunca existe:
a cópia nunca volta para a origem.

Sem dependência: só biblioteca padrão. Um leitor de YAML mínimo, porque este
arquivo tem de rodar na máquina do Bruno sem pip install (LEI 3 no espírito).

    python conferir_perfis.py
    python conferir_perfis.py --propagar
"""

import hashlib
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(AQUI, "perfis.yaml")
VENDOR = os.path.normpath(os.path.join(AQUI, "..", "..", "gerador", "perfis.yaml"))
GRADE = os.path.normpath(os.path.join(AQUI, "..", "..", "gerador", "index.html"))
# A Oficina tambem precisa saber quais perfis existem: e nela que se escolhe o
# perfil antes de exportar a especificacao. A lista vai GERADA para la pelo
# mesmo motivo que vai para o Gerador — uma verdade so (N56).
VITRINE = os.path.normpath(os.path.join(AQUI, "..", "index.html"))

# Os marcadores dentro do index.html do Gerador. O bloco entre eles é GERADO
# (N2, N57) e a próxima propagação o sobrescreve — não editar à mão lá.
MARCA_INICIO = "<!-- PERFIS:INICIO — gerado, não editar -->"
MARCA_FIM = "<!-- PERFIS:FIM -->"
MARCA_OF_INICIO = "<!-- PERFIS-OFICINA:INICIO — gerado, não editar -->"
MARCA_OF_FIM = "<!-- PERFIS-OFICINA:FIM -->"

# LaTeX parte de um baselineskip de 1,2 — ver o cabeçalho do perfis.yaml e o
# comentário medido do abnt.yaml. Sem este fator a comparação abaixo acusaria
# divergência em todo perfil, que é ruído, não sinal.
BASELINESKIP_LATEX = 1.2

# Quanto de folga se aceita entre a entrelinha em pontos e o linestretch do
# pandoc antes de virar reclamação. 2% é o arredondamento de escrever 19.4 em
# vez de 19.44; acima disso alguém mexeu num só dos dois.
FOLGA = 0.02


def ler_yaml_raso(texto):
    """Lê o suficiente do nosso perfis.yaml: mapas aninhados por indentação,
    escalares, listas em linha. Não é um parser de YAML e não tenta ser — é o
    parser burro de propósito do N7 aplicado a outro formato. Se o perfis.yaml
    passar a precisar de mais que isto, a resposta é simplificar o perfis.yaml."""
    raiz = {}
    pilha = [(-1, raiz)]
    linhas = texto.split("\n")
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        i += 1
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        recuo = len(linha) - len(linha.lstrip())
        corpo = linha.strip()
        if corpo.startswith("- "):
            continue                      # listas de itens: não usadas aqui
        if ":" not in corpo:
            continue
        chave, _, valor = corpo.partition(":")
        chave, valor = chave.strip(), valor.strip()
        while pilha and pilha[-1][0] >= recuo:
            pilha.pop()
        pai = pilha[-1][1]
        if valor in ("|", ">", "|-", ">-"):
            # Escalar de bloco. Tem de virar TEXTO, não mapa: as linhas de
            # dentro são prosa e várias têm dois-pontos. Tratá-las como pares
            # chave/valor fazia `divergencia` virar um dicionário vazio — e um
            # dicionário vazio é falso, então o perfil `padrao` aparecia como
            # "DIVERGE SEM EXPLICACAO" tendo a explicação escrita ao lado.
            bloco = []
            while i < len(linhas):
                seg = linhas[i]
                if seg.strip() and (len(seg) - len(seg.lstrip())) <= recuo:
                    break
                bloco.append(seg.strip())
                i += 1
            pai[chave] = " ".join(x for x in bloco if x).strip()
        elif valor == "":
            novo = {}
            pai[chave] = novo
            pilha.append((recuo, novo))
        else:
            pai[chave] = converter(valor)
    return raiz


def converter(v):
    v = v.strip()
    if v.startswith("#"):
        return None
    v = re.sub(r"\s+#.*$", "", v).strip()
    if v.startswith("[") and v.endswith("]"):
        return [converter(x) for x in v[1:-1].split(",") if x.strip()]
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v in ("true", "false"):
        return v == "true"
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def linestretch_do_pandoc(caminho):
    """O `linestretch:` que está HOJE no .yaml do pandoc. Lê a linha crua: o
    arquivo é do pandoc, não nosso, e não se deve assumir estrutura dele."""
    if not os.path.exists(caminho):
        return None
    for linha in io.open(caminho, encoding="utf-8"):
        m = re.match(r"\s*linestretch\s*:\s*([\d.]+)", linha)
        if m:
            return float(m.group(1))
    return None


def fontsize_do_pandoc(caminho):
    if not os.path.exists(caminho):
        return None
    for linha in io.open(caminho, encoding="utf-8"):
        m = re.match(r"\s*fontsize\s*:\s*([\d.]+)\s*pt", linha)
        if m:
            return float(m.group(1))
    return None


def main():
    propagar = "--propagar" in sys.argv
    texto = io.open(ORIGEM, encoding="utf-8").read()
    dados = ler_yaml_raso(texto)
    perfis = dados.get("perfis", {})

    queixas = []
    notas = []

    print("perfis.yaml versao %s, gerado em %s" %
          (dados.get("versao"), dados.get("gerado_em")))
    print("%d perfis, %d familias de fonte\n" %
          (len(perfis), len(dados.get("fontes", {}))))

    # ---- 1. cada perfil contra o .yaml do pandoc que ele diz derivar --------
    cab = "%-14s %6s %8s %8s %8s  %s"
    print(cab % ("perfil", "corpo", "entrel.", "razao", "pandoc", "situacao"))
    print("-" * 72)
    for nome, p in perfis.items():
        corpo = p.get("corpo_pt")
        ent = p.get("entrelinha_pt")
        declarado = p.get("pandoc_linestretch")
        arquivo = p.get("pandoc_perfil")
        if corpo is None or ent is None:
            queixas.append("%s: sem corpo_pt ou entrelinha_pt" % nome)
            continue
        razao = ent / corpo
        efetivo = (declarado * BASELINESKIP_LATEX) if declarado else None

        real = linestretch_do_pandoc(os.path.join(AQUI, arquivo or ""))
        if arquivo and real is None:
            queixas.append("%s: nao achei linestretch em %s" % (nome, arquivo))
        elif real is not None and declarado is not None and abs(real - declarado) > 1e-9:
            queixas.append(
                "%s: perfis.yaml diz pandoc_linestretch %s, mas %s tem %s. "
                "Alguem mexeu num so." % (nome, declarado, arquivo, real))

        corpo_pandoc = fontsize_do_pandoc(os.path.join(AQUI, arquivo or ""))

        situacao = "ok"
        if efetivo and abs(razao - efetivo) / efetivo > FOLGA:
            # Divergencia explicada no proprio perfil nao e queixa: e escolha
            # registrada. Sem explicacao escrita, e defeito.
            if p.get("divergencia"):
                situacao = "diverge do pandoc (explicado no perfil)"
                notas.append("%s: compoe a %.3f, o pandoc a ~%.3f" %
                             (nome, razao, efetivo))
            else:
                situacao = "DIVERGE SEM EXPLICACAO"
                queixas.append(
                    "%s: compoe a %.3f e o pandoc a ~%.3f, e nao ha campo "
                    "`divergencia` dizendo por que." % (nome, razao, efetivo))
        if corpo_pandoc and abs(corpo_pandoc - corpo) > 1e-9:
            if p.get("divergencia"):
                notas.append("%s: corpo %g aqui, %g no %s" %
                             (nome, corpo, corpo_pandoc, arquivo))
            else:
                queixas.append("%s: corpo %g aqui e %g em %s, sem explicacao."
                               % (nome, corpo, corpo_pandoc, arquivo))

        print(cab % (nome, "%g" % corpo, "%.2f pt" % ent, "%.3f" % razao,
                     ("%.2f" % declarado) if declarado else "—", situacao))

    # ---- 2. a fonte de cada perfil existe e foi medida ----------------------
    fontes = dados.get("fontes", {})
    for nome, p in perfis.items():
        f = p.get("fonte")
        if f not in fontes:
            queixas.append("%s: fonte '%s' nao esta declarada em `fontes`." % (nome, f))
        elif fontes[f].get("largura_medida") is False:
            notas.append("%s: a largura media da %s e ESTIMADA — a medida de "
                         "linha deste perfil e palpite." % (nome, f))

    # ---- 3. a copia vendorizada do Gerador ---------------------------------
    print()
    h = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    if propagar:
        escrever_vendor(texto, h)
        print("propagado para %s" % VENDOR)
        n = escrever_tabela_no_body(dados)
        print("tabela de %d perfis escrita no <body> de %s" % (n, GRADE))
        n = escrever_lista_na_oficina(dados)
        print("lista de %d perfis escrita no <body> de %s" % (n, VITRINE))
    elif not os.path.exists(VENDOR):
        queixas.append("a copia do Gerador nao existe. Rode com --propagar.")
    else:
        alvo = io.open(VENDOR, encoding="utf-8").read()
        m = re.search(r"sha-256 da origem:\s*([0-9a-f]{64})", alvo)
        if not m:
            queixas.append("a copia do Gerador esta sem carimbo de origem (N56).")
        elif m.group(1) != h:
            queixas.append(
                "a copia do Gerador foi carimbada com outro sha-256: ela esta "
                "VELHA ou foi editada no destino. Rode com --propagar.")
        else:
            print("copia do Gerador: em dia (sha-256 %s...)" % h[:12])

    # ---- veredito ----------------------------------------------------------
    print()
    for n in notas:
        print("  nota  · %s" % n)
    if queixas:
        print()
        for q in queixas:
            print("  ERRO  · %s" % q)
        print("\n%d divergencia(s). Nada aqui se resolve em silencio." % len(queixas))
        return 1
    print("\nSem divergencia.")
    return 0


def escrever_vendor(texto, h):
    carimbo = (
        "# ===========================================================================\n"
        "# COPIA VENDORIZADA — NAO EDITAR AQUI (NORMAS.md N56)\n"
        "#\n"
        "#   origem : oficina/pandoc/perfis.yaml\n"
        "#   copiado: 2026-09-10\n"
        "#   sha-256 da origem: " + h + "\n"
        "#\n"
        "# O Gerador precisa deste arquivo ao lado dele para abrir servido de uma pasta\n"
        "# so. A verdade continua sendo a da Oficina. Achou defeito? Corrige la e roda\n"
        "#\n"
        "#   python oficina/pandoc/conferir_perfis.py --propagar\n"
        "#\n"
        "# Editar esta copia e o defeito do N56: o gerador_rolo.py bifurcou em 538\n"
        "# linhas sem que nada avisasse.\n"
        "# ===========================================================================\n\n")
    io.open(VENDOR, "w", encoding="utf-8", newline="\n").write(carimbo + texto)


def esc(v):
    return (str(v).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def escrever_tabela_no_body(dados):
    """Escreve os perfis no <body> do Gerador, como HTML de verdade.

    Por que no <body> e não por fetch: (1) LEI 2 — o que não está no <body>
    não existe para uma IA, um crawler ou um `curl`; (2) `fetch` de um arquivo
    ao lado é BLOQUEADO em `file://`, e a bancada tem de abrir por duplo
    clique como as outras. Gerar o bloco resolve os dois sem criar uma segunda
    verdade: a verdade continua sendo o perfis.yaml, e este HTML é derivado.
    """
    fontes = dados.get("fontes", {})
    linhas = [
        '<table id="dados-perfis">',
        '<caption class="mono">Gerado de oficina/pandoc/perfis.yaml em '
        + esc(dados.get("gerado_em", "?")) + ' — não editar aqui.</caption>',
        "<thead><tr><th>perfil</th><th>para</th><th>fonte</th><th>corpo</th>"
        "<th>entrelinha</th><th>entre letras</th><th>alinhamento</th>"
        "<th>hifeniza</th><th>títulos</th><th>abertura</th><th>cabeçalho</th>"
        "<th>adorno</th><th>notas</th><th>papel</th></tr></thead>",
        "<tbody>",
    ]
    for nome, p in dados.get("perfis", {}).items():
        f = fontes.get(p.get("fonte"), {})
        arquivos = f.get("arquivos") or []
        attrs = {
            "data-id": nome,
            "data-nome": p.get("nome", nome),
            "data-nome-comercial": p.get("nome_comercial", ""),
            "data-nome-clinico": p.get("nome_clinico", ""),
            "data-fonte": p.get("fonte", ""),
            "data-fonte-css": f.get("css", ""),
            "data-fonte-arquivos": "|".join(str(a) for a in arquivos),
            "data-largura-media-em": f.get("largura_media_em", ""),
            "data-largura-medida": "false" if f.get("largura_medida") is False else "true",
            "data-corpo-pt": p.get("corpo_pt", ""),
            "data-entrelinha-pt": p.get("entrelinha_pt", ""),
            "data-letra-em": p.get("letra_em", 0),
            "data-palavra-em": p.get("palavra_em", 0),
            "data-alinhamento": p.get("alinhamento", ""),
            "data-alinhamento-titulo": p.get("alinhamento_titulo", "esquerda"),
            "data-hifenizacao": "true" if p.get("hifenizacao") else "false",
            "data-abertura": p.get("abertura_de_capitulo", "pagina-nova"),
            "data-cabecalho": p.get("cabecalho", "nenhum"),
            "data-adorno": p.get("adorno", "nenhum"),
            "data-notas": p.get("notas", ""),
            "data-notas-corpo": p.get("notas_corpo", "igual"),
            # Campos do perfil ABNT. Vazio quer dizer "como sempre foi": o
            # Gerador so usa o que estiver escrito, e nenhum perfil antigo
            # muda de aparencia por causa deles.
            "data-notas-corpo-pt": p.get("notas_corpo_pt", ""),
            "data-recuo-mm": p.get("recuo_primeira_linha_mm", ""),
            "data-titulos-corpo-pt": p.get("titulos_corpo_pt", ""),
            "data-citacao-recuo-mm": p.get("citacao_recuo_mm", ""),
            "data-citacao-corpo-pt": p.get("citacao_corpo_pt", ""),
            "data-citacao-entrelinha-pt": p.get("citacao_entrelinha_pt", ""),
            "data-folio": p.get("folio", "pe-centro"),
            "data-papel": p.get("papel", ""),
            "data-papel-cor": p.get("papel_cor", ""),
        }
        abertura = "<tr " + " ".join(
            '%s="%s"' % (k, esc(v)) for k, v in attrs.items()) + ">"
        razao = ""
        try:
            razao = " (%.3fx)" % (float(p["entrelinha_pt"]) / float(p["corpo_pt"]))
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            pass
        celulas = [
            "<b>%s</b>" % esc(p.get("nome", nome)),
            esc(p.get("para", "")),
            esc(p.get("fonte", "")),
            "%s pt" % esc(p.get("corpo_pt", "")),
            "%s pt%s" % (esc(p.get("entrelinha_pt", "")), esc(razao)),
            ("%s em" % esc(p.get("letra_em"))) if p.get("letra_em") else "—",
            esc(p.get("alinhamento", "")),
            "sim" if p.get("hifenizacao") else "não",
            esc(p.get("alinhamento_titulo", "esquerda")),
            esc(p.get("abertura_de_capitulo", "pagina-nova")),
            esc(p.get("cabecalho", "nenhum")),
            esc(p.get("adorno", "nenhum")),
            esc(p.get("notas", "")),
            esc(p.get("papel", "")),
        ]
        linhas.append(abertura + "".join("<td>%s</td>" % c for c in celulas) + "</tr>")
    linhas += ["</tbody>", "</table>"]
    bloco = "\n  ".join(linhas)

    alvo = io.open(GRADE, encoding="utf-8").read()
    i = alvo.find(MARCA_INICIO)
    j = alvo.find(MARCA_FIM)
    if i < 0 or j < 0:
        raise SystemExit(
            "nao achei os marcadores PERFIS:INICIO / PERFIS:FIM em %s.\n"
            "Sem eles nao ha onde escrever, e escrever no lugar errado seria "
            "pior que nao escrever." % GRADE)
    novo = (alvo[:i + len(MARCA_INICIO)] + "\n  " + bloco + "\n  " + alvo[j:])
    io.open(GRADE, "w", encoding="utf-8", newline="\n").write(novo)
    return len(dados.get("perfis", {}))


def escrever_lista_na_oficina(dados):
    """A lista curta que a Oficina precisa: id, nome, para quem, fonte e corpo.

    Ela escolhe o perfil e exporta a especificacao; o Gerador compoe com ele.
    Sem esta lista, ou a Oficina teria os perfis escritos a mao (segunda
    verdade, N56) ou o perfil sairia adivinhado por fonte e corpo."""
    linhas = ['<ul id="dados-perfis-oficina">']
    for nome, p in dados.get("perfis", {}).items():
        attrs = {
            "data-id": nome,
            "data-nome": p.get("nome", nome),
            "data-para": p.get("para", ""),
            "data-fonte": p.get("fonte", ""),
            "data-corpo": p.get("corpo_pt", ""),
            # A Oficina estima linhas por pagina, e para isso precisa da
            # entrelinha REAL do perfil. Sem ela, estimava por uma constante
            # de classe (1,35 serifada) e errava 28 por cento no ABNT, que
            # compoe a 1,725.
            "data-entrelinha": p.get("entrelinha_pt", ""),
        }
        linhas.append(
            "<li " + " ".join('%s="%s"' % (k, esc(v)) for k, v in attrs.items()) + ">"
            + "<b>%s</b> <span class=\"mono\">· %s · %s %s pt</span></li>"
            % (esc(p.get("nome", nome)), esc(p.get("para", "")),
               esc(p.get("fonte", "")), esc(p.get("corpo_pt", ""))))
    linhas.append("</ul>")
    bloco = "\n  ".join(linhas)

    alvo = io.open(VITRINE, encoding="utf-8").read()
    i = alvo.find(MARCA_OF_INICIO)
    j = alvo.find(MARCA_OF_FIM)
    if i < 0 or j < 0:
        raise SystemExit(
            "nao achei os marcadores PERFIS-OFICINA:INICIO / :FIM em %s." % VITRINE)
    novo = alvo[:i + len(MARCA_OF_INICIO)] + "\n  " + bloco + "\n  " + alvo[j:]
    io.open(VITRINE, "w", encoding="utf-8", newline="\n").write(novo)
    return len(dados.get("perfis", {}))


if __name__ == "__main__":
    sys.exit(main())
