# Servidor local do Oficina. Copia do gerador/servir.py, so muda a porta.
#
# Por que não `python -m http.server` direto: ele manda o navegador guardar o
# arquivo em cache. Depois de uma alteração no index.html, atualizar a aba
# devolve a versão VELHA — e sem nenhum aviso. Perdemos tempo com isso no
# Corretor em 2026-08-23: a correção estava no disco, o navegador servia a
# anterior, e nem fechar o servidor resolvia, porque o cache é do navegador.
#
# A única diferença para o `http.server` padrão são os três cabeçalhos de
# no-cache abaixo. Nada sai do computador: só fala com esta máquina.
#
# Porta 4184. Tabela das portas no abrir_oficina.bat — todas podem ficar
# abertas ao mesmo tempo.

import http.server
import sys

PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 4184


class SemCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()


if __name__ == '__main__':
    with http.server.ThreadingHTTPServer(('127.0.0.1', PORTA), SemCache) as s:
        print('Oficina em http://localhost:%d/' % PORTA)
        print('Sem cache: atualizar a aba mostra sempre a versao do disco.')
        print('Para parar, feche esta janela.')
        s.serve_forever()
