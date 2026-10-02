with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert Map HTML Container and CSS
map_ui = """
      <div class="encoder-card full-width" style="margin-top: 15px;">
        <label>Live Tactical Map View</label>
        <div id="map" style="height: 400px; width: 100%; border-radius: 8px; margin-top: 8px; border: 1px solid var(--border);"></div>
      </div>
"""

if 'id="map"' not in html:
    html = html.replace('<pre id="triangulateOut">Awaiting calculation...</pre>', 
                        '<pre id="triangulateOut">Awaiting calculation...</pre>' + map_ui)

# 2. Add Google Maps Initialization and Overlay Logic
maps_js = """
    let map, obs1Marker, obs2Marker, targetMarker, line1, line2;

    function initMap() {
      const defaultCenter = { lat: 38.8936, lng: -77.0359 };
      map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: defaultCenter,
        mapTypeId: "hybrid",
      });
      runTriangulation();
    }

    function updateMapMarkers(lat1, lon1, brng1, lat2, lon2, brng2, targetLat, targetLon) {
      if (!map) return;

      const p1 = { lat: lat1, lng: lon1 };
      const p2 = { lat: lat2, lng: lon2 };
      const pTarget = { lat: parseFloat(targetLat), lng: parseFloat(targetLon) };

      if (obs1Marker) obs1Marker.setMap(null);
      if (obs2Marker) obs2Marker.setMap(null);
      if (targetMarker) targetMarker.setMap(null);
      if (line1) line1.setMap(null);
      if (line2) line2.setMap(null);

      obs1Marker = new google.maps.Marker({ position: p1, map, title: "Observer 1", label: "O1" });
      obs2Marker = new google.maps.Marker({ position: p2, map, title: "Observer 2", label: "O2" });
      targetMarker = new google.maps.Marker({ position: pTarget, map, title: "Triangulated Target", label: "T" });

      line1 = new google.maps.Polyline({
        path: [p1, pTarget],
        geodesic: true,
        strokeColor: "#00F2FE",
        strokeOpacity: 0.9,
        strokeWeight: 3
      });
      line2 = new google.maps.Polyline({
        path: [p2, pTarget],
        geodesic: true,
        strokeColor: "#4FACFE",
        strokeOpacity: 0.9,
        strokeWeight: 3
      });

      line1.setMap(map);
      line2.setMap(map);

      const bounds = new google.maps.LatLngBounds();
      bounds.extend(p1);
      bounds.extend(p2);
      bounds.extend(pTarget);
      map.fitBounds(bounds);
    }
"""

if 'function initMap()' not in html:
    html = html.replace('function runTriangulation() {', maps_js + '\n    function runTriangulation() {')
    html = html.replace("document.getElementById('triangulateOut').innerText = \n        `Target Lat: ${resLat}°\\nTarget Lon: ${resLon}°\\nStatus: Intersected`;",
                        "document.getElementById('triangulateOut').innerText = \n        `Target Lat: ${resLat}°\\nTarget Lon: ${resLon}°\\nStatus: Intersected`;\n      updateMapMarkers(lat1, lon1, brng1, lat2, lon2, brng2, resLat, resLon);")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[✓] Google Maps module successfully integrated into index.html!")
