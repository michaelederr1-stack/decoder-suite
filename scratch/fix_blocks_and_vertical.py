with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix layout CSS for vertical text and dark mode textareas
css_fix = """
<style>
  /* Dark Mode Input & Textarea Standardization */
  textarea, input[type="text"], input[type="number"], select {
    background: #0a0f1a !important;
    color: #00f2fe !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    border-radius: 6px !important;
    padding: 10px !important;
    font-family: inherit;
  }

  textarea::placeholder {
    color: #4a5a6e !important;
  }

  /* Clean Vertical Text Layout */
  #vertOutputCSS {
    writing-mode: vertical-rl !important;
    text-orientation: upright !important;
    letter-spacing: 2px !important;
    line-height: 2 !important;
    font-family: 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif;
    font-size: 1.1rem;
    background: #050b14 !important;
    padding: 20px !important;
    border-radius: 8px !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    min-height: 200px;
    max-height: 350px;
    overflow-x: auto !important;
    display: inline-block;
  }

  /* Align Checkboxes neatly */
  .checkbox-group {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    color: #8a99ad;
    font-size: 0.85rem;
  }
</style>
"""

if '</head>' in html:
    html = html.replace('</head>', css_fix + '\n</head>')

# Unified JavaScript for Encoding Engine & Vertical Transposition
js_fix = """
    function processCipherBlocks() {
      // Find top block input regardless of ID variations
      const inputElem = document.getElementById('blockInput') || document.querySelectorAll('#page-blocks textarea')[0] || document.querySelector('textarea');
      const rawText = inputElem ? inputElem.value : '';
      
      const formatElem = document.getElementById('baseFormat');
      const format = formatElem ? formatElem.value : 'alpha';

      const groupSizeElem = document.getElementById('groupSize');
      const groupSize = groupSizeElem ? (parseInt(groupSizeElem.value, 10) || 5) : 5;

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
      const formatted = groups.join(' ');

      if (outElem) outElem.innerText = formatted || 'No matching characters.';
      if (statsElem) statsElem.innerText = `Total Symbols: ${processed.length} | Block Count: ${groups.length} (Size: ${groupSize})`;
    }

    function transposeVertical() {
      const inputElem = document.getElementById('vertInput') || document.querySelectorAll('#page-blocks textarea')[1];
      const input = inputElem ? inputElem.value : '';
      const dir = document.getElementById('vertDirection')?.value || 'ltr';
      const outputElem = document.getElementById('vertOutputCSS');

      if (!outputElem) return;

      if (!input || !input.trim()) {
        outputElem.innerText = '縦書きテキストプレビュー (Awaiting input...)';
        return;
      }

      outputElem.style.writingMode = dir === 'rtl' ? 'vertical-rl' : 'vertical-lr';
      outputElem.style.textOrientation = 'upright';
      outputElem.innerText = input;
    }

    // Attach global event listeners to ensure input triggers work dynamically
    document.addEventListener("DOMContentLoaded", function() {
      document.querySelectorAll('textarea, input, select').forEach(el => {
        el.addEventListener('input', () => {
          processCipherBlocks();
          transposeVertical();
        });
        el.addEventListener('change', () => {
          processCipherBlocks();
          transposeVertical();
        });
      });
    });
"""

# Replace JS logic safely
if 'function processCipherBlocks()' in html:
    import re
    html = re.sub(r'function processCipherBlocks\(\).*?(?=function |\n\s*</script>)', js_fix + '\n\n', html, flags=re.DOTALL)
else:
    html = html.replace('</script>', js_fix + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Encoding engine listeners hooked up and vertical text orientation corrected!")
