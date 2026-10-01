with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Export Button UI in the top header/controls section
export_btn = """
      <div style="margin-top: 15px; margin-bottom: 15px; display: flex; justify-content: flex-end;">
        <button onclick="exportAllToCSV()" style="background: var(--accent-color, #00f2fe); color: #000; font-weight: bold; padding: 10px 18px; border: none; border-radius: 6px; cursor: pointer; transition: opacity 0.2s;">
          📥 Export Full Analysis to CSV
        </button>
      </div>
"""

if 'exportAllToCSV' not in html:
    # Inject button right before the main container or first panel
    if '<div class="panel' in html:
        html = html.replace('<div class="panel', export_btn + '\n<div class="panel', 1)

# 2. Add full CSV extraction and download logic
export_js = """
    function exportAllToCSV() {
      const rows = [];
      rows.push(["Module / Section", "Parameter / Field", "Value / Result"]);

      // Helper to add sanitized rows
      const addRow = (module, field, val) => {
        let cleanVal = (val || '').toString().replace(/\\r?\\n/g, ' ').replace(/"/g, '""');
        rows.push([`"${module}"`, `"${field}"`, `"${cleanVal}"`]);
      };

      // 1. Text & Encoder/Decoder Outputs
      const rawInput = document.getElementById('blockInput')?.value || document.querySelector('textarea')?.value || '';
      addRow("Input Data", "Raw Text Input", rawInput);

      // Collect pre/code outputs across all panels
      document.querySelectorAll('.panel, .encoder-card').forEach((card, idx) => {
        const title = card.querySelector('h2, label')?.innerText || `Section ${idx + 1}`;
        card.querySelectorAll('pre, input, textarea').forEach(el => {
          if (el.id && el.id !== 'blockInput') {
            const val = el.value || el.innerText;
            if (val) addRow(title.trim(), el.id, val.trim());
          }
        });
      });

      // 2. Observer Coordinates & Triangulation Data
      const obs1Lat = document.getElementById('obs1_lat')?.value;
      const obs1Lon = document.getElementById('obs1_lon')?.value;
      const obs1Brng = document.getElementById('obs1_brng')?.value;
      if (obs1Lat) addRow("Geo-Triangulation", "Observer 1 (Lat, Lon, Bearing)", `${obs1Lat}, ${obs1Lon}, ${obs1Brng}°`);

      const obs2Lat = document.getElementById('obs2_lat')?.value;
      const obs2Lon = document.getElementById('obs2_lon')?.value;
      const obs2Brng = document.getElementById('obs2_brng')?.value;
      if (obs2Lat) addRow("Geo-Triangulation", "Observer 2 (Lat, Lon, Bearing)", `${obs2Lat}, ${obs2Lon}, ${obs2Brng}°`);

      const triOut = document.getElementById('triangulateOut')?.innerText;
      if (triOut) addRow("Geo-Triangulation", "Target Coordinates", triOut);

      // 3. Cipher Blocks Output
      const blockOut = document.getElementById('blockOutput')?.innerText;
      const blockStats = document.getElementById('blockStats')?.innerText;
      if (blockOut) addRow("Cipher Grouping", "Grouped Text", blockOut);
      if (blockStats) addRow("Cipher Grouping", "Block Statistics", blockStats);

      // Build CSV String
      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\\n");
      const encodedUri = encodeURI(csvContent);

      // Trigger Browser Download
      const link = document.createElement("a");
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `analysis_report_${timestamp}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
"""

if 'function exportAllToCSV()' not in html:
    html = html.replace('</script>', export_js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Full CSV exporter successfully attached to index.html!")
