# -*- coding: utf-8 -*-
"""
conferir.py — a conferencia rapida da Oficina, antes de recarregar a aba.

A Oficina foi a ultima bancada a ganhar isto, e pagou por nao ter: em
2026-09-11, duas vezes na mesma tarde, um `<script>` dela parou de compilar e o
sintoma foi o de sempre — a pagina abre inteira, bonita, com as secoes VAZIAS,
porque o script nao chegou a rodar. Parece problema de dado. Nao e.

Nove conferencias, e cada uma nasceu de um defeito real:

1. `node --check` em cada bloco <script>.
2. Abertura de comentario HTML dentro de <script>: muda o estado do
   tokenizador e o navegador engole o resto da pagina, sem erro no console.
3. O catalogo do <body> (LEI 2): ids unicos, campos obrigatorios por lista.
4. A costura japonesa declara quantos FUROS tem. Furar e irreversivel.
5. As fracoes dos canones sao as que a documentacao promete (nonos = 1/9).
6. O CONTRATO com o Gerador: tudo o que o `deEspecificacao()` de la EXIGE tem
   de ser escrito pelo `especificacaoParaGerador()` daqui. Os dois lados do
   contrato moram em arquivos diferentes, e e assim que um contrato quebra.
7. O CONTRATO DA VOLTA: o `retornoParaOficina()` de la escreve e o
   `receberRetorno()` daqui le. Nenhum dos dois estoura quando um campo some —
   a bancada cairia de volta na estimativa em silencio.
8. Vocabulario morto: a ficha dizia "LuaTeX" e "pdfbook2" num fluxo que nunca
   existiu. Ficha que descreve um fluxo inexistente e pior que ficha nenhuma.
9. As duas bancadas contam CAPITULO igual, medido arquivo por arquivo
   (`../conferir_capitulos.py`). Em 2026-09-12 nao contavam: a Oficina dizia
   "1 capitulos" no Encheiridion e o Gerador "2 de 2 capitulos", sobre o mesmo
   .md. Dois numeros na tela para a mesma coisa e o que o N56 proibe.

    python conferir.py
"""
import io
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(AQUI, "index.html")
GERADOR = os.path.normpath(os.path.join(AQUI, "..", "gerador", "index.html"))

t = io.open(ALVO, encoding="utf-8").read()
falhas = []
notas = []

# --- 1 e 2. os blocos <script> ---------------------------------------------
blocos = re.findall(r"<script>(.*?)</script>", t, re.S)
tmp = os.path.join(AQUI, "_conferir.tmp.js")
for n, b in enumerate(blocos):
    io.open(tmp, "w", encoding="utf-8").write(b)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode:
        falhas.append("bloco <script> %d nao compila:\n%s" % (n + 1, r.stderr.strip()))
    k = b.find("<!--")
    if k >= 0:
        linha = t[:t.index(b)].count("\n") + b[:k].count("\n") + 1
        falhas.append(
            "bloco <script> %d tem abertura de comentario HTML literal na linha "
            "%d. O navegador engole o resto da pagina sem erro no console. "
            "Escreva \\x3C!--" % (n + 1, linha))
if os.path.exists(tmp):
    os.remove(tmp)

# --- 3. o catalogo do <body> (LEI 2) ---------------------------------------
LISTAS = {
    "dados-textos": ["autor", "palavras"],
    "dados-fontes": ["classe", "css", "larg"],
    "dados-formatos": ["l", "a", "prop"],
    "dados-encad": ["fam", "dif"],
    "dados-canones": ["tipo", "frase"],
    "dados-impressao": ["espelha"],
    "dados-colunas": ["n"],
    "dados-temas": ["fundo", "texto"],
    "dados-capas": ["dif"],
    "dados-fios": ["cor"],
    "dados-estoque": ["uso"],
    "dados-aberturas": [],
}


def itens(id_lista):
    m = re.search(r'<ul id="%s">(.*?)</ul>' % id_lista, t, re.S)
    if not m:
        return None
    return re.findall(r"<li ([^>]*)>", m.group(1))


