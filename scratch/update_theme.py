with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS styling for Galaxy background, 3D card depth, and neat tables
theme_css = """
<style>
  /* Animated Galaxy Background */
  body {
    background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%) !important;
    color: #e0e6ed !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    margin: 0;
    overflow-x: hidden;
  }

  body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: 
      radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
      radial-gradient(2px 2px at 40px 70px, #00f2fe, rgba(0,0,0,0)),
      radial-gradient(1px 1px at 90px 40px, #fff, rgba(0,0,0,0)),
      radial-gradient(2px 2px at 160px 120px, #9b51e0, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    opacity: 0.3;
    z-index: -1;
    pointer-events: none;
  }

  /* 3D Glassmorphism Panel Effect */
  .panel, .encoder-card, .card {
    background: rgba(16, 22, 36, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 242, 254, 0.15) !important;
    border-radius: 12px !important;
    box-shadow: 
      0 10px 30px rgba(0, 0, 0, 0.5),
      inset 0 1px 1px rgba(255, 255, 255, 0.1),
      inset 0 -2px 5px rgba(0, 242, 254, 0.05) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }

  .panel:hover, .encoder-card:hover {
    transform: translateY(-3px) scale(1.002);
    box-shadow: 
      0 15px 35px rgba(0, 242, 254, 0.15),
      inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
  }

  /* Neat, Presentable Tables */
  table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 12px 0;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  th {
    background: rgba(0, 242, 254, 0.15) !important;
    color: #00f2fe !important;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 0.8px;
    padding: 12px 14px;
    text-align: left;
    border-bottom: 1px solid rgba(0, 242, 254, 0.2);
  }

  td {
    padding: 10px 14px;
    background: rgba(10, 15, 26, 0.4);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 0.9rem;
    color: #c0c9d6;
  }

  tr:last-child td {
    border-bottom: none;
  }

  tr:hover td {
    background: rgba(0, 242, 254, 0.05) !important;
  }

  /* Compact 3D Buttons */
  button {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
    color: #050b14 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3) !important;
    cursor: pointer;
    transition: all 0.2s ease !important;
  }

  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5) !important;
  }

  /* Fix cyan block button stretching */
  div[style*="background: var(--accent-color"], button[onclick="exportAllToCSV()"] {
    width: auto !important;
    display: inline-block !important;
  }
</style>
"""

# Inject CSS styles before </head>
if '</head>' in html:
    html = html.replace('</head>', theme_css + '\n</head>')

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Galaxy background, 3D card styling, and table formatting applied!")
