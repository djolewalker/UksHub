// Close notification
document
  .getElementById("hub-notification-panel-button")
  .addEventListener("click", function () {
    document.getElementById("hub-notification-panel").remove();
  });