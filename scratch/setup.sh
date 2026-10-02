#!/usr/bin/env bash
set -e
cd ~/decoder_project 2>/dev/null || { echo "ERROR: ~/decoder_project not found. Run: cd ~ && ls"; exit 1; }
echo "In: $(pwd)"
[ -f public/index.html ] || { echo "ERROR: public/index.html not found. Run: ls -la  and paste it to me."; exit 1; }
mkdir -p scratch

# Make sure Cloudflare only publishes public/ (not scripts and backups)
if grep -q '"directory": "\."' wrangler.jsonc 2>/dev/null; then
  sed -i 's#"directory": "\."#"directory": "./public"#' wrangler.jsonc
  echo "Fixed wrangler.jsonc: now serves ./public"
fi
touch .gitignore
for line in ".wrangler/" "__pycache__/" "nano.*.save"; do
  grep -qxF "$line" .gitignore || echo "$line" >> .gitignore
done

cat > scratch/cipher_new.js <<'JS_END'
/* ========== CIPHER CODECS (encode + decode) ========== */
const byId = id => document.getElementById(id);
const _te = new TextEncoder(), _td = new TextDecoder();

const encBytes = (s, radix, pad) =>
  Array.from(_te.encode(s)).map(b => b.toString(radix).padStart(pad, '0')).join('');
const toBytes = (s, strip, size, radix, what) => {
  const d = s.replace(strip, '');
  if (!d) return [];
  if (d.length % size) throw new Error(`${what} input must be a multiple of ${size} digits`);
  return d.match(new RegExp(`.{${size}}`, 'g')).map(x => parseInt(x, radix));
};
const fromBytes = bytes => {
  if (bytes.some(b => b > 255)) throw new Error('Value out of byte range');
  return _td.decode(Uint8Array.from(bytes));
};

const b64e = s => { let bin = ''; _te.encode(s).forEach(b => bin += String.fromCharCode(b)); return btoa(bin); };
const b64d = s => _td.decode(Uint8Array.from(atob(s), c => c.charCodeAt(0)));

const B32 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
function b32e(s) {
  let bits = '', out = '';
  _te.encode(s).forEach(b => bits += b.toString(2).padStart(8, '0'));
  for (let i = 0; i < bits.length; i += 5) out += B32[parseInt(bits.slice(i, i + 5).padEnd(5, '0'), 2)];
  return out + '='.repeat((8 - out.length % 8) % 8);
}
function b32d(s) {
  let bits = '';
  for (const ch of s.toUpperCase().replace(/=+$/, '')) {
    const v = B32.indexOf(ch);
    if (v < 0) throw new Error('Invalid Base32 character');
    bits += v.toString(2).padStart(5, '0');
  }
  const bytes = [];
  for (let i = 0; i + 8 <= bits.length; i += 8) bytes.push(parseInt(bits.slice(i, i + 8), 2));
  return _td.decode(Uint8Array.from(bytes));
}

const rot13 = s => s.replace(/[a-z]/gi, c => {
  const base = c <= 'Z' ? 65 : 97;
  return String.fromCharCode((c.charCodeAt(0) - base + 13) % 26 + base);
});

const MORSE = {A:'.-',B:'-...',C:'-.-.',D:'-..',E:'.',F:'..-.',G:'--.',H:'....',I:'..',J:'.---',
  K:'-.-',L:'.-..',M:'--',N:'-.',O:'---',P:'.--.',Q:'--.-',R:'.-.',S:'...',T:'-',U:'..-',
  V:'...-',W:'.--',X:'-..-',Y:'-.--',Z:'--..',0:'-----',1:'.----',2:'..---',3:'...--',
  4:'....-',5:'.....',6:'-....',7:'--...',8:'---..',9:'----.'};
const MORSE_REV = Object.fromEntries(Object.entries(MORSE).map(([k, v]) => [v, k]));

const CODECS = {
  binary: { enc: s => encBytes(s, 2, 8),  dec: s => fromBytes(toBytes(s, /[^01]/g, 8, 2, 'Binary')) },
  hex:    { enc: s => encBytes(s, 16, 2), dec: s => fromBytes(toBytes(s.replace(/0x/gi, ''), /[^0-9a-f]/gi, 2, 16, 'Hex')) },
  octal:  { enc: s => encBytes(s, 8, 3),  dec: s => fromBytes(toBytes(s, /[^0-7]/g, 3, 8, 'Octal')) },
  a1z26: {
    enc: s => s.toUpperCase().split(/\s+/)
      .map(w => Array.from(w).filter(c => c >= 'A' && c <= 'Z').map(c => c.charCodeAt(0) - 64).join('-'))
      .filter(Boolean).join(' / '),
    dec: s => s.split(/\s*\/\s*/)
      .map(w => w.split(/[\s,-]+/).filter(Boolean)
        .map(n => { const v = parseInt(n, 10); return v >= 1 && v <= 26 ? String.fromCharCode(64 + v) : '?'; })
        .join('')).join(' ')
  },
  base64: { enc: b64e, dec: b64d },
  base32: { enc: b32e, dec: b32d },
  rot13:  { enc: rot13, dec: rot13 },
  morse: {
    enc: s => s.toUpperCase().split(/\s+/)
      .map(w => Array.from(w).map(c => MORSE[c] || '').filter(Boolean).join(' ')).join(' / '),
    dec: s => s.trim().split(/\s*\/\s*/)
      .map(w => w.split(/\s+/).map(c => MORSE_REV[c] || '?').join('')).join(' ')
  },
  url: { enc: encodeURIComponent, dec: decodeURIComponent }
};

