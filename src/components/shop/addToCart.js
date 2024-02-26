import {HTTP, URLS} from "../../http/client";
import {toggleSideCart, updateSideCart} from "./sideCart";

function addToCart(product_id, product_type, quantity) {
  const data = {
    product_id: product_id,
    product_type: product_type,
    quantity: quantity
  }
  // await the response from the server
  HTTP.post(URLS.ADD_TO_CART, data).then(response => {
    // see if response is successful
    const data = response.data;
    if (response.success) {
      updateSideCart(data);
      toggleSideCart();
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
      addToCart(product_id, product_type, quantity);
    });
  });
}

export {initializeAddToCartButtons};