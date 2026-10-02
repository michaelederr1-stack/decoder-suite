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