const GROUPED = ['alpha', 'binary', 'hex', 'octal', 'base64', 'base32'];
const STRIP_WS_ON_DECODE = ['base64', 'base32'];

function processCipherBlocks() {
  const raw = byId('blockInput').value;
  const format = byId('baseFormat').value;
  const dirEl = byId('direction');
  const dir = dirEl ? dirEl.value : 'enc';
  const groupSize = parseInt(byId('groupSize').value, 10) || 5;
  const out = byId('blockOutput'), stats = byId('blockStats');

  if (!raw.trim()) {
    out.textContent = 'Awaiting input…'; out.dataset.raw = '';
    stats.textContent = 'Length: 0 · Groups: 0';
    return;
  }

  let result;
  try {
    if (format === 'alpha') {
      result = raw;
      if (byId('alphaOnly').checked) result = result.replace(/[^a-zA-Z0-9]/g, '');
      if (byId('uppercaseOnly').checked) result = result.toUpperCase();
    } else if (CODECS[format]) {
      const input = (dir === 'dec' && STRIP_WS_ON_DECODE.includes(format)) ? raw.replace(/\s+/g, '') : raw;
      result = CODECS[format][dir === 'dec' ? 'dec' : 'enc'](input);
    } else {
      throw new Error('Unknown format: ' + format);
    }
  } catch (e) {
    out.textContent = 'Error: ' + e.message; out.dataset.raw = ''; stats.textContent = '';
    return;
  }

  out.dataset.raw = result;
  if ((format === 'alpha' || dir === 'enc') && GROUPED.includes(format)) {
    const groups = result.match(new RegExp(`[\\s\\S]{1,${groupSize}}`, 'g')) || [];
    out.textContent = groups.join(' ') || 'No matching characters.';
    stats.textContent = `Length: ${result.length} · Groups: ${groups.length} (size ${groupSize})`;
  } else {
    out.textContent = result || 'No matching characters.';
    stats.textContent = `Length: ${result.length}`;
  }
}

const _swapBtn = byId('btnSwap');
if (_swapBtn) _swapBtn.addEventListener('click', () => {
  const raw = byId('blockOutput').dataset.raw;
  if (!raw) return;
  byId('blockInput').value = raw;
  const d = byId('direction');
  if (d) d.value = d.value === 'enc' ? 'dec' : 'enc';
  processCipherBlocks();
});
JS_END

cat > scratch/patch_cipher.py <<'PY_END'
import pathlib, re, shutil, sys

p = pathlib.Path('public/index.html')
new_js = pathlib.Path('scratch/cipher_new.js').read_text(encoding='utf-8')
src = p.read_text(encoding='utf-8')

if 'CIPHER CODECS' in src:
    sys.exit('Already patched - nothing to do.')

def must_sub(pattern, repl, text, flags=0, what=''):
    new, n = re.subn(pattern, lambda m: repl, text, count=1, flags=flags)
    if n != 1:
        sys.exit(f'ABORTED: could not find {what}. Nothing was changed.')
    return new

src = must_sub(r'    function processCipherBlocks\(\) \{.*?\n    \}\n', new_js + '\n', src, re.S, 'processCipherBlocks()')
src = must_sub(r'"alphaOnly"\]\.forEach\(', '"alphaOnly", "direction"].forEach(', src, 0, 'the blockInput listener list')
src = must_sub(r'<option value="alpha">Alphanumeric</option>',
  '<option value="alpha">Clean &amp; group (no encoding)</option>\n'
  '                  <option value="a1z26">A1Z26 (A=1 ... Z=26)</option>\n'
  '                  <option value="base64">Base64</option>\n'
  '                  <option value="base32">Base32</option>\n'
  '                  <option value="rot13">ROT13</option>\n'
  '                  <option value="morse">Morse</option>\n'
  '                  <option value="url">URL-encoded</option>', src, 0, 'the Alphanumeric option')

m = re.search(r'<input type="number" id="groupSize"[^>]*/>\s*</div>', src)
if not m:
    sys.exit('ABORTED: could not find the group size field. Nothing was changed.')
src = src[:m.end()] + '''
              <div>
                <label for="direction">Direction</label>
                <select id="direction">
                  <option value="enc">Encode</option>
                  <option value="dec">Decode</option>
                </select>
              </div>''' + src[m.end():]

m = re.search(r'<button[^>]*id="btnCopyBlocks"[^>]*>.*?</button>', src, re.S)
if not m:
    sys.exit('ABORTED: could not find the Copy Output button. Nothing was changed.')
src = src[:m.end()] + '\n            <button class="secondary sm" id="btnSwap" style="margin-top:10px">Swap</button>' + src[m.end():]

if 'rel="icon"' not in src:
    src = src.replace('</head>', '  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>*</text></svg>">\n</head>', 1)

pathlib.Path('scratch').mkdir(exist_ok=True)
shutil.copy(p, 'scratch/index.html.before-cipher-patch')
p.write_text(src, encoding='utf-8')
print('Patched OK. Backup saved to scratch/index.html.before-cipher-patch')
PY_END

python3 scratch/patch_cipher.py
echo
echo "---- wrangler.jsonc ----"; cat wrangler.jsonc
echo "---- public/ ----"; ls public
echo
echo "DONE. Next: preview with   npx wrangler dev"
