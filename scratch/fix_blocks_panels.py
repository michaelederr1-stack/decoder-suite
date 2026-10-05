with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Fully structured HTML for #page-blocks with TWO separate panels
page_blocks_html = """
<div id="page-blocks" class="tab-page">
  <!-- PANEL 1: Cipher Grouping & Multi-Base Transmutation -->
  <div class="panel full-width" style="margin-bottom: 25px;">
    <h2>🔤 Cipher Grouping & Multi-Base Transmutation</h2>
    <p style="color: #8a99ad; font-size: 0.9rem; margin-bottom: 15px;">
      Convert and group raw payload data into standardized military block sizes, binary bits, hexadecimal bytes, or octal notation.
    </p>

    <div class="grid-encoders" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div class="encoder-card" style="background: rgba(10,15,26,0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.2);">
        <label for="blockInput" style="display:block; margin-bottom: 8px; font-weight: bold; color: #00f2fe;">Input Text / Payload</label>
        <textarea id="blockInput" rows="4" style="width: 100%; box-sizing: border-box;" placeholder="Enter text or raw data to convert and group..."></textarea>
        
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; align-items: center;">
          <div>
            <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Format Base:</label>
            <select id="baseFormat">
              <option value="alpha">Alphanumeric (Text Chunks)</option>
              <option value="binary">Binary (0s & 1s)</option>
              <option value="hex">Hexadecimal (0-F)</option>
              <option value="octal">Octal (Base 8)</option>
            </select>
          </div>

          <div>
            <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Group Size:</label>
            <input type="number" id="groupSize" value="5" min="1" max="32" style="width: 70px;">
          </div>

          <div style="margin-top: 18px; display: flex; gap: 15px;">
            <label style="font-size: 0.85rem; color: #8a99ad; cursor: pointer;">
              <input type="checkbox" id="uppercaseOnly" checked> Uppercase
            </label>
            <label style="font-size: 0.85rem; color: #8a99ad; cursor: pointer;">
              <input type="checkbox" id="alphaOnly" checked> Strip Non-Alphanumeric
            </label>
          </div>
        </div>
      </div>

      <div class="encoder-card" style="background: rgba(10,15,26,0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.2);">
        <label style="display:block; margin-bottom: 8px; font-weight: bold; color: #00f2fe;">Formatted & Grouped Output</label>
        <div id="blockOutput" style="min-height: 100px; background: #050b14; padding: 10px; border-radius: 6px; color: #50fa7b; font-family: monospace;">Awaiting input...</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #00f2fe;" id="blockStats">Length: 0 symbols | Groups: 0</div>
      </div>
    </div>
  </div>

  <!-- PANEL 2: Vertical Text Transposition Engine -->
  <div class="panel full-width">
    <h2>⛩️ Vertical Text Transposition Engine (Tate-chu-yoko / 縦書き)</h2>
    <p style="color: #8a99ad; font-size: 0.85rem; margin-bottom: 12px;">
      Format text for traditional East Asian vertical layout (Japanese, Cantonese, Traditional Chinese, Korean).
    </p>

    <div class="grid-encoders" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div class="encoder-card" style="background: rgba(10,15,26,0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.2);">
        <label for="vertInput" style="display:block; margin-bottom: 8px; font-weight: bold; color: #00f2fe;">Input Text (English / CJK / Text)</label>
        <textarea id="vertInput" rows="4" style="width: 100%; box-sizing: border-box;" placeholder="Enter text to transpose vertically..."></textarea>
        
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; align-items: center;">
          <div>
            <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Transposition Mode:</label>
            <select id="vertMode">
              <option value="raw">Direct Vertical Stacking (CJK / Text)</option>
              <option value="kana">Phonetic Transliteration (English -> Katakana)</option>
            </select>
          </div>

          <div>
            <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Column Flow:</label>
            <select id="vertDirection">
              <option value="rtl">Traditional (Right-to-Left Columns)</option>
              <option value="ltr">Modern (Left-to-Right Columns)</option>
            </select>
          </div>
        </div>
      </div>

      <div class="encoder-card" style="background: rgba(10,15,26,0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.2);">
        <label style="display:block; margin-bottom: 8px; font-weight: bold; color: #00f2fe;">Transposed Vertical Output</label>
        <div id="vertOutputContainer" style="background: #050b14; padding: 15px; border-radius: 6px; min-height: 200px; max-height: 350px; overflow-x: auto;">
          <div id="vertOutputCSS" style="writing-mode: vertical-rl; text-orientation: upright; font-size: 1.2rem; color: #00f2fe; line-height: 2.2; letter-spacing: 4px;">縦書きテキストプレビュー (Awaiting input...)</div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

# Replace entire block tab content
if '<div id="page-blocks"' in html:
    html = re.sub(r'<div id="page-blocks".*?</div>\s*<!-- END BLOCK TAB -->', page_blocks_html + '\n<!-- END BLOCK TAB -->', html, flags=re.DOTALL)
    if '<!-- END BLOCK TAB -->' not in html:
        html = re.sub(r'<div id="page-blocks".*?</div>\s*</div>\s*</div>', page_blocks_html, html, flags=re.DOTALL)

# Re-inject JS script ensuring all nav buttons and both encoder blocks function simultaneously
js_script = """
<script>
    // Tab Switching Engine for top buttons
    function switchPage(pageId, btnElement) {
      document.querySelectorAll('.tab-page').forEach(page => {
        page.classList.remove('active');
        page.style.display = 'none';
      });

      document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
      });

      const targetPage = document.getElementById(pageId);
      if (targetPage) {
        targetPage.classList.add('active');
        targetPage.style.display = 'block';
      }

      if (btnElement) {
        btnElement.classList.add('active');
      }
    }

    // Process Top Cipher Blocks
    function processCipherBlocks() {
      const inputElem = document.getElementById('blockInput');
      const rawText = inputElem ? inputElem.value : '';
      const format = document.getElementById('baseFormat')?.value || 'alpha';
      const groupSize = parseInt(document.getElementById('groupSize')?.value, 10) || 5;
      const uppercaseOnly = document.getElementById('uppercaseOnly')?.checked ?? true;
      const alphaOnly = document.getElementById('alphaOnly')?.checked ?? true;

      const outElem = document.getElementById('blockOutput');
      const statsElem = document.getElementById('blockStats');

      if (!rawText || !rawText.trim()) {
        if (outElem) outElem.innerText = 'Awaiting input...';
        if (statsElem) statsElem.innerText = 'Length: 0 symbols | Groups: 0';
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

      const regex = new RegExp('.{1,' + groupSize + '}', 'g');
      const groups = processed.match(regex) || [];

      if (outElem) outElem.innerText = groups.join(' ') || 'No matching characters.';
      if (statsElem) statsElem.innerText = `Total Symbols: ${processed.length} | Block Count: ${groups.length} (Size: ${groupSize})`;
    }

    // Phonetic Conversion
    const kanaMap = {
      'ka':'カ','ki':'キ','ku':'ク','ke':'ケ','ko':'コ','sa':'サ','shi':'シ','su':'ス','se':'セ','so':'ソ',
      'ta':'タ','chi':'チ','tsu':'ツ','te':'テ','to':'ト','na':'ナ','ni':'ニ','nu':'ヌ','ne':'ネ','no':'ノ',
      'ha':'ハ','hi':'ヒ','fu':'フ','he':'ヘ','ho':'ホ','ma':'マ','mi':'ミ','mu':'ム','me':'メ','mo':'モ',
      'ya':'ヤ','yu':'ユ','yo':'ヨ','ra':'ラ','ri':'リ','ru':'ル','re':'レ','ro':'ロ','wa':'ワ','wo':'ヲ',
      'a':'ア','i':'イ','u':'ウ','e':'エ','o':'オ','n':'ン'
    };

    function transliterateToKana(str) {
      let text = str.toLowerCase(), result = '', i = 0;
      while (i < text.length) {
        if (i + 3 <= text.length && kanaMap[text.slice(i, i + 3)]) { result += kanaMap[text.slice(i, i + 3)]; i += 3; }
        else if (i + 2 <= text.length && kanaMap[text.slice(i, i + 2)]) { result += kanaMap[text.slice(i, i + 2)]; i += 2; }
        else if (kanaMap[text[i]]) { result += kanaMap[text[i]]; i += 1; }
        else { result += text[i]; i += 1; }
      }
      return result;
    }

    // Process Bottom Transposition Engine
    function transposeVertical() {
      const input = document.getElementById('vertInput')?.value || '';
      const mode = document.getElementById('vertMode')?.value || 'raw';
      const dir = document.getElementById('vertDirection')?.value || 'rtl';
      const outputElem = document.getElementById('vertOutputCSS');

      if (!outputElem) return;
      if (!input || !input.trim()) {
        outputElem.innerText = '縦書きテキストプレビュー (Awaiting input...)';
        return;
      }

      outputElem.style.writingMode = dir === 'rtl' ? 'vertical-rl' : 'vertical-lr';
      outputElem.innerText = mode === 'kana' ? transliterateToKana(input) : input;
    }

    // Event listeners
    document.addEventListener("DOMContentLoaded", function() {
      document.querySelectorAll('input, select, textarea').forEach(elem => {
        elem.addEventListener('input', () => { processCipherBlocks(); transposeVertical(); });
        elem.addEventListener('change', () => { processCipherBlocks(); transposeVertical(); });
      });

      processCipherBlocks();
      transposeVertical();
    });
</script>
"""

html = re.sub(r'<script.*?>.*?</script>', js_script, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Restored both panels directly inside #page-blocks tab with full button support!")
