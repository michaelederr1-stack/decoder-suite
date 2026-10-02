import re

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Triangulation Panel UI into HTML before the script tag
geo_panel = """
    <div class="panel full-width">
      <h2>NATO MGRS & Geo-Triangulation Engine</h2>
      <div class="grid-encoders">
        <div class="encoder-card">
          <label>Observer 1 (Lat, Lon, Bearing°)</label>
          <div style="display: flex; gap: 8px; margin-top: 6px;">
            <input type="number" id="obs1_lat" value="38.8977" step="any" placeholder="Lat">
            <input type="number" id="obs1_lon" value="-77.0365" step="any" placeholder="Lon">
            <input type="number" id="obs1_brng" value="45" step="any" placeholder="Azimuth°">
          </div>
        </div>
        <div class="encoder-card">
          <label>Observer 2 (Lat, Lon, Bearing°)</label>
          <div style="display: flex; gap: 8px; margin-top: 6px;">
            <input type="number" id="obs2_lat" value="38.8895" step="any" placeholder="Lat">
            <input type="number" id="obs2_lon" value="-77.0353" step="any" placeholder="Lon">
            <input type="number" id="obs2_brng" value="315" step="any" placeholder="Azimuth°">
          </div>
        </div>
        <div class="encoder-card">
          <label>Triangulated Target Output</label>
          <pre id="triangulateOut">Awaiting calculation...</pre>
        </div>
      </div>
    </div>
"""

# Insert panel before </script> container wrapper end
if 'NATO MGRS & Geo-Triangulation Engine' not in html:
    html = html.replace('<script>', geo_panel + '\n  <script>')

# 2. Add JavaScript function for Spherical Triangulation
js_logic = """
    function runTriangulation() {
      const lat1 = parseFloat(document.getElementById('obs1_lat')?.value);
      const lon1 = parseFloat(document.getElementById('obs1_lon')?.value);
      const brng1 = parseFloat(document.getElementById('obs1_brng')?.value);
      const lat2 = parseFloat(document.getElementById('obs2_lat')?.value);
      const lon2 = parseFloat(document.getElementById('obs2_lon')?.value);
      const brng2 = parseFloat(document.getElementById('obs2_brng')?.value);

      if ([lat1, lon1, brng1, lat2, lon2, brng2].some(isNaN)) {
        document.getElementById('triangulateOut').innerText = 'Enter valid coordinates and azimuth angles.';
        return;
      }

      const toRad = deg => (deg * Math.PI) / 180;
      const toDeg = rad => (rad * 180) / Math.PI;

      const phi1 = toRad(lat1), lam1 = toRad(lon1);
      const phi2 = toRad(lat2), lam2 = toRad(lon2);
      const theta13 = toRad(brng1), theta23 = toRad(brng2);

      const dPhi = phi2 - phi1;
      const dLam = lam2 - lam1;

      const delta12 = 2 * Math.asin(Math.sqrt(
        Math.sin(dPhi / 2) ** 2 + Math.cos(phi1) * Math.cos(phi2) * Math.sin(dLam / 2) ** 2
      ));

      if (delta12 === 0) {
        document.getElementById('triangulateOut').innerText = 'Error: Observer positions are identical.';
        return;
      }

      const thetaA = Math.acos((Math.sin(phi2) - Math.sin(phi1) * Math.cos(delta12)) / (Math.sin(delta12) * Math.cos(phi1)));
      const thetaB = Math.acos((Math.sin(phi1) - Math.sin(phi2) * Math.cos(delta12)) / (Math.sin(delta12) * Math.cos(phi2)));

      const theta12 = Math.sin(lam2 - lam1) > 0 ? thetaA : 2 * Math.PI - thetaA;
      const theta21 = Math.sin(lam2 - lam1) > 0 ? 2 * Math.PI - thetaB : thetaB;

      const alpha1 = (theta13 - theta12 + Math.PI) % (2 * Math.PI) - Math.PI;
      const alpha2 = (theta21 - theta23 + Math.PI) % (2 * Math.PI) - Math.PI;

      if (Math.sin(alpha1) === 0 && Math.sin(alpha2) === 0) {
        document.getElementById('triangulateOut').innerText = 'Infinite / parallel lines of bearing.';
        return;
      }

      const alpha3 = Math.acos(-Math.cos(alpha1) * Math.cos(alpha2) + Math.sin(alpha1) * Math.sin(alpha2) * Math.cos(delta12));
      const delta13 = Math.atan2(Math.sin(delta12) * Math.sin(alpha1) * Math.sin(alpha2), Math.cos(alpha2) + Math.cos(alpha1) * Math.cos(alpha3));

      const phi3 = Math.asin(Math.sin(phi1) * Math.cos(delta13) + Math.cos(phi1) * Math.sin(delta13) * Math.cos(theta13));
      const dLam13 = Math.atan2(Math.sin(theta13) * Math.sin(delta13) * Math.cos(phi1), Math.cos(delta13) - Math.sin(phi1) * Math.sin(phi3));
      const lam3 = lam1 + dLam13;

      const resLat = toDeg(phi3).toFixed(6);
      const resLon = (((toDeg(lam3) + 540) % 360) - 180).toFixed(6);

      document.getElementById('triangulateOut').innerText = 
        `Target Lat: ${resLat}°\nTarget Lon: ${resLon}°\nStatus: Intersected`;
    }
"""

if 'runTriangulation' not in html:
    html = html.replace('function processAll() {', js_logic + '\n    function processAll() {')
    html = html.replace('processAll();', 'processAll();\n      runTriangulation();')

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Triangulation engine updated and injected into index.html successfully!")
