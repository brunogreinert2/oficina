# -*- coding: utf-8 -*-
"""
medir_contraste.py — a Oficina medida pela regua do ecossistema.

NAO mede nada por conta propria: traduz os tokens `--ui-*` desta bancada para
os nomes que o `app-leitura/scripts/medir_contraste.py` espera e entrega o
trabalho a ele. Um segundo medidor seria uma segunda verdade sobre a mesma
cor — o defeito que o N56 descreve — e o dia em que a regua mudasse, uma das
duas ficaria para tras.

Mede cada tema DUAS vezes:
  · sobre o FUNDO da pagina (`--ui-fundo`);
  · sobre a SUPERFICIE dos cartoes (`--ui-superficie`), que e onde vive metade
    da interface — ficha de escolha, ficha tecnica, zona de arrastar. Medir so
    o fundo deixaria essa metade sem numero.

    python medir_contraste.py
    python medir_contraste.py --html contraste.html
"""
import argparse
import io
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(AQUI, "index.html")
REGUA = os.path.normpath(os.path.join(
    AQUI, "..", "app-leitura", "scripts", "medir_contraste.py"))

# De onde vem cada nome que a regua conhece. O que a Oficina nao tem (destaque
# de busca) fica de fora, e a regua simplesmente nao mede aquele par.
DE_PARA = {
    "color-text": "ui-texto",
    "color-muted": "ui-texto-suave",
    "color-accent": "ui-acento",
    "color-error": "ui-alerta",
    "color-borda-ui": "ui-linha",
    "color-border": "ui-linha",
}


def ler_temas(html):
    """Os blocos de tema do `<style>` da Oficina, na ordem em que estao."""
    temas = {}
    for m in re.finditer(r"(:root|\[data-theme=([a-z]+)\])\s*\{(.*?)\n\}", html, re.S):
        nome = "noite" if m.group(1) == ":root" else m.group(2)
        vars_ = dict(re.findall(r"--([a-z0-9-]+):\s*([^;]+);", m.group(3)))
        if "ui-fundo" not in vars_:
            continue
        temas.setdefault(nome, {}).update({k: v.strip() for k, v in vars_.items()})
    return temas


def css_traduzido(temas):
    """O CSS que a regua sabe ler, com os nomes dela."""
    blocos = []
    for nome, v in temas.items():
        for sufixo, fundo in (("", "ui-fundo"), (" sobre carta", "ui-superficie")):
            if fundo not in v:
                continue
            linhas = ["  --color-bg: %s;" % v[fundo]]
            for alvo, origem in DE_PARA.items():
                if origem in v:
                    linhas.append("  --%s: %s;" % (alvo, v[origem]))
            blocos.append("[data-theme='%s%s'] {\n%s\n}" % (nome, sufixo, "\n".join(linhas)))
    return "\n\n".join(blocos) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", help="caminho para gravar o relatorio em HTML")
    # Qualquer bancada do ecossistema: elas usam os mesmos tokens `--ui-*`, e a
    # pergunta "isto e defeito daqui ou da casa inteira?" so se responde
    # medindo as outras com a mesma regua.
    ap.add_argument("--bancada", help="outro index.html para medir")
    a = ap.parse_args()
    global ALVO
    if a.bancada:
        ALVO = os.path.abspath(a.bancada)

    if not os.path.exists(REGUA):
        raise SystemExit(
            "nao achei a regua do ecossistema em %s.\n"
            "Ela e quem mede; esta bancada so traduz os tokens. Se o "
            "app-leitura mudou de lugar, corrija o caminho aqui." % REGUA)

    temas = ler_temas(io.open(ALVO, encoding="utf-8").read())
    if not temas:
        raise SystemExit("nao achei bloco de tema nenhum no index.html.")

    tmp = os.path.join(tempfile.gettempdir(), "oficina-tokens.css")
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(css_traduzido(temas))

    cmd = [sys.executable, REGUA, "--css", tmp]
    if a.html:
        cmd += ["--html", os.path.abspath(a.html)]
    print("Oficina: %d temas, medidos sobre o fundo e sobre a superficie dos "
          "cartoes.\n" % len(temas))
    r = subprocess.run(cmd)
    os.remove(tmp)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
