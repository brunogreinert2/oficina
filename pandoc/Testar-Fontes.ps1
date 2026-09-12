<#
    Testar-Fontes.ps1
    Lista as fontes instaladas que cobrem, ao mesmo tempo:
      - acentos do português  (ã ç é ô ü)
      - grego básico          (φ λ ω)
      - grego politônico      (ᾶ ῥ ἐ ὕ ῶ)  ← é aqui que quase toda fonte falha

    Uso:  powershell -ExecutionPolicy Bypass -File .\Testar-Fontes.ps1
#>

Add-Type -AssemblyName PresentationCore

# Caracteres-sonda, tirados dos textos reais da disciplina
$sondas = @{
    'Português'   = [char[]]'ãçéôüáà'
    'GregoBasico' = [char[]]'φλωμκσπ'
    'Politonico'  = [char[]]([string][char]0x1FF6 + [char]0x1FE5 + [char]0x1F10 + [char]0x1F55 + [char]0x1F76)
    'Extras'      = [char[]]([string][char]0x2081 + [char]0x27E8 + [char]0x2192)  # subscrito, angular, seta
}

$resultados = foreach ($fam in [Windows.Media.Fonts]::SystemFontFamilies) {
    $tf = $null
    foreach ($t in $fam.GetTypefaces()) {
        $gt = $null
        if ($t.TryGetGlyphTypeface([ref]$gt)) { $tf = $gt; break }
    }
    if (-not $tf) { continue }

    $linha = [ordered]@{ Fonte = $fam.Source }
    foreach ($k in 'Português','GregoBasico','Politonico','Extras') {
        $faltam = @($sondas[$k] | Where-Object { -not $tf.CharacterToGlyphMap.ContainsKey([int]$_) })
        $linha[$k] = if ($faltam.Count -eq 0) { 'ok' } else { "faltam $($faltam.Count)" }
    }
    [pscustomobject]$linha
}

Write-Host ""
Write-Host "=== FONTES COMPLETAS (servem para os textos da disciplina) ===" -ForegroundColor Green
$completas = $resultados | Where-Object { $_.Português -eq 'ok' -and $_.GregoBasico -eq 'ok' -and $_.Politonico -eq 'ok' }
$completas | Sort-Object Fonte | Format-Table -AutoSize

if ($completas.Count -eq 0) {
    Write-Host "Nenhuma fonte instalada cobre grego politonico." -ForegroundColor Red
    Write-Host "Baixe Libertinus Serif: https://github.com/alerque/libertinus/releases" -ForegroundColor Yellow
} else {
    Write-Host "Use qualquer uma acima em 'mainfont' no academico.yaml." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== SO GREGO BASICO (quebram no politonico - cuidado) ===" -ForegroundColor Yellow
$resultados |
    Where-Object { $_.GregoBasico -eq 'ok' -and $_.Politonico -ne 'ok' } |
    Sort-Object Fonte | Format-Table -AutoSize

# --- fontes de acessibilidade -------------------------------------------------
Write-Host ""
Write-Host "=== FONTES DE ACESSIBILIDADE ===" -ForegroundColor Green
$acessiveis = 'Cardo','Atkinson Hyperlegible','Atkinson Hyperlegible Next','OpenDyslexic','Segoe UI Symbol'
foreach ($nome in $acessiveis) {
    $achou = $resultados | Where-Object { $_.Fonte -like "$nome*" } | Select-Object -First 1
    if (-not $achou) {
        Write-Host ("  {0,-28} NAO INSTALADA" -f $nome) -ForegroundColor DarkGray
    } else {
        $cor = if ($achou.Politonico -eq 'ok') { 'Green' } else { 'Yellow' }
        $obs = if ($achou.Politonico -eq 'ok') { 'cobre grego - pode ser fonte principal' }
               else { 'SEM grego - precisa do preambulo-grego-cardo.tex' }
        Write-Host ("  {0,-28} PT:{1,-10} politonico:{2,-10} {3}" -f `
            $achou.Fonte, $achou.Português, $achou.Politonico, $obs) -ForegroundColor $cor
    }
}
Write-Host ""
Write-Host "Fontes de acessibilidade sem grego funcionam: o Novo-Caderno.ps1 carrega" -ForegroundColor DarkGray
Write-Host "o preambulo-grego-cardo.tex, que poe a Cardo so nos trechos gregos." -ForegroundColor DarkGray
