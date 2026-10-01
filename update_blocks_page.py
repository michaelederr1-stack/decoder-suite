with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Expanded Cipher & Multi-Base Grouping UI
blocks_tab_ui = """
<div id="page-blocks" class="tab-page">
  <div class="panel full-width">
    <h2>🔤 Cipher Grouping & Multi-Base Transmutation</h2>
    <p style="color: var(--text-dim, #8a99ad); font-size: 0.9rem; margin-bottom: 15px;">
      Convert and group raw payload data into standardized military block sizes, binary bits, hexadecimal bytes, or octal notation.
    </p>

    <div class="grid-encoders">
      <div class="encoder-card">
        <label for="blockInput">Input Text / Payload</label>
        <textarea id="blockInput" rows="4" placeholder="Enter text or raw data to convert and group..." oninput="processCipherBlocks()"></textarea>
        
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; align-items: center;">
          <div>
            <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Format Base:</label>
            <select id="baseFormat" onchange="processCipherBlocks()" style="padding: 6px 10px; border-radius: 4px; background: #0a0f1a; color: #00f2fe; border: 1px solid rgba(0,242,254,0.3);">
              <option value="alpha">Alphanumeric (Text Chunks)</option>
              <option value="binary">Binary (0s & 1s)</option>
              <option value="hex">Hexadecimal (0-F)</option>
              <option value="octal">Octal (Base 8)</option>
            </select>
          </div>

          <div>
            <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Group Size:</label>
            <input type="number" id="groupSize" value="5" min="1" max="32" style="width: 70px; padding: 6px; border-radius: 4px; background: #0a0f1a; color: #fff; border: 1px solid rgba(0,242,254,0.3);" onchange="processCipherBlocks()" oninput="processCipherBlocks()">
          </div>

          <div style="margin-top: 18px; display: flex; gap: 15px;">
            <label style="font-size: 0.85rem; color: #8a99ad; cursor: pointer;">
              <input type="checkbox" id="uppercaseOnly" checked onchange="processCipherBlocks()"> Uppercase
            </label>
            <label style="font-size: 0.85rem; color: #8a99ad; cursor: pointer;">
              <input type="checkbox" id="alphaOnly" checked onchange="processCipherBlocks()"> Strip Non-Alphanumeric
            </label>
          </div>
        </div>
      </div>

      <div class="encoder-card">
        <label>Formatted & Grouped Output</label>
        <pre id="blockOutput" style="white-space: pre-wrap; word-break: break-all; min-height: 100px; max-height: 250px; overflow-y: auto;">Awaiting input...</pre>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #00f2fe;" id="blockStats">Length: 0 symbols | Groups: 0</div>
      </div>
    </div>
  </div>
</div>
"""

# JavaScript engine handling Alphanumeric, Binary, Hex, and Octal conversion & grouping
js_blocks_engine = """
    function processCipherBlocks() {
      const rawText = document.getElementById('blockInput')?.value || '';
      const format = document.getElementById('baseFormat')?.value || 'alpha';
      const groupSize = parseInt(document.getElementById('groupSize')?.value, 10) || 5;
      const uppercaseOnly = document.getElementById('uppercaseOnly')?.checked;
      const alphaOnly = document.getElementById('alphaOnly')?.checked;

      if (!rawText) {
        if (document.getElementById('blockOutput')) document.getElementById('blockOutput').innerText = 'Awaiting input...';
        if (document.getElementById('blockStats')) document.getElementById('blockStats').innerText = 'Length: 0 symbols | Groups: 0';
        return;
      }

      let processed = '';

      if (format === 'binary') {
        processed = Array.from(rawText).map(c => c.charCodeAt(0).toString(2).padStart(8, '0')).join('');
      } else if (format === 'hex') {
        processed = Array.from(rawText).map(c => c.charCodeAt(0).toString(16).padStart(2, '0')).join('');
      } else if (format === 'octal') {
        processed = Array.from(rawText).map(c => c.charCodeAt(0).toString(8).padStart(3, '0')).join('');
      } else {
        processed = rawText;
        if (alphaOnly) processed = processed.replace(/[^a-zA-Z0-9]/g, '');
      }

      if (uppercaseOnly && format !== 'binary' && format !== 'octal') {
        processed = processed.toUpperCase();
      }

      // Chunk string into designated group sizes
      const regex = new RegExp('.{1,' + groupSize + '}', 'g');
      const groups = processed.match(regex) || [];
      const formatted = groups.join(' ');

      const outElem = document.getElementById('blockOutput');
      const statsElem = document.getElementById('blockStats');

      if (outElem) outElem.innerText = formatted || 'No matching characters.';
      if (statsElem) statsElem.innerText = `Total Symbols: ${processed.length} | Block Count: ${groups.length} (Size: ${groupSize})`;
    }
"""

# 1. Strip out any old inline cipher block panels from the bottom
import re
html = re.sub(r'<div class="panel full-width"[^>]*>.*?Alphanumeric Blocks & Cipher Grouping.*?</div>\s*</div>', '', html, flags=re.DOTALL)

# 2. Inject new dedicated tab page before closing script container or container end
if 'id="page-blocks"' not in html:
    if '</main>' in html:
        html = html.replace('</main>', blocks_tab_ui + '\n</main>')
    elif '</div>' in html:
        html = html.replace('<!-- END PANELS -->', blocks_tab_ui + '\n<!-- END PANELS -->') if '<!-- END PANELS -->' in html else html.replace('<script>', blocks_tab_ui + '\n  <script>')

# 3. Replace processing function logic
if 'function processCipherBlocks()' in html:
    html = re.sub(r'function processCipherBlocks\(\).*?\n    \}', js_blocks_engine, html, flags=re.DOTALL)
else:
    html = html.replace('</script>', js_blocks_engine + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Moved Cipher Grouping to its own tab and enabled Octal, Hex, Binary & Alphanumeric base modes!")
