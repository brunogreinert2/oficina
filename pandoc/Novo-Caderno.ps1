<#
    Novo-Caderno.ps1
    Monta um PDF de caderno sob medida, perguntando o que a pessoa precisa.

    Uso:
        .\Novo-Caderno.ps1 caminho\do\arquivo.md
        .\Novo-Caderno.ps1            (pergunta o arquivo)

    Existe porque no papel não há zoom: o corpo escolhido é definitivo.
    Vale gerar, imprimir UMA folha de teste e só então imprimir o caderno.
#>

param([string]$Arquivo)

$ErrorActionPreference = 'Stop'

function Escolher($titulo, $ajuda, $opcoes, $padrao) {
    Write-Host ""
    Write-Host $titulo -ForegroundColor Cyan
    if ($ajuda) { Write-Host "  $ajuda" -ForegroundColor DarkGray }
    for ($i = 0; $i -lt $opcoes.Count; $i++) {
        $marca = if ($i -eq $padrao) { "*" } else { " " }
        Write-Host ("  [{0}]{1} {2}" -f ($i+1), $marca, $opcoes[$i].Rotulo)
        if ($opcoes[$i].Nota) { Write-Host ("       {0}" -f $opcoes[$i].Nota) -ForegroundColor DarkGray }
    }
    $r = Read-Host "  Numero (Enter = padrao marcado com *)"
    if ([string]::IsNullOrWhiteSpace($r)) { return $opcoes[$padrao] }
    $n = 0
    if ([int]::TryParse($r, [ref]$n) -and $n -ge 1 -and $n -le $opcoes.Count) { return $opcoes[$n-1] }
    Write-Host "  Valor invalido, usando o padrao." -ForegroundColor Yellow
    return $opcoes[$padrao]
}

# --- arquivo de entrada -------------------------------------------------------
if (-not $Arquivo) { $Arquivo = Read-Host "Caminho do arquivo .md" }
$Arquivo = $Arquivo.Trim('"')
if (-not (Test-Path $Arquivo)) { Write-Host "Arquivo nao encontrado: $Arquivo" -ForegroundColor Red; exit 1 }
$item = Get-Item $Arquivo

Write-Host ""
Write-Host "=== Novo caderno: $($item.Name) ===" -ForegroundColor Green
Write-Host "No papel nao ha zoom. Imprima uma folha de teste antes do caderno inteiro." -ForegroundColor DarkGray

# --- receita por necessidade --------------------------------------------------
$receitas = @(
    @{ Rotulo="Leitura comum";  Nota="O padrao. Corpo 11, entrelinha 1.2.";                    Corpo=11; Linha=1.2;  Letra=0;   Fonte="Cardo" }
    @{ Rotulo="Vista cansada";  Nota="Presbiopia. Um degrau de corpo e mais ar entre linhas."; Corpo=12; Linha=1.35; Letra=0;   Fonte="Cardo" }
    @{ Rotulo="Baixa visao";    Nota="Corpo grande e entrelinha ampla. Considere so frente.";  Corpo=17; Linha=1.6;  Letra=0;   Fonte="Cardo" }
    @{ Rotulo="Astigmatismo";   Nota="Letras descoladas. Aumentar corpo ajuda menos.";          Corpo=12; Linha=1.35; Letra=2.0; Fonte="Atkinson Hyperlegible" }
    @{ Rotulo="Dislexia";       Nota="OpenDyslexic com letras e linhas afastadas.";             Corpo=12; Linha=1.6;  Letra=2.0; Fonte="OpenDyslexic" }
    @{ Rotulo="Personalizado";  Nota="Escolher cada ajuste separadamente.";                     Corpo=0;  Linha=0;    Letra=0;   Fonte="" }
)
$r = Escolher "Para quem e este caderno?" "Pontos de partida, nao prescricao. O certo e o que ficar confortavel." $receitas 0

$corpo = $r.Corpo; $linha = $r.Linha; $letra = $r.Letra; $fonte = $r.Fonte

if ($r.Rotulo -eq "Personalizado") {
    $o = Escolher "Corpo da letra" "Acima de 12 o caderno engorda rapido: 9 paginas viram 17 em 14pt e 35 em 20pt." @(
        @{Rotulo="11 pt - padrao"}, @{Rotulo="12 pt - um degrau"},
        @{Rotulo="14 pt"}, @{Rotulo="17 pt"}, @{Rotulo="20 pt - maximo"}) 0
    $corpo = @(11,12,14,17,20)[[array]::IndexOf(@("11 pt - padrao","12 pt - um degrau","14 pt","17 pt","20 pt - maximo"), $o.Rotulo)]

    $o = Escolher "Espaco entre linhas" "Ajuda quando a linha de cima parece cair sobre a de baixo." @(
        @{Rotulo="Normal"}, @{Rotulo="Ampla"}, @{Rotulo="Muito ampla"}) 0
    $linha = @{ "Normal"=1.2; "Ampla"=1.35; "Muito ampla"=1.6 }[$o.Rotulo]

    $o = Escolher "Espaco entre letras" "Descola as letras. Costuma ser o ajuste que mais muda no astigmatismo." @(
        @{Rotulo="Normal"}, @{Rotulo="Amplo"}, @{Rotulo="Muito amplo"}) 0
    $letra = @{ "Normal"=0.0; "Amplo"=1.5; "Muito amplo"=3.0 }[$o.Rotulo]

    $o = Escolher "Fonte" "Atkinson e OpenDyslexic NAO tem grego - a Cardo entra sozinha nos trechos gregos." @(
        @{Rotulo="Cardo"; Nota="Serifada classica. Cobre grego politonico."},
        @{Rotulo="Atkinson Hyperlegible"; Nota="Traco uniforme, letras bem diferentes entre si."},
        @{Rotulo="OpenDyslexic"; Nota="Base das letras mais pesada."}) 0
    $fonte = $o.Rotulo
}

