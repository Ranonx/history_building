/** @format */

//Generate Map using Leaflet.js
var map = L.map('map').setView([22.2964, 114.1795], 13);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

//Brief Location Info Popup
L.geoJSON(geojsonData)
  .bindPopup(function (layer) {
    return `<b>${layer.feature.properties.NAME_TC}</b><br>
    ${layer.feature.properties.NAME}<br>
    <div class="row justify-content-center">
    <button class='btn btn-outline-info' onclick="openModal('${layer.feature.properties.FILE_REF}')">Open</button>
    </div>`;
  })
  .addTo(map);
