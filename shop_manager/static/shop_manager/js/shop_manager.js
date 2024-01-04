document.addEventListener('DOMContentLoaded', function() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const changeOrderButtons = document.querySelectorAll('.changeOrderStatus');

  changeOrderButtons.forEach((button) => {
    button.addEventListener('click', changeOrderStatus);
  });

  /**
   * @param {Event} event
   */
  function changeOrderStatus(event) {
    const button = event.target;
    const orderId = button.dataset.orderId;
    const newStatus = button.dataset.changeToStatus;
    const url = `http://127.0.0.1:8000/shop-manager/api/change-order-status/`;

    fetch(url, {
      method: 'POST',
      body: JSON.stringify({
        order_id: orderId,
        new_status: newStatus,
      }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    })
        .then((response) => {
          if (response.status === 204) {
            const tableRow = button.closest('tr');
            tableRow.remove();
          } else {
            return response.text().then((text) => {
              throw new Error(text || response.statusText);
            });
          }
        })
        .catch((error) => {
          alert('Error: ' + error.message);
        });
  }
});
