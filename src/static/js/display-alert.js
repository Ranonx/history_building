/** @format */

// Display alert information for Debugging
function displayAlert(message, type) {
  const alertPlaceholder = document.getElementById('alertPlaceholder');
  const alert = `<div class="alert alert-${type}" role="alert">${message}</div>`;
  alertPlaceholder.innerHTML = alert;
  // Optionally, remove the alert after some time
  setTimeout(() => {
    alertPlaceholder.innerHTML = '';
  }, 5000); // Removes the alert after 5 seconds
}
