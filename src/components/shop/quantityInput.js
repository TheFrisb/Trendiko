import {HTTP, URLS} from "../../http/client";
import {updateSideCart} from "./sideCart";

const ACTION_TYPES = {
  INCREMENT: 'INCREMENT',
  DECREMENT: 'DECREMENT'
}

function updateQuantity(actionType, quantity) {
  if (actionType === ACTION_TYPES.INCREMENT) {
    quantity++;
  } else if (actionType === ACTION_TYPES.DECREMENT) {
    quantity--;
  }

  return quantity;
}

function updateCartItemQuantity(quantity, pk) {
  HTTP.put(URLS.UPDATE_CART_ITEM_QUANTITY + `${pk}/`, {quantity: quantity}).then(response => {
    const data = response.data;
    if (response.success) {
      updateSideCart(data);
    }
  });

  return quantity;
}

function attachProductInputListeners(inputEl) {
  // find closest .productDataContainer
  let productDataContainer = inputEl.closest('.productDataContainer');
  let addToCartButtons = productDataContainer.querySelectorAll('.addToCartButton');
  let incrementButton = inputEl.nextElementSibling;
  let decrementButton = inputEl.previousElementSibling;

  function updateAddToCartButtons() {
    addToCartButtons.forEach(function (button) {
      button.setAttribute('data-quantity', quantity);
    });
  }


  incrementButton.addEventListener('click', function () {
    let quantity = parseInt(inputEl.value);
    console.log("before increment", quantity)
    quantity = updateQuantity(ACTION_TYPES.INCREMENT, quantity);
    inputEl.value = quantity;
    updateAddToCartButtons();
  });
  decrementButton.addEventListener('click', function () {
    let quantity = parseInt(inputEl.value);
    quantity = updateQuantity(ACTION_TYPES.DECREMENT, quantity);
    inputEl.value = quantity;
    updateAddToCartButtons();
  });
}


function attachCartItemInputListeners(inputEl) {
  const pk = inputEl.closest('.cartItem').getAttribute('data-cart-item-id');
  let incrementButton = inputEl.nextElementSibling;
  let decrementButton = inputEl.previousElementSibling;
  incrementButton.addEventListener('click', function () {
    let quantity = parseInt(inputEl.value) + 1;
    updateCartItemQuantity(quantity, pk);
  });
  decrementButton.addEventListener('click', function () {
    let quantity = parseInt(inputEl.value) - 1;
    updateCartItemQuantity(quantity, pk);
  });
}

function initializeQuantityInput() {
  let productInputs = document.querySelectorAll('.quantityInput');
  productInputs.forEach(function (input) {
    attachProductInputListeners(input);
  });

  let cartItemInputs = document.querySelectorAll('.cartItem__quantityInput');
  cartItemInputs.forEach(function (input) {
    attachCartItemInputListeners(input);
  });
}

export {initializeQuantityInput};