/** @format */
//open-modal.js

// Display Popup Modal after "Clicking the Button"
function openModal(fileRef) {
  fetch(`/get-place-details?file_ref=${fileRef}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('detailsModalTitle').innerHTML = `${data.name}`;

      document.getElementById(
        'modalContent'
      ).innerHTML = `Place Name: ${data.name}<br>Address: ${data.address}`;

      // Now fetch images using the fileRef
      fetchImages(fileRef);

      // Set the value for place_id and modify the button based on visit status
      const visitButton = document.querySelector(
        "#detailsModal form button[type='submit']"
      );
      document.querySelector(
        "#detailsModal form input[name='place_id']"
      ).value = fileRef;
      if (data.visited) {
        visitButton.classList.remove('btn-outline-success');
        visitButton.classList.add('btn-success');
        visitButton.disabled = true;
        visitButton.textContent = '已打卡'; // "Already Checked In" or similar
      } else {
        visitButton.classList.remove('btn-success');
        visitButton.classList.add('btn-outline-success');
        visitButton.disabled = false;
        visitButton.textContent = '打卡'; // "Check In"
      }

      var modal = new bootstrap.Modal(document.getElementById('detailsModal'));
      modal.show();
    })
    .catch((error) => console.error('Error fetching place details:', error));
}

//Handle "Check" Action
document
  .getElementById('visitForm')
  .addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const place_id = document.querySelector(
      "#detailsModal form input[name='place_id']"
    ).value;

    fetch('/add-visit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ place_id: place_id }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        displayAlert('Visit added successfully!', 'success');
        confetti();
        // Close the modal
        var modal = bootstrap.Modal.getInstance(
          document.getElementById('detailsModal')
        );
        modal.hide();
      })
      .catch((error) => {
        console.error('Error:', error);
        displayAlert(
          'Error submitting your request. Please try again.',
          'danger'
        );
      });
  });

// Function to fetch and display images related to the place
function fetchImages(fileRef) {
  const imageUrl = `http://localhost:5001/fetch-images?fileRef=${fileRef}`;
  fetch(imageUrl)
    .then((response) => response.json())
    .then((imageData) => {
      // Assuming imageData is an array of URLs
      const imagesContainer = document.getElementById('modalContent');
      imageData.forEach((url) => {
        const img = document.createElement('img');
        img.src = url;
        img.style.width = '100%'; // Adjust styling as needed
        imagesContainer.appendChild(img);
      });
    })
    .catch((error) => {
      console.error('Error fetching images:', error);
      // Optionally handle the error in UI, e.g., show an error alert
    });
}
