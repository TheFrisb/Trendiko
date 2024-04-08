import {HTTP, URLS} from "../http/client";

const checkoutForm = document.getElementById("checkoutForm");

function debounce(fn, delay) {
  let timeoutId;
  console.log('debounce')
  return function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fn.apply(this, arguments);
    }, delay);
  };
}

function handleInputKeydown(event) {
  const input = event.target;
  const data = {
    [input.name]: input.value
  };

  console.log('handleInputKeydown', data)

  return HTTP.post(URLS.ABANDONED_CART_DETAILS, data)
}

function initializeAbandonedCart() {
  console.log('initializeAbandonedCart')
  let inputs = checkoutForm.querySelectorAll('input');
  console.log(inputs)
  inputs.forEach(input => {
    input.addEventListener('keydown', debounce(handleInputKeydown, 5000));
  });
}

export {initializeAbandonedCart};