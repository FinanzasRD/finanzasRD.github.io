$dirs = @(
  "C:\Users\winde\Desktop\finanzasrd\blog",
  "C:\Users\winde\Desktop\finanzasrd"
)
$files = @()
foreach ($d in $dirs) {
  Get-ChildItem -Path $d -Filter "*.html" | ForEach-Object { $files += $_ }
}

$correctIcon = "href=""data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💰</text></svg>"""
$brokenIconLine1 = "href=""data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
$brokenIconLine2 = "href=""data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💰</text></svg>""><text y='.9em' font-size='90'>💰</text></svg>"""

$newBio = @'
        <a href="../autores/carlos-mendez.html" class="author-bio" style="display:flex;text-decoration:none;cursor:pointer;gap:1rem;align-items:start;background:var(--primary-light);border-radius:var(--radius-sm);padding:1.25rem;margin:2rem 0;border:1px solid rgba(10,92,54,0.12)">
          <div class="author-bio__avatar" style="font-size:2.5rem;flex-shrink:0;width:56px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:50%;overflow:hidden;background:var(--white)">
            <img src="../images/author-carlos.jpg" alt="" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='none';this.parentElement.textContent='👨‍💼'">
          </div>
          <div class="author-bio__info" style="flex:1">
            <strong style="display:block;color:var(--dark);font-size:.95rem">Carlos Miguel Echavarría Rodríguez</strong>
            <span style="display:block;color:var(--primary-dark);font-size:.8rem;font-weight:600;margin-bottom:.5rem">Fundador & Editor Principal de FinanzasRD</span>
            <p style="font-size:.85rem;color:var(--text-light);margin:0;line-height:1.6">Ingeniero en Sistemas Computacionales (UTESA) apasionado por la educación financiera. Creador de FinanzasRD. Combino mi formación tecnológica con el análisis financiero para ayudarte a tomar mejores decisiones con tu dinero.</p>
          </div>
          <span style="color:var(--primary-dark);font-weight:600;font-size:.8rem;white-space:nowrap;align-self:center">Ver perfil →</span>
        </a>
'@

$total = 0
$fixedIcons = 0
$fixedBio = 0
$fixedEncoding = 0

foreach ($f in $files) {
  $name = $f.Name
  if ($name -eq "template.html") { continue }
  
  $c = Get-Content -Path $f.FullName -Raw -Encoding UTF8
  $changed = $false
  
  # 1. Fix broken icon links
  if ($c -match [regex]::Escape($brokenIconLine1)) {
    # Fix line 1: replace broken icon link
    $c = $c -replace [regex]::Escape($brokenIconLine1), $correctIcon
    $changed = $true
  }
  if ($c -match [regex]::Escape($brokenIconLine2)) {
    # Fix line 2: replace broken apple-touch-icon link
    $c = $c -replace [regex]::Escape($brokenIconLine2), $correctIcon
    $changed = $true
    $fixedIcons++
  }
  
  # 2. Update old author bio
  if ($c -match "Ver perfil completo") {
    # Replace old author bio block
    $oldBioPattern = '(?s)<a href="\.\./autores/carlos-mendez\.html" class="author-bio"[^>]*>.*?Ver perfil completo.*?</a>'
    if ($c -match $oldBioPattern) {
      $c = $c -replace $oldBioPattern, $newBio
      $changed = $true
      $fixedBio++
    }
  }
  
  # 3. Fix double accent encoding issues
  if ($c -match "úú") {
    $c = $c -replace "úú", "ú"
    $changed = $true
    $fixedEncoding++
  }
  
  if ($changed) {
    Set-Content -Path $f.FullName -Value $c -Encoding UTF8
    $total++
    Write-Host "  FIXED: $name"
  }
}

Write-Host "`nResumen:"
Write-Host "  Archivos modificados: $total"
Write-Host "  Iconos arreglados: $fixedIcons"
Write-Host "  Author bios actualizados: $fixedBio"
Write-Host "  Encoding arreglado: $fixedEncoding"