def atributos(bruto):
    # Aspas duplas OU simples: `data-css='"Cardo", serif'` e escrito com
    # simples porque o valor tem aspas duplas dentro. A primeira versao desta
    # conferencia so olhava as duplas e acusou quatro fontes de nao ter css.
    pares = re.findall(r'data-([a-z-]+)="([^"]*)"', bruto)
    pares += re.findall(r"data-([a-z-]+)='([^']*)'", bruto)
    return dict(pares)


for lista, obrigatorios in LISTAS.items():
    linhas = itens(lista)
    if linhas is None:
        falhas.append("a lista <ul id=\"%s\"> sumiu do <body>. O catalogo e o "
                      "dado (LEI 2); sem ela a bancada abre vazia." % lista)
        continue
    vistos = set()
    for bruto in linhas:
        d = atributos(bruto)
        ident = d.get("id")
        if not ident:
            falhas.append("%s: item sem data-id." % lista)
            continue
        if ident in vistos:
            falhas.append("%s: id repetido '%s'. Id e eterno (LEI 6) e unico."
                          % (lista, ident))
        vistos.add(ident)
        for campo in obrigatorios:
            if campo not in d:
                falhas.append("%s/%s: falta data-%s." % (lista, ident, campo))

# --- 3b. o estoque: um item por uso, e papel com gramatura ----------------
# E daqui que o colofao do Gerador tira papel, linha e peso. Dois papeis de
# miolo sem menu para escolher fariam a exportacao levar o primeiro em
# silencio — o livro sairia com a ficha de outro papel.
USOS = ("miolo", "capa", "linha", "cera")
por_uso = {}
for bruto in (itens("dados-estoque") or []):
    d = atributos(bruto)
    uso = d.get("uso")
    if uso not in USOS:
        falhas.append("dados-estoque/%s: uso '%s' desconhecido (conheco: %s)."
                      % (d.get("id"), uso, ", ".join(USOS)))
        continue
    por_uso.setdefault(uso, []).append(d.get("id"))
    if uso in ("miolo", "capa"):
        try:
            ok = float(d.get("gram", "")) > 0
        except ValueError:
            ok = False
        if not ok:
            falhas.append("dados-estoque/%s: papel sem data-gram. O peso que o "
                          "colofao publica sai dela." % d.get("id"))
for uso, ids in sorted(por_uso.items()):
    if len(ids) > 1:
        falhas.append("dados-estoque: %d itens de uso '%s' (%s). A Oficina ainda "
                      "nao tem menu para escolher, e exportaria o primeiro em "
                      "silencio." % (len(ids), uso, ", ".join(ids)))

# --- 3c. a abertura de capitulo e lista FECHADA nas duas bancadas ---------
# A Oficina exporta o valor e o Gerador compoe por ele. Um id a mais de um lado
# so viraria uma especificacao que a outra bancada nao entende — e o sintoma
# seria um livro com outro numero de paginas, sem erro nenhum na tela.
aberturas_aqui = set()
for bruto in (itens("dados-aberturas") or []):
    aberturas_aqui.add(atributos(bruto).get("id"))
if os.path.exists(GERADOR):
    g_txt = io.open(GERADOR, encoding="utf-8").read()
    m_sel = re.search(r'<select id="sel-abertura">(.*?)</select>', g_txt, re.S)
    if not m_sel:
        notas.append("nao achei o menu de abertura no Gerador; lista nao conferida.")
    else:
        la = set(v for v in re.findall(r'<option value="([^"]*)"', m_sel.group(1)) if v)
        if la != aberturas_aqui:
            falhas.append(
                "abertura de capitulo: a Oficina conhece %s e o Gerador %s. A "
                "lista e FECHADA: a Oficina exporta o valor e o Gerador compoe "
                "por ele." % (sorted(aberturas_aqui), sorted(la)))

# --- 4. a costura japonesa declara os furos --------------------------------
for bruto in (itens("dados-encad") or []):
    d = atributos(bruto)
    if d.get("fam") == "jap":
        furos = d.get("furos")
        if not furos or not furos.isdigit() or int(furos) < 2:
            falhas.append(
                "encadernacao '%s' e japonesa e nao declara data-furos. O "
                "desenho, a lista de corte e o calculo do fio saem desse "
                "numero, e furar papel nao tem conserto." % d.get("id"))

