import {HTTP, URLS} from "../../http/client";
import {removeCartItemElement, updateCart} from "./cart";
import {notyf__short} from "../../utils/error";
import {parseLocaleNumber} from "../../utils/numberFormatter";

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
  HTTP.put(URLS.UPDATE_CART_ITEM_QUANTITY + `${parseLocaleNumber(pk)}/`, {quantity: parseLocaleNumber(quantity)}).then(response => {
    const data = response.data;
    if (response.success) {
      updateCart(data);
    } else {
      let status_code = response.status;
      if (status_code === 403) {
        notyf__short.error(data.message);
      }
    }
  });

  return quantity;
}

function removeCartItem(pk) {
  HTTP.delete(`${URLS.REMOVE_CART_ITEM}${parseLocaleNumber(pk)}`).then(response => {
    if (response) {
      removeCartItemElement(pk, response.data.has_free_shipping);
    }
  });

}

function attachProductInputListeners(inputEl) {
  // find closest .productDataContainer
  let productDataContainer = inputEl.closest('.productDataContainer');
  let addToCartButtons = productDataContainer.querySelectorAll('.addToCartButton');
  let incrementButton = inputEl.nextElementSibling;
  let decrementButton = inputEl.previousElementSibling;

  function updateAddToCartButtons(quantity) {
    addToCartButtons.forEach(function (button) {
      button.setAttribute('data-quantity', quantity);
    });

    // updateStickyAddToCartBtnIfExists(null, quantity)
  }


  incrementButton.addEventListener('click', function () {
    let quantity = parseLocaleNumber(inputEl.value)
    quantity = updateQuantity(ACTION_TYPES.INCREMENT, quantity);
    inputEl.value = quantity;
    updateAddToCartButtons(quantity);
  });
  decrementButton.addEventListener('click', function () {
    let quantity = parseLocaleNumber(inputEl.value)
    quantity = updateQuantity(ACTION_TYPES.DECREMENT, quantity);
    inputEl.value = quantity;
    updateAddToCartButtons(quantity);
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

function attachOrderItemInputListeners(inputEl) {
  let incrementButton = inputEl.nextElementSibling;
  let decrementButton = inputEl.previousElementSibling;
  let addToOrderButton = inputEl.closest('.orderItem').querySelector('.addToOrderButton');

  incrementButton.addEventListener('click', function () {
    let quantity = parseInt(inputEl.value) + 1;
    inputEl.value = quantity;
    addToOrderButton.setAttribute('data-quantity', quantity);

  });
  decrementButton.addEventListener('click', function () {
    let quantity = parseInt(inputEl.value) - 1;
    if (quantity < 1) {
      quantity = 1;
    }
    inputEl.value = quantity;
    addToOrderButton.setAttribute('data-quantity', quantity);
  });

}

function initializeQuantityActions() {
  let productInputs = document.querySelectorAll('.quantityInput');
  productInputs.forEach(function (input) {
    attachProductInputListeners(input);
  });

  let cartItemInputs = document.querySelectorAll('.cartItem__quantityInput');
  cartItemInputs.forEach(function (input) {
    attachCartItemInputListeners(input);
  });

  let orderItemInputs = document.querySelectorAll('.orderItem__quantityInput');
  orderItemInputs.forEach(function (input) {
    attachOrderItemInputListeners(input);
  });

  let removeCartItemButtons = document.querySelectorAll('.cartItem__removeItem');

  removeCartItemButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      const pk = button.closest('.cartItem').getAttribute('data-cart-item-id');
      removeCartItem(pk);
    });
  });


}

export {initializeQuantityActions, attachCartItemInputListeners, removeCartItem};