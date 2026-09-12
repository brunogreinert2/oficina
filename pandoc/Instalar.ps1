<#
    Instalar.ps1
    Cria a pasta de configuração do Pandoc, copia os arquivos deste diretório
    para os lugares certos, corrige o caminho absoluto do preâmbulo e testa.

    Uso (a partir desta pasta):
        powershell -ExecutionPolicy Bypass -File .\Instalar.ps1
#>

$ErrorActionPreference = 'Stop'

# --- 1. Pandoc está instalado? ------------------------------------------------
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "Pandoc nao encontrado no PATH." -ForegroundColor Red
    Write-Host "Instale com:  winget install --id JohnMacFarlane.Pandoc" -ForegroundColor Yellow
    exit 1
}

$versao = (pandoc --version | Select-Object -First 1)
Write-Host "Encontrado: $versao" -ForegroundColor Green

# --- 2. Descobrir a pasta de configuração REAL --------------------------------
# O proprio pandoc informa. Nao chute o caminho: pode mudar conforme a instalacao.
# A linha pode vir como "User data directory:" ou "Default user data directory:",
# e em algumas versoes lista dois caminhos separados por " or ". Pegamos o primeiro.
$linha = pandoc --version | Select-String -Pattern 'user data directory:'
if ($linha) {
    $userDir = ($linha.Line -replace '(?i).*user data directory:\s*', '').Trim()
    $userDir = ($userDir -split '\s+or\s+')[0].Trim()
} else {
    $userDir = Join-Path $env:APPDATA 'pandoc'
}
if ([string]::IsNullOrWhiteSpace($userDir)) { $userDir = Join-Path $env:APPDATA 'pandoc' }
Write-Host "Pasta de configuracao: $userDir"

$defaultsDir = Join-Path $userDir 'defaults'

# --- 3. Criar as pastas (o Pandoc nao cria sozinho) ---------------------------
foreach ($d in @($userDir, $defaultsDir)) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Force -Path $d | Out-Null
        Write-Host "  criada: $d" -ForegroundColor Cyan
    } else {
        Write-Host "  ja existia: $d" -ForegroundColor DarkGray
    }
}

# --- 4. Copiar os arquivos ----------------------------------------------------
$aqui = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

$perfis = @('academico.yaml','academico-neohellenic.yaml','caderno.yaml',
            'caderno-frente.yaml','caderno-presbiopia.yaml',
            'caderno-baixa-visao.yaml','caderno-astigmatismo.yaml','caderno-dislexia.yaml',
            'abnt.yaml')
foreach ($p in $perfis) { Copy-Item (Join-Path $aqui $p) $defaultsDir -Force }
foreach ($t in @('preambulo-grego.tex','preambulo-simbolos.tex','preambulo-grego-cardo.tex',
                 'preambulo-abnt.tex')) {
    Copy-Item (Join-Path $aqui $t) $userDir -Force
}
Write-Host "Arquivos copiados." -ForegroundColor Green

# --- 5. Corrigir os caminhos absolutos dentro de TODOS os defaults ------------
# Os YAML apontam para os preambulos; o caminho precisa ser o REAL desta maquina.
foreach ($p in $perfis) {
    $alvo = Join-Path $defaultsDir $p
    $t = Get-Content $alvo -Raw -Encoding UTF8
    foreach ($tex in @('preambulo-grego.tex','preambulo-simbolos.tex',
                       'preambulo-grego-cardo.tex','preambulo-abnt.tex')) {
        $novo = (Join-Path $userDir $tex) -replace '\\', '/'
        $t = $t -replace "(?m)^\s*-\s*`"[^`"]*$([regex]::Escape($tex))`"", "  - `"$novo`""
    }
    Set-Content $alvo -Value $t -Encoding UTF8
}
Write-Host "Caminhos dos preambulos ajustados para: $userDir" -ForegroundColor Cyan

# --- 6. Teste de fumaça -------------------------------------------------------
Write-Host ""
Write-Host "Testando com grego politonico..." -ForegroundColor Yellow
$sonda = Join-Path $env:TEMP 'sonda-grego.md'
@"
# Teste

Politonico: thaumazein em grego -- to $([char]0x03B8)$([char]0x03B1)$([char]0x1F50)$([char]0x03BC)$([char]0x03AC)$([char]0x03B6)$([char]0x03B5)$([char]0x03B9)$([char]0x03BD)

Politonico 2: $([char]0x1F41) $([char]0x03B3)$([char]0x1F70)$([char]0x03C1) $([char]0x03BC)$([char]0x1FE6)$([char]0x03B8)$([char]0x03BF)$([char]0x03C2)

Portugues: acao, coracao, imas, agua, e, a, u, o -- $([char]0x00E3)$([char]0x00E7)$([char]0x00E9)$([char]0x00F4)$([char]0x00FC)
"@ | Set-Content $sonda -Encoding UTF8

$pdf = Join-Path $env:TEMP 'sonda-grego.pdf'
$saida = & pandoc $sonda -d academico -o $pdf 2>&1
$perdidos = $saida | Select-String 'Missing character'

if ($perdidos) {
    Write-Host "ATENCAO: glifos faltando na fonte atual." -ForegroundColor Red
    $perdidos | Select-Object -First 5 | ForEach-Object { Write-Host "  $_" }
    Write-Host "Rode Testar-Fontes.ps1 e troque 'mainfont' em $defaultsDir\academico.yaml" -ForegroundColor Yellow
} elseif (Test-Path $pdf) {
    Write-Host "PDF gerado sem perder nenhum glifo: $pdf" -ForegroundColor Green
} else {
    Write-Host "Falhou. Saida do pandoc:" -ForegroundColor Red
    $saida | Select-Object -First 15 | ForEach-Object { Write-Host "  $_" }
}

Write-Host ""
Write-Host "Pronto. Perfis disponiveis:" -ForegroundColor Green
Write-Host "    -d academico          leitura na tela / impressao avulsa" -ForegroundColor White
Write-Host "    -d caderno            imprimir FRENTE E VERSO e costurar" -ForegroundColor White
Write-Host "    -d caderno-frente     imprimir SO NA FRENTE e costurar" -ForegroundColor White
Write-Host "    -d caderno-presbiopia vista cansada: corpo 12, mais ar entre linhas" -ForegroundColor White
Write-Host "    -d caderno-baixa-visao   corpo 17, entrelinha ampla, SO FRENTE" -ForegroundColor White
Write-Host "    -d caderno-astigmatismo  letras descoladas, Atkinson Hyperlegible" -ForegroundColor White
Write-Host "    -d caderno-dislexia      OpenDyslexic, letras e linhas amplas" -ForegroundColor White
Write-Host "    -d academico-neohellenic grego em GFS NeoHellenic" -ForegroundColor White
Write-Host "    -d abnt                  trabalho academico NBR 14724" -ForegroundColor White
Write-Host ""
Write-Host "    pandoc arquivo.md -d caderno-presbiopia -o arquivo.pdf" -ForegroundColor Cyan
Write-Host ""
Write-Host "Novo-Caderno.ps1 existe para combinacoes fora dos perfis - opcional." -ForegroundColor DarkGray
