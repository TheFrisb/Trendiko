import {HTTP} from "../../http/client";
import {ADMIN_URLS} from "../../http/adminURLS";
import {notyf__long} from "../../utils/error";

const changeOrderButtons = document.querySelectorAll('.changeOrderStatus');

function changeOrderStatus(event) {
  const button = event.target;
  const orderId = button.dataset.orderId;
  const newStatus = button.dataset.changeToStatus;

  // stringify the data
  const data = {
    order_id: orderId,
    new_status: newStatus
  }

  HTTP.post(ADMIN_URLS.CHANGE_ORDER_STATUS, data).then(response => {
    const data = response.data;
    console.log(data)
    console.log(response)
    if (response.success) {
      const tableRow = button.closest('tr');
      tableRow.remove();
    } else {
      notyf__long.error('Error: ' + response.data);
    }
  });
}

function initializeChangeOrderStatusButtons() {
  changeOrderButtons.forEach((button) => {
    button.addEventListener('click', changeOrderStatus);
  });
}

export {initializeChangeOrderStatusButtons};