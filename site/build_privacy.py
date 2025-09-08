import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
md_path = ROOT / 'PRIVACY_POLICY.md'
out_dir = ROOT / 'site'
out_dir.mkdir(parents=True, exist_ok=True)
html_path = out_dir / 'privacy.html'

md = md_path.read_text(encoding='utf-8')

def render(md: str) -> str:
    lines = md.splitlines()
    html = []
    in_list = False
    for line in lines:
        if line.startswith('# '):
            if in_list:
                html.append('</ul>'); in_list = False
            html.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('## '):
            if in_list:
                html.append('</ul>'); in_list = False
            html.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('- '):
            if not in_list:
                html.append('<ul>'); in_list = True
            html.append(f'<li>{line[2:].strip()}</li>')
        elif not line.strip():
            if in_list:
                html.append('</ul>'); in_list = False
            html.append('<p></p>')
        else:
            if in_list:
                html.append('</ul>'); in_list = False
            html.append(f'<p>{line.strip()}</p>')
    if in_list:
        html.append('</ul>')
    body = '\n'.join(html)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Roaming Detector — Privacy Policy</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 2rem; line-height: 1.5; color: #111; }}
    h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.5rem; }}
    ul {{ padding-left: 1.2rem; }}
    footer {{ margin-top: 2rem; font-size: 0.9rem; color: #555; }}
  </style>
  <meta name="robots" content="noindex" />
  <meta name="theme-color" content="#ffffff" />
  <link rel="icon" href="data:," />
  <link rel="canonical" href="https://example.com/privacy/roaming-detector" />
  <meta property="og:title" content="Roaming Detector — Privacy Policy" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:description" content="Roaming Detector processes location on-device only and does not transmit your data." />
  <meta name="description" content="Roaming Detector processes location on-device only and does not transmit your data." />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
</head>
<body>
{body}
<footer>© {2025} Roaming Detector</footer>
</body>
</html>'''

html = render(md)
html_path.write_text(html, encoding='utf-8')
print(f'Wrote {html_path}')

