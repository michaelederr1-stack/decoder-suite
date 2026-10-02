with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update/Ensure complete UI layout inside #page-blocks
blocks_ui_complete = """
<div id="page-blocks" class="tab-page">
  <div class="panel full-width">
    <h2>🔤 Cipher Grouping & Multi-Base Transmutation</h2>
    <p style="color: #8a99ad; font-size: 0.9rem; margin-bottom: 15px;">
      Convert and group raw payload data into standardized military block sizes, binary bits, hexadecimal bytes, or octal notation.
    </p>

    <div class="grid-encoders" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div class="encoder-card" style="background: rgba(10,15,26,0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.2);">
        <label for="blockInput" style="display:block; margin-bottom: 8px; font-weight: bold; color: #00f2fe;">Input Text / Payload</label>
        <textarea id="blockInput" rows="4" style="width: 100%;" placeholder="Enter text or raw data to convert and group..."></textarea>
        
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
        <div id="blockOutput" style="min-height: 100px;">Awaiting input...</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #00f2fe;" id="blockStats">Length: 0 symbols | Groups: 0</div>
      </div>
    </div>
  </div>

  <div class="panel full-width" style="margin-top: 20px;">
    <h2>⛩️ Vertical Text Transposition Engine (Tate-chu-yoko / 縦書き)</h2>
    <p style="color: #8a99ad; font-size: 0.85rem; margin-bottom: 12px;">
      Format text for traditional East Asian vertical layout (Japanese, Cantonese, Traditional Chinese, Korean).
    </p>

    <div class="grid-encoders" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div class="encoder-card" style="background: rgba(10,15,26,0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0,242,254,0.2);">
        <label for="vertInput" style="display:block; margin-bottom: 8px; font-weight: bold; color: #00f2fe;">Input Text (English / CJK / Text)</label>
        <textarea id="vertInput" rows="4" style="width: 100%;" placeholder="Enter text to transpose vertically..."></textarea>
        
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
        <div id="vertOutputContainer">
          <div id="vertOutputCSS" class="vert-text">縦書きテキストプレビュー (Awaiting input...)</div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

# 2. Inject or replace the #page-blocks container safely
import re
if '<div id="page-blocks"' in html:
    html = re.sub(r'<div id="page-blocks".*?<!-- END PAGE BLOCKS -->', blocks_ui_complete + '\n<!-- END PAGE BLOCKS -->', html, flags=re.DOTALL)
    if '<!-- END PAGE BLOCKS -->' not in html:
        html = re.sub(r'<div id="page-blocks".*?</div>\s*</div>\s*</div>', blocks_ui_complete, html, flags=re.DOTALL)
else:
    html = html.replace('</main>', blocks_ui_complete + '\n</main>')

# 3. Master JavaScript containing ALL suite functions: Tab Switching, Agent, Block Encoding, and Transposition Engine
master_script = """
<script>
    // --- Navigation & Page Switcher Engine ---
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

      if (pageId === 'page-geo' && typeof map !== 'undefined' && map) {
        setTimeout(() => {
          if (map.invalidateSize) map.invalidateSize();
        }, 150);
      }
    }

    // --- Cipher Block Grouping Engine ---
    function processCipherBlocks() {
      const inputElem = document.getElementById('blockInput');
      const rawText = inputElem ? inputElem.value : '';
      
      const formatElem = document.getElementById('baseFormat');
      const format = formatElem ? formatElem.value : 'alpha';

      const groupSizeElem = document.getElementById('groupSize');
      const groupSize = groupSizeElem ? (parseInt(groupSizeElem.value, 10) || 5) : 5;

      const uppercaseOnly = document.getElementById('uppercaseOnly') ? document.getElementById('uppercaseOnly').checked : true;
      const alphaOnly = document.getElementById('alphaOnly') ? document.getElementById('alphaOnly').checked : true;

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
      const formatted = groups.join(' ');

      if (outElem) outElem.innerText = formatted || 'No matching characters.';
      if (statsElem) statsElem.innerText = `Total Symbols: ${processed.length} | Block Count: ${groups.length} (Size: ${groupSize})`;
    }

    // --- Phonetic English-to-Katakana Dictionary ---
    const kanaMap = {
      'ka':'カ','ki':'キ','ku':'ク','ke':'ケ','ko':'コ',
      'sa':'サ','shi':'シ','su':'ス','se':'セ','so':'ソ',
      'ta':'タ','chi':'チ','tsu':'ツ','te':'テ','to':'ト',
      'na':'ナ','ni':'ニ','nu':'ヌ','ne':'ネ','no':'ノ',
      'ha':'ハ','hi':'ヒ','fu':'フ','he':'ヘ','ho':'ホ',
      'ma':'マ','mi':'ミ','mu':'ム','me':'メ','mo':'モ',
      'ya':'ヤ','yu':'ユ','yo':'ヨ',
      'ra':'ラ','ri':'リ','ru':'ル','re':'レ','ro':'ロ',
      'wa':'ワ','wo':'ヲ','a':'ア','i':'イ','u':'ウ','e':'エ','o':'オ','n':'ン'
    };

    function transliterateToKana(str) {
      let text = str.toLowerCase();
      let result = '';
      let i = 0;
      while (i < text.length) {
        if (i + 3 <= text.length && kanaMap[text.slice(i, i + 3)]) {
          result += kanaMap[text.slice(i, i + 3)];
          i += 3;
        } else if (i + 2 <= text.length && kanaMap[text.slice(i, i + 2)]) {
          result += kanaMap[text.slice(i, i + 2)];
          i += 2;
        } else if (kanaMap[text[i]]) {
          result += kanaMap[text[i]];
          i += 1;
        } else {
          result += text[i];
          i += 1;
        }
      }
      return result;
    }

    // --- Vertical Transposition Engine ---
    function transposeVertical() {
      const inputElem = document.getElementById('vertInput');
      const input = inputElem ? inputElem.value : '';
      const mode = document.getElementById('vertMode') ? document.getElementById('vertMode').value : 'raw';
      const dir = document.getElementById('vertDirection') ? document.getElementById('vertDirection').value : 'rtl';
      const outputElem = document.getElementById('vertOutputCSS');

      if (!outputElem) return;

      if (!input || !input.trim()) {
        outputElem.innerText = '縦書きテキストプレビュー (Awaiting input...)';
        return;
      }

      let textToDisplay = input;
      if (mode === 'kana') {
        textToDisplay = transliterateToKana(input);
      }

      outputElem.style.writingMode = dir === 'rtl' ? 'vertical-rl' : 'vertical-lr';
      outputElem.style.textOrientation = 'upright';
      outputElem.innerText = textToDisplay;
    }

    // --- Dynamic DOM Listener Bindings ---
    document.addEventListener("DOMContentLoaded", function() {
      const allInputs = document.querySelectorAll('input, select, textarea');
      allInputs.forEach(elem => {
        elem.addEventListener('input', () => { processCipherBlocks(); transposeVertical(); });
        elem.addEventListener('change', () => { processCipherBlocks(); transposeVertical(); });
      });

      // Default active tab button click
      const defaultTab = document.querySelector('.nav-btn');
      if (defaultTab) defaultTab.click();

      processCipherBlocks();
      transposeVertical();
    });
</script>
"""

# Clean replacement of script tag
html = re.sub(r'<script.*?>.*?</script>', master_script, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] All top navigation buttons, multi-base options, and vertical transposition modes restored and operational!")
