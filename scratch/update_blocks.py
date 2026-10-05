with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Alphanumeric Block UI into HTML
blocks_ui = """
    <div class="panel full-width" style="margin-top: 15px;">
      <h2>Alphanumeric Blocks & Cipher Grouping</h2>
      <div class="grid-encoders">
        <div class="encoder-card">
          <label for="blockInput">Input Text / Ciphertext</label>
          <textarea id="blockInput" rows="3" placeholder="Enter text to group or sanitize..." oninput="processCipherBlocks()"></textarea>
          <div style="display: flex; gap: 10px; margin-top: 8px; align-items: center;">
            <label style="font-size: 0.85rem; color: var(--text-dim);">Group Size:</label>
            <input type="number" id="groupSize" value="5" min="1" max="20" style="width: 70px;" onchange="processCipherBlocks()" oninput="processCipherBlocks()">
            
            <label style="font-size: 0.85rem; color: var(--text-dim); margin-left: 10px;">
              <input type="checkbox" id="uppercaseOnly" checked onchange="processCipherBlocks()"> Uppercase
            </label>
            <label style="font-size: 0.85rem; color: var(--text-dim);">
              <input type="checkbox" id="alphaOnly" checked onchange="processCipherBlocks()"> Strip Non-Alphanumeric
            </label>
          </div>
        </div>
        <div class="encoder-card">
          <label>Grouped Output</label>
          <pre id="blockOutput">Awaiting input...</pre>
          <div style="margin-top: 8px; font-size: 0.85rem; color: var(--text-dim);" id="blockStats">Length: 0 chars | Groups: 0</div>
        </div>
      </div>
    </div>
"""

# Insert panel before script tag or container end
if 'Alphanumeric Blocks & Cipher Grouping' not in html:
    html = html.replace('<!-- END PANELS -->', blocks_ui + '\n<!-- END PANELS -->') if '<!-- END PANELS -->' in html else html.replace('<script>', blocks_ui + '\n  <script>')

# 2. Add JavaScript processing logic
js_blocks = """
    function processCipherBlocks() {
      const rawText = document.getElementById('blockInput')?.value || '';
      const groupSize = parseInt(document.getElementById('groupSize')?.value, 10) || 5;
      const uppercaseOnly = document.getElementById('uppercaseOnly')?.checked;
      const alphaOnly = document.getElementById('alphaOnly')?.checked;

      if (!rawText.trim()) {
        if (document.getElementById('blockOutput')) document.getElementById('blockOutput').innerText = 'Awaiting input...';
        if (document.getElementById('blockStats')) document.getElementById('blockStats').innerText = 'Length: 0 chars | Groups: 0';
        return;
      }

      let processed = rawText;

      if (alphaOnly) {
        processed = processed.replace(/[^a-zA-Z0-9]/g, '');
      }

      if (uppercaseOnly) {
        processed = processed.toUpperCase();
      }

      // Group into chunks
      const regex = new RegExp('.{1,' + groupSize + '}', 'g');
      const groups = processed.match(regex) || [];
      const formatted = groups.join(' ');

      document.getElementById('blockOutput').innerText = formatted || 'No matching alphanumeric characters.';
      document.getElementById('blockStats').innerText = `Length: ${processed.length} chars | Groups: ${groups.length}`;
    }
"""

if 'function processCipherBlocks()' not in html:
    html = html.replace('function processAll() {', js_blocks + '\n    function processAll() {')
    html = html.replace('processAll();', 'processAll();\n      processCipherBlocks();')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Alphanumeric cipher grouping module added to index.html!")
