$baseUrl = "https://finanzasrd.github.io"

# --- 1. Blog articles ---
Get-ChildItem "C:\Users\winde\Desktop\finanzasrd\blog\*.html" | Where-Object { $_.Name -ne "template.html" } | ForEach-Object {
    $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8
    $slug = $_.Name

    if ($content -match 'rel="canonical"') {
        $current = if ($content -match 'rel="canonical"\s*href="([^"]+)"') { $matches[1] }
        $expected = "$baseUrl/blog/$slug"
        if ($current -ne $expected) {
            $content = $content -replace 'rel="canonical"\s*href="([^"]+)"', "rel=`"canonical`" href=`"$expected`""
            Set-Content -Path $_.FullName -Value $content -Encoding UTF8
            Write-Host "  FIXED canonical: $slug (was $current)"
        } else {
            Write-Host "  OK: $slug"
        }
    } else {
        $canonical = "  <link rel=`"canonical`" href=`"$baseUrl/blog/$slug`">"
        $content = $content -replace '(</title>)', "`${1}`n$canonical"
        Set-Content -Path $_.FullName -Value $content -Encoding UTF8
        Write-Host "  ADDED canonical: $slug"
    }
}

# --- 2. Root pages ---
$rootPages = @("about.html", "privacidad.html", "terminos.html", "cookies.html", "descargo.html", "nuestra-metodologia.html", "index.html")
foreach ($page in $rootPages) {
    $path = "C:\Users\winde\Desktop\finanzasrd\$page"
    if (-not (Test-Path $path)) { continue }
    $content = Get-Content -Path $path -Raw -Encoding UTF8
    $slug = if ($page -eq "index.html") { "" } else { $page }
    $expected = "$baseUrl/$slug"

    if ($content -match 'rel="canonical"') {
        $current = if ($content -match 'rel="canonical"\s*href="([^"]+)"') { $matches[1] }
        if ($current -ne $expected) {
            $content = $content -replace 'rel="canonical"\s*href="([^"]+)"', "rel=`"canonical`" href=`"$expected`""
            Set-Content -Path $path -Value $content -Encoding UTF8
            Write-Host "  FIXED canonical: $page (was $current)"
        } else {
            Write-Host "  OK: $page"
        }
    } else {
        $canonical = "  <link rel=`"canonical`" href=`"$expected`">"
        $content = $content -replace '(</title>)', "`${1}`n$canonical"
        Set-Content -Path $path -Value $content -Encoding UTF8
        Write-Host "  ADDED canonical: $page"
    }
}

# --- 3. Author pages ---
Get-ChildItem "C:\Users\winde\Desktop\finanzasrd\autores\*.html" | ForEach-Object {
    $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8
    $slug = "autores/$($_.Name)"
    $expected = "$baseUrl/$slug"

    if ($content -match 'rel="canonical"') {
        $current = if ($content -match 'rel="canonical"\s*href="([^"]+)"') { $matches[1] }
        if ($current -ne $expected) {
            $content = $content -replace 'rel="canonical"\s*href="([^"]+)"', "rel=`"canonical`" href=`"$expected`""
            Set-Content -Path $_.FullName -Value $content -Encoding UTF8
            Write-Host "  FIXED canonical: $($_.Name) (was $current)"
        } else {
            Write-Host "  OK: $($_.Name)"
        }
    } else {
        $canonical = "  <link rel=`"canonical`" href=`"$expected`">"
        $content = $content -replace '(</title>)', "`${1}`n$canonical"
        Set-Content -Path $_.FullName -Value $content -Encoding UTF8
        Write-Host "  ADDED canonical: $($_.Name)"
    }
}

Write-Host "`nDone!"
