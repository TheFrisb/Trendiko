import {HTTP} from "../../http/client";
import {ADMIN_URLS} from "../../http/adminURLS";
import {notyf__long} from "../../utils/error";

const removeAbandonedCartButtons = document.querySelectorAll('.removeAbandonedCartBtn');

function removeAbandonedCart(event) {
  const button = event.target;
  const cartId = button.dataset.cartId;

  // stringify the data
  const data = {
    cart_id: cartId
  }

  HTTP.post(ADMIN_URLS.REMOVE_ABANDONED_CART, data).then(response => {
    const data = response.data;
    if (response.success) {
      const tableRow = button.closest('tr');
      tableRow.remove();
      notyf__long.success("Кошничката е избришана");
    } else {
      notyf__long.error(response.data.message);
    }
  });
}

function initializeRemoveAbandonedCartButtons() {
  removeAbandonedCartButtons.forEach((button) => {
    button.addEventListener('click', removeAbandonedCart);
  });
}

export {initializeRemoveAbandonedCartButtons};