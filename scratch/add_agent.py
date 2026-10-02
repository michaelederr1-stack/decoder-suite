with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Include Math.js CDN for robust complex equation solving
mathjs_cdn = '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.js"></script>'
if 'math.js' not in html:
    html = html.replace('</head>', f'  {mathjs_cdn}\n</head>')

# 2. Add Assistant Drawer UI to the bottom-right corner
agent_ui = """
<div id="agent-drawer" style="position: fixed; bottom: 20px; right: 20px; width: 350px; background: rgba(16, 22, 36, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); z-index: 9999; font-family: sans-serif; transition: all 0.3s ease;">
  <div id="agent-header" onclick="toggleAgentDrawer()" style="padding: 12px 16px; background: linear-gradient(135deg, rgba(0,242,254,0.2), rgba(79,172,254,0.2)); border-radius: 12px 12px 0 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,242,254,0.2);">
    <span style="font-weight: bold; color: #00f2fe; font-size: 0.95rem;">🤖 Suite AI Assistant & Solver</span>
    <span id="agent-toggle-icon" style="color: #00f2fe;">▲</span>
  </div>
  
  <div id="agent-body" style="padding: 15px; display: none; max-height: 420px; overflow-y: auto;">
    <div style="display: flex; gap: 8px; margin-bottom: 10px;">
      <button onclick="runTroubleshooter()" style="font-size: 0.75rem; padding: 6px 10px; flex: 1;">🔍 Audit Suite Inputs</button>
      <button onclick="clearAgentLog()" style="font-size: 0.75rem; padding: 6px 10px; background: rgba(255,255,255,0.1) !important; color: #fff !important;">Clear</button>
    </div>

    <div id="agent-log" style="background: rgba(5, 11, 20, 0.8); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 10px; font-size: 0.85rem; color: #c0c9d6; min-height: 120px; max-height: 200px; overflow-y: auto; margin-bottom: 10px; white-space: pre-wrap; word-break: break-all;">
Ready to assist. Evaluate complex math expressions or audit page configurations.
    </div>

    <div style="display: flex; gap: 6px;">
      <input type="text" id="agentInput" placeholder="e.g. sin(45 deg) * 100 or 0x4F + 12" style="flex: 1; padding: 8px; font-size: 0.85rem; border-radius: 4px; border: 1px solid rgba(0,242,254,0.3); background: #0a0f1a; color: #fff;" onkeydown="if(event.key==='Enter') solveMathExpression()">
      <button onclick="solveMathExpression()" style="padding: 8px 12px; font-size: 0.85rem;">Solve</button>
    </div>
  </div>
</div>
"""

if 'id="agent-drawer"' not in html:
    html = html.replace('</body>', agent_ui + '\n</body>')

# 3. Add JavaScript Engine for Math Solving and Input Troubleshooting
agent_js = """
    function toggleAgentDrawer() {
      const body = document.getElementById('agent-body');
      const icon = document.getElementById('agent-toggle-icon');
      if (body.style.display === 'none' || !body.style.display) {
        body.style.display = 'block';
        icon.innerText = '▼';
      } else {
        body.style.display = 'none';
        icon.innerText = '▲';
      }
    }

    function appendAgentLog(msg, type = 'info') {
      const log = document.getElementById('agent-log');
      if (!log) return;
      const color = type === 'error' ? '#ff5555' : (type === 'success' ? '#50fa7b' : '#00f2fe');
      log.innerHTML += `\\n<span style="color: ${color}">> ${msg}</span>`;
      log.scrollTop = log.scrollHeight;
    }

    function clearAgentLog() {
      const log = document.getElementById('agent-log');
      if (log) log.innerText = 'Assistant reset. Ready.';
    }

    function solveMathExpression() {
      const input = document.getElementById('agentInput')?.value || '';
      if (!input.trim()) return;

      appendAgentLog(`Eval: ${input}`, 'info');
      try {
        if (typeof math !== 'undefined') {
          const result = math.evaluate(input);
          appendAgentLog(`Result: ${result}`, 'success');
        } else {
          // Fallback basic evaluator if CDN loading is delayed
          const result = Function('"use strict";return (' + input + ')')();
          appendAgentLog(`Result: ${result}`, 'success');
        }
      } catch (err) {
        appendAgentLog(`Error: ${err.message}`, 'error');
      }
    }

    function runTroubleshooter() {
      appendAgentLog("Running Suite Diagnostics...", "info");
      let issues = 0;

      // 1. Check Observer Bearings
      const brng1 = parseFloat(document.getElementById('obs1_brng')?.value);
      const brng2 = parseFloat(document.getElementById('obs2_brng')?.value);

      if (!isNaN(brng1) && !isNaN(brng2) && Math.abs(brng1 - brng2) % 180 === 0) {
        appendAgentLog("Warning: Observer bearings are parallel or anti-parallel. Triangulation will fail.", "error");
        issues++;
      }

      // 2. Check Leaflet / Map Instance
      if (typeof map === 'undefined' || !map) {
        appendAgentLog("Notice: Map instance not initialized yet.", "error");
        issues++;
      } else {
        appendAgentLog("Map engine: Online and attached.", "success");
      }

      // 3. Check Input String
      const rawText = document.getElementById('blockInput')?.value;
      if (!rawText) {
        appendAgentLog("Notice: Block input payload is currently empty.", "info");
      } else {
        appendAgentLog(`Payload active: ${rawText.length} characters loaded.`, "success");
      }

      if (issues === 0) {
        appendAgentLog("Diagnostic complete: All suite parameters optimal.", "success");
      }
    }
"""

if 'function toggleAgentDrawer()' not in html:
    html = html.replace('</script>', agent_js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] AI Assistant drawer & equation solver added to index.html!")
