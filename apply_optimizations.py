import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(ROOT, 'index.html')

MOJIBAKE_MAP = {
    'Ã¡': 'á',
    'Ã§Ã£': 'çã',
    'Ã§Ãµ': 'çõ',
    'Ã§': 'ç',
    'Ã£': 'ã',
    'Ãµ': 'õ',
    'Ã©': 'é',
    'Ã­': 'í',  # í
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã¢': 'â',
    'Ãª': 'ê',
    'Ã´': 'ô',
    'Ã€': 'À',
    'Ã ': 'à',
    'Ã\xad': 'í',
    'Ã\x81': 'Á',
    'Ã\x89': 'É',
    'Ã\x8d': 'Í',
    'Ã\x93': 'Ó',
    'Ã\x9a': 'Ú',
    'Ã\x87': 'Ç',
    'Ã\x83': 'Ã',
    'Ã\x95': 'Õ',
}

CUSTOM_CSS = """
<style id="ia-custom-fixes">
/* Smooth Navigation */
html { scroll-behavior: smooth; }

/* Base Responsiveness & UX */
* { box-sizing: border-box; }
img { max-width: 100%; height: auto; }

/* Focus Accessibility */
:focus { outline: 3px solid #0c4da2; outline-offset: 2px; }

/* Skip Link CSS */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #0c4da2;
    color: white;
    padding: 8px;
    z-index: 100000;
    transition: top 0.3s;
}
.skip-link:focus {
    top: 0;
}

/* UX Hover Effects */
a, button { transition: all 0.3s ease; }
a:hover { opacity: 0.8; }

/* Mobile Optimization */
@media (max-width: 768px) {
    .elementor-container { padding: 15px !important; }
    .elementor-column { width: 100% !important; }
}
</style>
"""

SKIP_LINK_HTML = '<a href="#content" class="skip-link">Pular para o conteúdo</a>\n'

def apply_mojibake_fixes(html):
    count = 0
    for bad, good in MOJIBAKE_MAP.items():
        if bad in html:
            c = html.count(bad)
            html = html.replace(bad, good)
            count += c
    return html, count

def inject_css(html):
    if '<style id="ia-custom-fixes">' in html:
        return html, False
    
    # Inject before </head>
    idx = html.find('</head>')
    if idx != -1:
        return html[:idx] + CUSTOM_CSS + html[idx:], True
    return html, False

def inject_skip_link(html):
    if 'class="skip-link"' in html:
        return html, False
    
    # Find <body>
    match = re.search(r'<body[^>]*>', html)
    if match:
        end_idx = match.end()
        # Ensure we have an element with id="content" somewhere
        # The script will try to add id="content" to the first elementor-section or similar
        html = html[:end_idx] + '\n' + SKIP_LINK_HTML + html[end_idx:]
        
        if 'id="content"' not in html:
            # Let's add it to the first data-element_type="section"
            section_match = re.search(r'<section\s+class="[^"]*elementor-section[^>]*>', html)
            if section_match:
                s = section_match.group(0)
                new_s = s.replace('<section ', '<section id="content" ')
                html = html.replace(s, new_s, 1)
            else:
                # Add a div right after skip link
                html = html.replace(SKIP_LINK_HTML, SKIP_LINK_HTML + '<div id="content"></div>')
        return html, True
    return html, False

def process_images(html):
    img_pattern = re.compile(r'<img\s+[^>]*>', re.IGNORECASE)
    def repl_img(m):
        tag = m.group(0)
        # Add alt="" if missing
        if 'alt=' not in tag:
            tag = tag.replace('<img ', '<img alt="" ')
        # Add loading="lazy" if missing
        if 'loading=' not in tag and 'data-lazy-src' not in tag:
            tag = tag.replace('<img ', '<img loading="lazy" ')
        return tag
    
    new_html = img_pattern.sub(repl_img, html)
    changed = (new_html != html)
    return new_html, changed

def fix_links(html):
    # Fix relative ../ links that are broken, making them absolute
    # Also if the user asked to convert relative navigation links to anchors, let's target typical hrefs.
    
    # We will convert generic broken WP relative links starting with `../`
    new_html = re.sub(r'href="\.\./([^"]*)"', r'href="https://iaadvocaciaempresarial.com.br/\1"', html)
    
    changed = (new_html != html)
    return new_html, changed

def process_file():
    with open(FILE_PATH, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html
    
    html, c_moji = apply_mojibake_fixes(html)
    html, c_css = inject_css(html)
    html, c_skip = inject_skip_link(html)
    html, c_img = process_images(html)
    html, c_links = fix_links(html)

    if html != original:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Optimization Summary:")
        print(f" - Mojibake instances fixed: {c_moji}")
        print(f" - CSS injected: {c_css}")
        print(f" - Skip link and ID content injected: {c_skip}")
        print(f" - Images processed (alt/lazy): {c_img}")
        print(f" - Links fixed: {c_links}")
        print("Success: index.html has been updated.")
    else:
        print("No changes needed. File is already optimized.")

if __name__ == '__main__':
    process_file()
