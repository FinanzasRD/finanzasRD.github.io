$blogDir = "C:\Users\winde\Desktop\finanzasrd\blog"
$exclude = @("template.html", "como-ahorrar-en-rd.html")

Get-ChildItem -Path $blogDir -Filter "*.html" | ForEach-Object {
    if ($_.Name -in $exclude) { return }
    
    $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8
    $changed = $false
    
    # 1. Replace old meta paragraph with new meta bar
    $pattern = '(?s)(<h1>.*?</h1>)\s*<p class="meta">.*?</p>'
    $replacement = '${1}' + "`n`n      <div class=`"article-meta-bar`">`n        <span>Por <strong><a href=`"../autores/carlos-mendez.html`" style=`"color:var(--primary-dark)`">Carlos Miguel Echavarr' + "i" + 'a Rodr' + "i" + 'guez</a></strong></span>`n        <span class=`"dot`">' + [char]0x2022 + '</span>`n        <span>Publicado: <strong>1 de junio de 2026</strong></span>`n        <span class=`"dot`">' + [char]0x2022 + '</span>`n        <span>Actualizado: <strong>1 de junio de 2026</strong></span>`n        <span class=`"dot`">' + [char]0x2022 + '</span>`n        <span>8 min de lectura</span>`n      </div>'
    
    if ($content -match $pattern) {
        $content = $content -replace $pattern, $replacement
        $changed = $true
        Write-Host "  Updated meta bar in $($_.Name)"
    }
    
    # 2. Check if sources block exists, if not add it before related-posts
    if ($content -notmatch "Fuentes consultadas") {
        $sourcesBlock = @"
      <div class="article-sources">
        <h3>Fuentes consultadas</h3>
        <ul>
          <li><a href="https://www.bancentral.gov.do" target="_blank" rel="noopener noreferrer">Banco Central de la Rep$([char]0xFA)blica Dominicana</a> — Tasas de inter$([char]0xE9)s de referencia y pol$([char]0xED)tica monetaria</li>
          <li><a href="https://www.sib.gob.do" target="_blank" rel="noopener noreferrer">Superintendencia de Bancos de la RD</a> — Indicadores financieros y tasas de entidades bancarias</li>
          <li><a href="https://www.banreservas.com.do" target="_blank" rel="noopener noreferrer">Banreservas</a> — Tasas de cuentas de ahorro y certificados financieros</li>
          <li><a href="https://www.popularenlinea.com" target="_blank" rel="noopener noreferrer">Banco Popular Dominicano</a> — Informaci$([char]0xF3)n de productos financieros</li>
          <li><a href="https://www.bhd.com.do" target="_blank" rel="noopener noreferrer">BHD</a> — Tasas de certificados financieros y cuentas</li>
        </ul>
        <span class="sources-note">Las fuentes se consultaron por $([char]0xFA)ltima vez en junio 2026. Las tasas y condiciones pueden haber cambiado. Verifica siempre con la entidad correspondiente.</span>
      </div>

"@
        $relatedPattern = '(<section class="related-posts">)'
        if ($content -match $relatedPattern) {
            $content = $content -replace $relatedPattern, "$sourcesBlock`$1"
            $changed = $true
            Write-Host "  Added sources block to $($_.Name)"
        }
    }
    
    # 3. Update author bio to new format if old format exists
    $oldAuthorPattern = '(?s)<a href="\.\./autores/carlos-mendez\.html" class="author-bio"[^>]*>.*?Ver perfil completo.*?</a>'
    $newAuthorBio = @"
<a href="../autores/carlos-mendez.html" class="author-bio" style="display:flex;text-decoration:none;cursor:pointer;gap:1rem;align-items:start;background:var(--primary-light);border-radius:var(--radius-sm);padding:1.25rem;margin:2rem 0;border:1px solid rgba(10,92,54,0.12)">
          <div class="author-bio__avatar" style="font-size:2.5rem;flex-shrink:0;width:56px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:50%;overflow:hidden;background:var(--white)">
            <img src="../images/author-carlos.jpg" alt="" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='none';this.parentElement.textContent='$([char]0xD83D)$([char]0xDC68)$([char]0x200D)$([char]0xD83D)$([char]0xDCBC)'">
          </div>
          <div class="author-bio__info" style="flex:1">
            <strong style="display:block;color:var(--dark);font-size:.95rem">Carlos Miguel Echavarr$([char]0xED)a Rodr$([char]0xED)guez</strong>
            <span style="display:block;color:var(--primary-dark);font-size:.8rem;font-weight:600;margin-bottom:.5rem">Fundador & Editor Principal de FinanzasRD</span>
            <p style="font-size:.85rem;color:var(--text-light);margin:0;line-height:1.6">Ingeniero en Sistemas Computacionales (UTESA) apasionado por la educaci$([char]0xF3)n financiera. Creador de FinanzasRD. Combino mi formaci$([char]0xF3)n tecnol$([char]0xF3)gica con el an$([char]0xE1)lisis financiero para ayudarte a tomar mejores decisiones con tu dinero.</p>
          </div>
          <span style="color:var(--primary-dark);font-weight:600;font-size:.8rem;white-space:nowrap;align-self:center">Ver perfil →</span>
        </a>
"@
    if ($content -match $oldAuthorPattern) {
        $content = $content -replace $oldAuthorPattern, $newAuthorBio
        $changed = $true
        Write-Host "  Updated author bio in $($_.Name)"
    }
    
    # 4. Fix encoding issues
    $content = $content -replace 'Art' + [char]0xEF + [char]0xBF + 'culos', 'Art' + [char]0xED + 'culos'
    $content = $content -replace 'pr' + [char]0xEF + [char]0xBF + 'stamos', 'pr' + [char]0xE9 + 'stamos'
    
    if ($changed) {
        Set-Content -Path $_.FullName -Value $content -Encoding UTF8
        Write-Host "  SAVED: $($_.Name)"
    } else {
        Write-Host "  No changes for $($_.Name)"
    }
}

Write-Host "`nDone!"
