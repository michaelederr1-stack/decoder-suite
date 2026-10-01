with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Navigation Tab Bar CSS & Structure
nav_css = """
<style>
  /* Flash-inspired Sleek Top Navigation Bar */
  .nav-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    border-bottom: 2px solid rgba(0, 242, 254, 0.2);
    padding-bottom: 10px;
    overflow-x: auto;
  }

  .nav-btn {
    background: rgba(16, 22, 36, 0.6) !important;
    color: #8a99ad !important;
    border: 1px solid rgba(0, 242, 254, 0.1) !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 20px !important;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
  }

  .nav-btn:hover {
    color: #ffffff !important;
    background: rgba(0, 242, 254, 0.1) !important;
    transform: translateY(-2px);
  }

  .nav-btn.active {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
    color: #050b14 !important;
    border-color: #00f2fe !important;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
  }

  /* Page Views Management */
  .tab-page {
    display: none;
    animation: fadeIn 0.3s ease-in-out;
  }

  .tab-page.active {
    display: block;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
"""

# Inject CSS before </head>
if '</head>' in html and 'nav-tabs' not in html:
    html = html.replace('</head>', nav_css + '\n</head>')

# 2. Navigation HTML Bar Template
nav_html = """
<div class="nav-tabs">
  <button class="nav-btn active" onclick="switchPage('page-decoder', this)">⚡ Traversal & Decoder</button>
  <button class="nav-btn" onclick="switchPage('page-geo', this)">🛰️ Tactical Triangulation</button>
  <button class="nav-btn" onclick="switchPage('page-blocks', this)">🔤 Cipher & Blocks</button>
</div>
"""

# Insert Nav Bar above main panels if not present
if 'switchPage(' not in html:
    if '<div class="panel' in html:
        html = html.replace('<div class="panel', nav_html + '\n<div class="panel', 1)

# 3. JavaScript Page Switching Functionality
nav_js = """
    function switchPage(pageId, btnElement) {
      // Hide all pages
      document.querySelectorAll('.tab-page').forEach(page => page.classList.remove('active'));
      
      // Deactivate all buttons
      document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));

      // Activate selected page and button
      const selectedPage = document.getElementById(pageId);
      if (selectedPage) selectedPage.classList.add('active');
      if (btnElement) btnElement.classList.add('active');

      // Refresh map sizing if navigating to Geo page
      if (pageId === 'page-geo' && typeof map !== 'undefined' && map) {
        setTimeout(() => {
          if (map.invalidateSize) map.invalidateSize(); // For Leaflet
          if (google && google.maps) google.maps.event.trigger(map, 'resize'); // For Google Maps
        }, 100);
      }
    }
"""

if 'function switchPage(' not in html:
    html = html.replace('</script>', nav_js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Navigation structure and page switching engine added!")
