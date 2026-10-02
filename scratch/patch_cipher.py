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
