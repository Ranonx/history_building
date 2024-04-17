/** @format */

var map = L.map('map').setView([22.2964, 114.1795], 13);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

L.geoJSON(geojsonData)
  .bindPopup(function (layer) {
    return layer.feature.properties.NAME;
  })
  .addTo(map);
