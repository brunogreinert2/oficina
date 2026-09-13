@echo off
REM ---------------------------------------------------------------------------
REM  Oficina - Pedra Angular
REM
REM  Duplo clique aqui. Sobe o servidor local e abre o Oficina no navegador.
REM  Para PARAR: feche a janela preta chamada "Servidor do Oficina".
REM
REM  Porta 4184. A porta e a identidade do app instalado: trocar a porta
REM  e trocar de app (o Edge ve outro endereco e perde o que estava salvo).
REM  Tabela das portas: 4181 Conversor, 4182 Corretor, 4183 Gerador,
REM  4184 Oficina, 4185 Portico, 4186 Laboratorio de Cores.
REM  A pagina continua abrindo por duplo clique no index.html, sem servidor;
REM  o servidor so e preciso para instalar e abrir como app.
REM  Nada sai do computador: o servidor so fala com esta maquina.
REM ---------------------------------------------------------------------------

cd /d "%~dp0"
start "Servidor do Oficina" /min cmd /c python servir.py 4184
timeout /t 2 /nobreak >nul
start "" "http://localhost:4184/"
exit
