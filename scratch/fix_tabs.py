with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS Fix for Active Tab Highlighting & Responsive Wrapping
tab_css_fix = """
<style>
  .nav-tabs {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    margin-bottom: 20px !important;
    border-bottom: 2px solid rgba(0, 242, 254, 0.3) !important;
    padding-bottom: 12px !important;
  }

  .nav-btn {
    background: rgba(16, 22, 36, 0.7) !important;
    color: #8a99ad !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.2s ease-in-out !important;
  }

  .nav-btn:hover {
    color: #ffffff !important;
    background: rgba(0, 242, 254, 0.15) !important;
    border-color: #00f2fe !important;
  }

  .nav-btn.active {
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
    color: #050b14 !important;
    border-color: #00f2fe !important;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
  }

  .tab-page {
    display: none;
  }

  .tab-page.active {
    display: block !important;
  }
</style>
"""

# JavaScript Page Switcher Logic
tab_js_fix = """
    function switchPage(pageId, btnElement) {
      // 1. Hide all tab pages
      document.querySelectorAll('.tab-page').forEach(page => {
        page.classList.remove('active');
        page.style.display = 'none';
      });

      // 2. Deactivate all navigation buttons
      document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
      });

      // 3. Activate selected tab page & button
      const targetPage = document.getElementById(pageId);
      if (targetPage) {
        targetPage.classList.add('active');
        targetPage.style.display = 'block';
      }

      if (btnElement) {
        btnElement.classList.add('active');
      }

      // 4. Force map refresh if switching to Geo tab
      if (pageId === 'page-geo') {
        setTimeout(() => {
          if (typeof map !== 'undefined' && map) {
            if (map.invalidateSize) map.invalidateSize();
            if (window.google && google.maps) google.maps.event.trigger(map, 'resize');
          }
        }, 150);
      }
    }

    // Ensure default page is active on load
    document.addEventListener("DOMContentLoaded", function() {
      const firstBtn = document.querySelector('.nav-btn');
      if (firstBtn) {
        firstBtn.click();
      }
    });
"""

if '</head>' in html:
    html = html.replace('</head>', tab_css_fix + '\n</head>')

if 'function switchPage(' in html:
    import re
    html = re.sub(r'function switchPage\(.*?\n    \}', tab_js_fix, html, flags=re.DOTALL)
else:
    html = html.replace('</script>', tab_js_fix + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Navigation buttons and page switching logic fixed!")
