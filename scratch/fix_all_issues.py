with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Standardized dark-mode styles and CSS vertical layout rules
styles = """
<style>
  /* Standard Dark Mode Styling for Form Inputs */
  #page-blocks textarea, 
  #page-blocks input[type="text"], 
  #page-blocks input[type="number"], 
  #page-blocks select {
    background-color: #0a0f1a !important;
    color: #00f2fe !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    border-radius: 6px !important;
    padding: 10px !important;
    font-family: monospace, sans-serif !important;
    box-sizing: border-box !important;
  }

  /* Output Display Box */
  #blockOutput {
    background: #050b14 !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    border-radius: 6px !important;
    padding: 12px !important;
    color: #50fa7b !important;
    font-family: monospace !important;
    white-space: pre-wrap !important;
    word-break: break-all !important;
    min-height: 80px;
  }

  /* Vertical CJK Writing Mode Output Container */
  #vertOutputContainer {
    background: #050b14 !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    border-radius: 6px !important;
    padding: 15px !important;
    min-height: 200px;
    max-height: 350px;
    overflow-x: auto !important;
    overflow-y: hidden !important;
  }

  .vert-text {
    writing-mode: vertical-rl !important;
    text-orientation: upright !important;
    letter-spacing: 4px !important;
    line-height: 2.2 !important;
    font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', 'Microsoft YaHei', serif !important;
    font-size: 1.2rem !important;
    color: #00f2fe !important;
    display: inline-block !important;
    height: 100% !important;
  }
</style>
"""

# Inject styles before closing head
if '</head>' in html and '/* Standard Dark Mode Styling' not in html:
    html = html.replace('</head>', styles + '\n</head>')

# 2. Complete, reliable JavaScript engine with English-to-Katakana/CJK converter
js_engine = """
<script>
    // --- 1. Top Encoding & Block Grouping Engine ---
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

    // --- Basic English-to-Katakana Phonetic Transliteration Map ---
    const kanaMap = {
      'a':'ア','i':'イ','u':'ウ','e':'エ','o':'オ',
      'ka':'カ','ki':'キ','ku':'ク','ke':'ケ','ko':'コ',
      'sa':'サ','shi':'シ','su':'ス','se':'セ','so':'ソ',
      'ta':'タ','chi':'チ','tsu':'ツ','te':'テ','to':'ト',
      'na':'ナ','ni':'ニ','nu':'ヌ','ne':'ネ','no':'ノ',
      'ha':'ハ','hi':'ヒ','fu':'フ','he':'ヘ','ho':'ホ',
      'ma':'マ','mi':'ミ','mu':'ム','me':'メ','mo':'モ',
      'ya':'ヤ','yu':'ユ','yo':'ヨ',
      'ra':'ラ','ri':'リ','ru':'ル','re':'レ','ro':'ロ',
      'wa':'ワ','wo':'ヲ','n':'ン'
    };

    function transliterateToKana(str) {
      let text = str.toLowerCase();
      let result = '';
      let i = 0;
      while (i < text.length) {
        if (i + 2 <= text.length && kanaMap[text.slice(i, i + 2)]) {
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

    // --- 2. Vertical Transposition Engine ---
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

      // If user selected Phonetic Katakana mode and input contains English
      if (mode === 'kana') {
        textToDisplay = transliterateToKana(input);
      }

      outputElem.style.writingMode = dir === 'rtl' ? 'vertical-rl' : 'vertical-lr';
      outputElem.style.textOrientation = 'upright';
      outputElem.innerText = textToDisplay;
    }

    // Attach explicit global event listeners
    document.addEventListener("DOMContentLoaded", function() {
      const bInput = document.getElementById('blockInput');
      if (bInput) {
        bInput.addEventListener('input', processCipherBlocks);
        bInput.addEventListener('keyup', processCipherBlocks);
      }

      const vInput = document.getElementById('vertInput');
      if (vInput) {
        vInput.addEventListener('input', transposeVertical);
        vInput.addEventListener('keyup', transposeVertical);
      }

      processCipherBlocks();
      transposeVertical();
    });
</script>
"""

# Replace all existing script tags with the clean unified script
import re
html = re.sub(r'<script.*?>.*?</script>', js_engine, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Completely rebuilt script engine with fixed listener bindings and Phonetic Kana transposition!")
