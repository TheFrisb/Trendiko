import {HTTP, URLS} from "../../http/client";
import {isSideCartActive, toggleCheckout, toggleSideCart, updateCart} from "./cart";

function addToCart(product_id, product_type, quantity, isBuyNow) {
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
      updateCart(data);
      if (!isSideCartActive() && !isBuyNow) {
        toggleSideCart();
      } else if (isBuyNow) {
        toggleCheckout();
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
      addToCart(product_id, product_type, quantity, button.classList.contains('buyNowButton'));
    });
  });
}

export {initializeAddToCartButtons};