/** @format */

// Display bounds information for Debugging
function updateBounds() {
  var bounds = map.getBounds();
  var minLat = bounds.getSouthWest().lat;
  var minLng = bounds.getSouthWest().lng;
  var maxLat = bounds.getNorthEast().lat;
  var maxLng = bounds.getNorthEast().lng;

  // Update the UI with the current bounds
  var boundsInfo = ` Min Lat: ${minLat.toFixed(4)}, Min Long: ${minLng.toFixed(
    4
  )} <br> Max Lat: ${maxLat.toFixed(4)}, Max Long: ${maxLng.toFixed(4)}`;
  document.getElementById('boundsDisplay').innerHTML = boundsInfo;
}
// Update bounds on map load and on map movements
map.on('load moveend', updateBounds);
updateBounds(); // Also update on initial load
