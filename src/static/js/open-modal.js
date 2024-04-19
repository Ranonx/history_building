/** @format */

// Display Popup Modal after "Clicking the Button"
function openModal(fileRef) {
  fetch(`/get-place-details?file_ref=${fileRef}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('detailsModalTitle').innerHTML = `${data.name}`;

      document.getElementById(
        'modalContent'
      ).innerHTML = `Place Name: ${data.name}<br>Address: ${data.address}`;

      document.querySelector(
        "#detailsModal form input[name='place_id']"
      ).value = fileRef;
      var modal = new bootstrap.Modal(document.getElementById('detailsModal'));
      modal.show();
    })
    .catch((error) => console.error('Error fetching place details:', error));
}
