with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

responsive_css = """
<style>
  /* Base Layout Constraints & Flex Box Scaling */
  html, body {
    width: 100%;
    min-height: 100vh;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  *, *:before, *:after {
    box-sizing: inherit;
  }

  /* Main Container Fluidity */
  .container, body > div {
    max-width: 1600px !important;
    width: 95% !important;
    margin: 0 auto !important;
    padding: 20px 10px !important;
  }

  /* Flexible Grid Layouts for Cards and Panels */
  .grid-encoders, .panel-grid, div[style*="display: flex"] {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)) !important;
    gap: 20px !important;
    width: 100% !important;
  }

  /* Prevent Panel Overflow */
  .panel, .encoder-card, .card {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow-x: auto !important; /* Allow internal scrolling if content exceeds card width */
    padding: 20px !important;
  }

  /* Scalable Form Controls */
  input, select, textarea, button {
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  textarea {
    width: 100% !important;
    min-height: 90px;
    resize: vertical;
  }

  /* Scalable & Scrollable Tables */
  .table-container, table {
    width: 100% !important;
    display: block !important;
    overflow-x: auto !important; /* Horizontal scrollbar on small screens instead of crushing content */
    white-space: nowrap;
  }

  th, td {
    padding: 12px 18px !important; /* Spaced out columns */
  }

  /* Media Query Adjustments for High-Res / Desktop Displays */
  @media (min-width: 1200px) {
    .full-width {
      grid-column: 1 / -1 !important;
    }
  }
</style>
"""

if '</head>' in html:
    html = html.replace('</head>', responsive_css + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Responsive grid layout and autoscaling styles applied!")
