import {HTTP, URLS} from "../../http/client";
import {isSideCartActive, toggleCheckout, toggleSideCart, updateCart} from "./cart";
import {notyf__short} from "../../utils/error";

function addToCart(product_id, product_type, quantity, attributeId, isBuyNow) {
  if (attributeId === 'undefined' || attributeId === '') {
    attributeId = null;
  }
  const data = {
    product_id: product_id,
    attribute_id: attributeId,
    product_type: product_type,
    quantity: quantity,
  }

  if (product_type === 'variable' && !attributeId) {
    notyf__short.error('Одберете варијација на производот');
    return;
  }

  HTTP.post(URLS.ADD_TO_CART, data).then(response => {
    // see if response is successful
    const data = response.data;
    if (response.success) {
      updateCart(data);
      if (!isSideCartActive() && !isBuyNow) {
        toggleSideCart();
      } else if (isBuyNow) {
        toggleCheckout();
      }
    } else {
      let status_code = response.status;
      if (status_code === 403) {
        notyf__short.error(data.message);
      } else {
        notyf__short.error('Проблем со додавањето на продуктот во кошничка. Ве молиме обидете се повторно.');
      }
    }
  });
}

function initializeAddToCartButtons() {
  const addToCartButtons = document.querySelectorAll('.addToCartButton');
  addToCartButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      const product_id = button.getAttribute('data-product-id');
      const product_type = button.getAttribute('data-product-type');
      const quantity = button.getAttribute('data-quantity');
      const attributeId = button.getAttribute('data-attribute-id');
      const isBuyNow = button.classList.contains('buyNowButton');
      addToCart(product_id, product_type, quantity, attributeId, isBuyNow)
    });
  });
}

export {initializeAddToCartButtons};