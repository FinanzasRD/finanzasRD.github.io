# GUÍA DE OPTIMIZACIÓN GOOGLE ADSENSE - FinanzasRD

## ESTADO ACTUAL
- Cuenta AdSense: ca-pub-5540590524171765 (YA configurada)
- 4 slots de anuncio en index.html (Hero bottom, after calculators, before blog, after blog)
- 1 slot en artículos de blog (after article content)

## MAPA DE CALOR PARA UBICACIÓN DE ANUNCIOS

### PÁGINA PRINCIPAL (index.html)
```
┌─────────────────────────────────┐
│         HEADER (fijo)           │
├─────────────────────────────────┤
│                                 │
│         HERO SECTION            │
│                                 │
├─────────────────────────────────┤
│   📍 ANUNCIO #1 (after hero)    │ ← ALTA prioridad (visibilidad máxima)
│      Display horizontal         │
├─────────────────────────────────┤
│                                 │
│     CONVERSOR DE DIVISAS        │
│                                 │
├─────────────────────────────────┤
│                                 │
│     CALCULADORAS (grid)         │
│                                 │
├─────────────────────────────────┤
│   📍 ANUNCIO #2 (after calc)    │ ← ALTA prioridad
│      Display horizontal         │
├─────────────────────────────────┤
│                                 │
│     COMPARADOR COOPERATIVAS     │
│                                 │
├─────────────────────────────────┤
│   📍 ANUNCIO #3 (before blog)   │ ← MEDIA prioridad
├─────────────────────────────────┤
│                                 │
│     BLOG (grid de artículos)    │
│                                 │
├─────────────────────────────────┤
│   📍 ANUNCIO #4 (after blog)    │ ← MEDIA prioridad
├─────────────────────────────────┤
│                                 │
│        CONTACTO / FOOTER        │
└─────────────────────────────────┘
```

### ARTÍCULO DE BLOG
```
┌─────────────────────────────────┐
│         HEADER (fijo)           │
├─────────────────────────────────┤
│    Breadcrumb + Título          │
├─────────────────────────────────┤
│    ✦ Contenido del artículo     │
│    ✦ Párrafo 1-2                │
├─────────────────────────────────┤
│   📍 ANUNCIO IN-ARTICLE         │ ← ALTA prioridad (mayor CTR)
│      (después del 3er párrafo)  │
├─────────────────────────────────┤
│    ✦ Resto del contenido        │
│    ✦ Conclusión                 │
├─────────────────────────────────┤
│    Artículos relacionados       │
├─────────────────────────────────┤
│   📍 ANUNCIO #2 (after related) │ ← MEDIA prioridad
├─────────────────────────────────┤
│         FOOTER                  │
└─────────────────────────────────┘
```

### FORMATOS RECOMENDADOS

| Ubicación | Formato | Tamaño | Nota |
|-----------|---------|--------|------|
| Hero bottom | Display | Responsive (auto) | Usar full-width-responsive |
| After calculadoras | Display | Responsive (auto) | Above the fold en mobile |
| In-article | In-article | Fluido | Mejor CTR |
| After related | Display | 728x90 o responsive | Buen complemento |
| Sidebar (desktop) | Display | 300x250 | Solo si hay sidebar |

### CONFIGURACIÓN RECOMENDADA POR SLOT

**ANUNCIO #1 (Hero Bottom)**
```
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5540590524171765"
     data-ad-slot="SLOT_ID_1"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
```

**ANUNCIO #2 (In-Article)**
```
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-client="ca-pub-5540590524171765"
     data-ad-slot="SLOT_ID_2"
     data-ad-format="fluid"></ins>
```

## ERRORES EVITAR PARA APROBACIÓN

### ❌ NO HACER:
1. Anuncios en modales o popups
2. Más de 3 anuncios visibles al mismo tiempo
3. Anuncios cerca de elementos de navegación (botones, menús)
4. Anuncios que cubran contenido
5. Colocar anuncios en páginas con poco contenido
6. Anuncios en páginas de error (404)
7. Pedir clics explícita o implícitamente
8. Contenido duplicado
9. Imágenes sin derechos de uso
10. Enlaces rotos o páginas vacías

### ✅ SÍ HACER:
1. Contenido original y de valor (mínimo 500 palabras por artículo)
2. Páginas de privacidad completas (✓ ya creadas)
3. Páginas de términos y condiciones (✓ ya creadas)
4. About Us / Contacto visibles (✓ creados)
5. Diseño responsive profesional (✓ optimizado)
6. Velocidad de carga rápida (✓ Core Web Vitals optimizado)
7. Navegación clara e intuitiva
8. SSL/HTTPS (GitHub Pages lo provee)
9. Contenido actualizado regularmente
10. Política de cookies (✓ cookie consent implementado)

## ESTRATEGIA PARA AUMENTAR RPM

### RPM (Revenue Per 1000 Impressions)
- **Nicho financiero:** RPM típico $15-50 (alto comparado con otros nichos)
- **Tráfico de RD:** RPM estimado $3-8 (menor que US, pero estable)
- **Meta:** Alcanzar $5-10 RPM con tráfico orgánico

### TÁCTICAS PARA SUBIR RPM:
1. **Tráfico orgánico de calidad** → mayor RPM
2. **Contenido evergreen** → tráfico constante
3. **Keywords de alto CPC** (seguros, préstamos, tarjetas) → mayor pago por clic
4. **Artículos de comparativa** ("Mejores X en RD") → alto engagement
5. **Anuncios nativos** → mejor UX, mayor CTR
6. **Evitar tráfico de baja calidad** (redes sociales sin segmentar)
7. **Actualizar contenido viejo** → Google premia con mejor posición

## PROCESO DE APROBACIÓN

### Checklist pre-aprobación:
- [ ] Política de privacidad completa ✓
- [ ] Términos y condiciones ✓
- [ ] Página de contacto funcional ✓
- [ ] Diseño responsive ✓
- [ ] Contenido original (mínimo 20-30 artículos) ✓ (11 actuales + plan)
- [ ] Sin contenido prohibido (préstamos ilegales, etc.)
- [ ] Navegación clara ✓
- [ ] Sin errores técnicos ✓
- [ ] Velocidad de carga aceptable ✓
- [ ] About Us / información del sitio ✓

### Tiempo estimado de aprobación:
- **Primera solicitud:** 1-4 semanas
- **Rechazos comunes:** Contenido insuficiente, páginas de privacidad incompletas, diseño pobre
- **Si rechazan:** Revisar motivo exacto, corregir, y volver a solicitar
