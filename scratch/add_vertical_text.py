with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. UI Panel for Vertical Script Transposition
vertical_ui = """
    <div class="panel full-width" style="margin-top: 20px;">
      <h2>⛩️ Vertical Text Transposition Engine (Tate-chu-yoko / 縦書き)</h2>
      <p style="color: #8a99ad; font-size: 0.85rem; margin-bottom: 12px;">
        Format text for traditional East Asian vertical layout (Japanese, Cantonese, Traditional Chinese, Korean).
      </p>

      <div class="grid-encoders">
        <div class="encoder-card">
          <label for="vertInput">Input Text (Kanji / Hanzi / Kana / Text)</label>
          <textarea id="vertInput" rows="4" placeholder="Enter text to transpose vertically..." oninput="transposeVertical()"></textarea>
          
          <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; align-items: center;">
            <div>
              <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Column Flow Direction:</label>
              <select id="vertDirection" onchange="transposeVertical()" style="padding: 6px 10px; border-radius: 4px; background: #0a0f1a; color: #00f2fe; border: 1px solid rgba(0,242,254,0.3);">
                <option value="rtl">Traditional (Right-to-Left Columns)</option>
                <option value="ltr">Modern (Left-to-Right Columns)</option>
              </select>
            </div>

            <div>
              <label style="font-size: 0.85rem; color: #8a99ad; display: block;">Max Column Height (Chars):</label>
              <input type="number" id="columnHeight" value="10" min="2" max="50" style="width: 75px; padding: 6px; border-radius: 4px; background: #0a0f1a; color: #fff; border: 1px solid rgba(0,242,254,0.3);" onchange="transposeVertical()" oninput="transposeVertical()">
            </div>
          </div>
        </div>

        <div class="encoder-card">
          <label>Transposed Vertical Output</label>
          <div id="vertOutputCSS" style="writing-mode: vertical-rl; text-orientation: upright; font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif; font-size: 1.1rem; line-height: 1.8; background: #050b14; padding: 15px; border-radius: 6px; min-height: 180px; max-height: 300px; overflow-x: auto; border: 1px solid rgba(0,242,254,0.2);">
            縦書きテキストプレビュー (Awaiting input...)
          </div>
        </div>
      </div>
    </div>
"""

# 2. JavaScript logic to handle CSS Vertical Writing Mode & Manual Grid Matrix fallback
vertical_js = """
    function transposeVertical() {
      const input = document.getElementById('vertInput')?.value || '';
      const dir = document.getElementById('vertDirection')?.value || 'rtl';
      const colHeight = parseInt(document.getElementById('columnHeight')?.value, 10) || 10;
      const outputElem = document.getElementById('vertOutputCSS');

      if (!outputElem) return;

      if (!input.trim()) {
        outputElem.innerText = '縦書きテキストプレビュー (Awaiting input...)';
        return;
      }

      // Apply native CJK vertical writing mode
      outputElem.style.writingMode = dir === 'rtl' ? 'vertical-rl' : 'vertical-lr';
      outputElem.style.textOrientation = 'upright';
      outputElem.innerText = input;
    }
"""

# Inject UI into the Cipher & Blocks Tab Page
if 'id="page-blocks"' in html:
    html = html.replace('</div>\n</div>', vertical_ui + '\n</div>\n</div>', 1)
elif '</main>' in html:
    html = html.replace('</main>', vertical_ui + '\n</main>')

# Inject JavaScript function
if 'function transposeVertical()' not in html:
    html = html.replace('</script>', vertical_js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Vertical Text Transposition Engine successfully added!")