# --- 5. os canones sao o que a documentacao promete ------------------------
ESPERADO = {
    "nonos":    {"int": 1 / 9.0,  "ext": 2 / 9.0,  "sup": 1 / 9.0,  "inf": 2 / 9.0},
    "compacta": {"int": 1 / 12.0, "ext": 1 / 9.0,  "sup": 1 / 12.0, "inf": 1 / 9.0},
}
for bruto in (itens("dados-canones") or []):
    d = atributos(bruto)
    alvo = ESPERADO.get(d.get("id"))
    if not alvo:
        continue
    for campo, valor in alvo.items():
        try:
            tem = float(d.get(campo, "nan"))
        except ValueError:
            tem = float("nan")
        if abs(tem - valor) > 0.0005:
            falhas.append(
                "canone '%s': data-%s vale %s e devia valer %.6f. A margem "
                "sai daqui, e o Gerador nao recalcula nada."
                % (d.get("id"), campo, d.get(campo), valor))

# --- 6. o contrato com o Gerador -------------------------------------------
# O `deEspecificacao()` do Gerador exige campos com `g(obj, 'campo')`, que
# ESTOURA quando falta. Ler de la o que e exigido e conferir que a exportacao
# daqui escreve — em vez de descobrir no dia em que alguem arrasta o arquivo.
if not os.path.exists(GERADOR):
    notas.append("nao achei o gerador/index.html para conferir o contrato.")
else:
    g = io.open(GERADOR, encoding="utf-8").read()
    m = re.search(r"function deEspecificacao\(j\)\{(.*?)\n\}", g, re.S)
    if not m:
        notas.append("nao achei deEspecificacao() no Gerador; contrato nao conferido.")
    else:
        corpo = m.group(1)
        exigidos = set(re.findall(r"g\(j\.([a-z_]+), '([a-z_]+)'\)", corpo))
        m2 = re.search(r"function especificacaoParaGerador\(c\)\{(.*?)\n\}", t, re.S)
        if not m2:
            falhas.append("nao achei especificacaoParaGerador() na Oficina.")
        else:
            exporta = m2.group(1)
            for grupo, campo in sorted(exigidos):
                if not re.search(r"\b%s\s*:" % re.escape(campo), exporta):
                    falhas.append(
                        "o Gerador EXIGE `%s.%s` e a exportacao daqui nao "
                        "escreve esse campo. Arrastar o arquivo la vai falhar "
                        "com 'falta o campo %s'." % (grupo, campo, campo))

