#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter um arquivo Markdown (HANDBOOK.md) em HTML responsivo para leitura em tablets e dispositivos móveis.

Funcionalidades:
- Converte o arquivo HANDBOOK.md em HANDBOOK.html usando Pandoc.
- Corrige os links âncora do sumário para garantir compatibilidade.
- Insere CSS responsivo e meta viewport no HTML final.

Autor: Christian Vladimir Uhdre Mulato
Data: 20/06/2025
Licença: MIT
"""
import subprocess
import re

# Caminhos dos arquivos
md_file = "HANDBOOK.md"
html_file = "HANDBOOK.html"

# CSS responsivo para leitura em tablet
css_content = """
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0 1em;
    background: #f9f9f9;
    color: #222;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}
h1, h2, h3, h4 {
    color: #2b579a;
}
a {
    color: #0078d4;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
@media (max-width: 900px) {
    body {
        padding: 0 0.5em;
        font-size: 1.05em;
    }
    h1 { font-size: 2em; }
    h2 { font-size: 1.5em; }
}
"""

# 1. Converter o Markdown em HTML usando Pandoc
subprocess.run([
    "pandoc", md_file, "-o", html_file, "--standalone"
], check=True)

# 2. Ler o HTML gerado
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# 3. Corrigir âncoras do sumário (remover acentos, espaços, etc.)
def normalize_anchor(text):
    import unicodedata
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-zA-Z0-9\-]', '', text)
    return text.lower()

def fix_toc_anchors(html):
    def repl(match):
        label = match.group(2)
        anchor = normalize_anchor(label)
        return f'{match.group(1)}#{anchor}{match.group(3)}'
    return re.sub(r'(<a href=")#([^"]+)(">)', repl, html)

html = fix_toc_anchors(html)

# 4. Inserir o CSS responsivo e a meta viewport antes do </head>
meta_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
style_block = f"{meta_viewport}<style>\n{css_content}\n</style>\n"

if "<head>" in html:
    html = html.replace("<head>", f"<head>\n{style_block}", 1)
else:
    html = html.replace("<body>", f"<head>\n{style_block}</head>\n<body>", 1)

# 5. Salvar o HTML final
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Arquivo HTML gerado com CSS responsivo: {html_file}")