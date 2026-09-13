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
REM Se o app ja foi instalado pelo Edge ("Instalar este site como aplicativo"),
REM abre o APP: janela propria e o icone proprio na barra de tarefas. O Edge
REM guarda cada app instalado numa pasta _crx__<app-id>, com o icone batizado
REM pelo nome do manifesto - e do nome dessa pasta que sai o app-id. Ainda nao
REM instalado: abre no navegador, como sempre. (O ? no nome casa a letra
REM acentuada; este arquivo e ASCII de proposito.)
set "APPDIR="
for /d %%D in ("%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Web Applications\_crx__*") do if exist "%%D\Oficina.ico" set "APPDIR=%%~nxD"
if not defined APPDIR goto navegador
start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge_proxy.exe" --profile-directory=Default --app-id=%APPDIR:~6%
exit

:navegador
start "" "http://localhost:4184/"
exit