# --- 7. o contrato da VOLTA -------------------------------------------------
# O `retornoParaOficina()` do Gerador escreve; o `receberRetorno()` daqui le.
# Nenhum dos dois estoura quando um campo some: a Oficina leria `undefined`,
# cairia de volta na estimativa e nao diria nada — e o que atravessa esta ponte
# nao e numero de tela, e folha de papel cortada.
if os.path.exists(GERADOR):
    g = io.open(GERADOR, encoding="utf-8").read()
    mr = re.search(r"function retornoParaOficina\(\)\{(.*?)\n\}", g, re.S)
    ml = re.search(r"function receberRetorno\(nomeArquivo, texto\)\{(.*?)\n\}", t, re.S)
    if not mr or not ml:
        notas.append("nao achei os dois lados da volta; contrato de retorno "
                     "nao conferido.")
    else:
        escreve, le = mr.group(1), ml.group(1)
        # O que a Oficina LE de dentro do `j` — e que portanto o Gerador tem
        # de escrever.
        lidos = set(re.findall(r"j\.paginas\.([a-z_]+)", le)) | \
                set(re.findall(r"j\.obra && j\.obra\.([a-z_]+)", le)) | \
                set(re.findall(r"j\.([a-z_]+) \|\| ", le))
        for campo in sorted(lidos):
            if not re.search(r"\b%s\s*:" % re.escape(campo), escreve):
                falhas.append(
                    "a Oficina le `%s` do retorno e o Gerador nao escreve esse "
                    "campo. O numero cairia para a estimativa em silencio."
                    % campo)
        # A ASSINATURA e o que decide se o retorno vale. Os dois lados a montam
        # separadamente: se as ordens divergirem, TODO retorno passa a ser
        # recusado como velho, e ninguem entende por que.
        ma = re.search(r"function assinaturaDoCaso\(caso, perfil\)\{(.*?)\n\}", g, re.S)
        mb = re.search(r"function assinaturaDaqui\(tx, f, cn, imp, col\)\{(.*?)\n\}", t, re.S)
        if not ma or not mb:
            notas.append("nao achei as duas assinaturas; validade do retorno "
                         "nao conferida.")
        else:
            def pecas(corpo):
                dentro = re.search(r"\[(.*?)\]\.join", corpo, re.S)
                if not dentro:
                    return None
                return [p.strip() for p in dentro.group(1).split(",")]
            pa, pb = pecas(ma.group(1)), pecas(mb.group(1))
            if pa is None or pb is None:
                notas.append("as assinaturas mudaram de forma; conferir a mao.")
            elif len(pa) != len(pb):
                falhas.append(
                    "as assinaturas tem tamanhos diferentes (%d no Gerador, %d "
                    "na Oficina): todo retorno seria recusado como velho."
                    % (len(pa), len(pb)))
            for i, (a, b) in enumerate(zip(pa or [], pb or [])):
                # Nomes de variavel sao de cada lado; o que tem de bater e a
                # ORDEM dos conceitos, e isso so se le. O checador cobra que
                # cada peca continue falando do mesmo assunto.
                assunto = ("obra", "formato", "canone", "impressao", "perfil",
                           "colunas")
                if i < len(assunto) and assunto[i] not in (a + b).lower():
                    falhas.append(
                        "a peca %d da assinatura devia ser %s e virou `%s` / "
                        "`%s`. Assinaturas fora de ordem recusam todo retorno."
                        % (i + 1, assunto[i], a, b))

# --- 8. vocabulario morto ---------------------------------------------------
for morto, porque in (
    ("LuaTeX", "quem compoe e o Gerador (Paged.js); LuaTeX nunca entrou"),
    ("pdfbook2", "quem impoe e o impor.py"),
):
    if morto in t:
        falhas.append("a pagina ainda diz '%s' — %s." % (morto, porque))

# --- 9. capitulo se conta igual nas duas bancadas ---------------------------
# O conferidor mora na RAIZ, ao lado do `conferir_paleta.py`, porque a regra
# nao e de nenhuma das duas: ela e a mesma nas duas, e um conferidor por
# bancada seria o defeito outra vez, agora nos conferidores. Os dois
# `conferir.py` chamam este mesmo arquivo.
CONFERIDOR_CAP = os.path.normpath(os.path.join(AQUI, "..", "conferir_capitulos.py"))
if not os.path.exists(CONFERIDOR_CAP):
    falhas.append(
        "nao achei o %s. Sem ele, nada impede a Oficina e o Gerador de voltarem "
        "a dizer numeros de capitulo diferentes para o mesmo .md (N56)."
        % CONFERIDOR_CAP)
else:
    # `encoding` e `PYTHONIOENCODING` explicitos: o filho escreve «», · e — e o
    # Windows entrega o cp1252 do console para um cano.
    amb = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, CONFERIDOR_CAP], capture_output=True,
                       text=True, encoding="utf-8", env=amb)
    if r.returncode:
        falhas.append("a contagem de CAPITULO divergiu do Gerador:\n%s"
                      % (r.stdout or r.stderr or "").strip())
    else:
        notas.append((r.stdout or "").strip())

# --- veredito ---------------------------------------------------------------
for n in notas:
    print("  nota  · %s" % n)
if falhas:
    for f in falhas:
        print("ERRO  · %s" % f)
    print("\n%d problema(s). Nada aqui se resolve em silencio." % len(falhas))
    sys.exit(1)
print("oficina/index.html: %d blocos <script> compilam, catalogo integro, "
      "furos declarados, canones conferidos, contrato com o Gerador de pe "
      "nas duas maos."
      % len(blocos))