$o = Escolher "Como vai imprimir?" "So frente elimina o fantasma do verso - importante na baixa visao." @(
    @{Rotulo="Frente e verso"; Nota="Metade das folhas. Margem de costura alterna sozinha."},
    @{Rotulo="So na frente";   Nota="Gasta o dobro de papel, mas nada transparece."}) 0
$duplex = ($o.Rotulo -eq "Frente e verso")

# --- montar o defaults temporario --------------------------------------------
$userDir = (pandoc --version | Select-String 'user data directory') -replace '(?i).*user data directory:\s*',''
$userDir = ($userDir -split '\s+or\s+')[0].Trim()
if ([string]::IsNullOrWhiteSpace($userDir)) { $userDir = Join-Path $env:APPDATA 'pandoc' }
$u = $userDir -replace '\\','/'

$headers = @("  - `"$u/preambulo-simbolos.tex`"")
if ($fonte -ne "Cardo") { $headers += "  - `"$u/preambulo-grego-cardo.tex`"" }

# article so aceita ate 12pt; acima disso o valor e ignorado em silencio
$classe = if ($corpo -gt 12) { "extarticle" } else { "article" }

$opts = @()
if ($fonte -eq "Cardo") {
    $opts += "    - `"BoldItalicFont={Cardo Bold}`""
    $opts += "    - `"BoldItalicFeatures={FakeSlant=0.2}`""
}
if ($letra -gt 0) { $opts += "    - `"LetterSpace=$letra`"" }

$geo = if ($duplex) { "a4paper,inner=32mm,outer=22mm,top=22mm,bottom=25mm,twoside" }
       else         { "a4paper,left=32mm,right=22mm,top=22mm,bottom=25mm" }

$yaml = @"
pdf-engine: xelatex
include-in-header:
$($headers -join "`n")
variables:
  documentclass: $classe
  mainfont: "$fonte"
$(if ($opts.Count) { "  mainfontoptions:`n" + ($opts -join "`n") })
  monofont: "Consolas"
  fontsize: ${corpo}pt
  linestretch: $linha
  geometry: "$geo"
$(if ($duplex) { "  classoption:`n    - twoside" })
  indent: false
  colorlinks: true
  linkcolor: black
  urlcolor: black
  lang: pt-BR
number-sections: false
"@

$tmp = Join-Path $env:TEMP "caderno-$([guid]::NewGuid().ToString('N').Substring(0,8)).yaml"
Set-Content -Path $tmp -Value $yaml -Encoding UTF8

# --- gerar --------------------------------------------------------------------
$saida = Join-Path $item.DirectoryName ($item.BaseName + ".pdf")
Write-Host ""
Write-Host "Gerando: $fonte, ${corpo}pt, entrelinha $linha, espaco entre letras $letra" -ForegroundColor Cyan
Write-Host "         $(if($duplex){'frente e verso'}else{'so na frente'}), classe $classe"

Push-Location $item.DirectoryName
$log = & pandoc $item.FullName -d $tmp -o $saida 2>&1
Pop-Location

$perdidos = $log | Select-String 'Missing character'
if ($perdidos) {
    Write-Host ""
    Write-Host "ATENCAO: caracteres perdidos - eles NAO estarao no PDF:" -ForegroundColor Red
    $perdidos | Select-Object -First 5 | ForEach-Object { Write-Host "  $_" }
} elseif (Test-Path $saida) {
    $n = (Get-Item $saida).Length
    Write-Host ""
    Write-Host "Pronto, sem perder nenhum caractere: $saida" -ForegroundColor Green
    Write-Host "  $([math]::Round($n/1KB)) KB" -ForegroundColor DarkGray
    Write-Host "  Imprima a pagina 1 e a 2 primeiro, e confira o tamanho no papel." -ForegroundColor Yellow
} else {
    Write-Host "Falhou:" -ForegroundColor Red
    $log | Select-Object -First 12 | ForEach-Object { Write-Host "  $_" }
}

Remove-Item $tmp -ErrorAction SilentlyContinue
