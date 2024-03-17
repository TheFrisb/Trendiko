import {getCsrfToken} from "../utils/csrf";

let INTERNAL_API_BASE_PATH = "/api";

const URLS = {
  'ADD_TO_CART': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'UPDATE_CART_ITEM_QUANTITY': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'REMOVE_CART_ITEM': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'CHECKOUT': INTERNAL_API_BASE_PATH + '/cart/checkout/',
  'ADD_TO_ORDER': INTERNAL_API_BASE_PATH + '/cart/order-item/',
}

const HTTP = {
  post: async (url, data) => {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify(data),
    });
    return {
      success: response.ok,
      status: response.status,
      data: await response.json()
    }
  },

  put: async (url, data) => {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify(data),
    });
    return {
      success: response.ok,
      status: response.status,
      data: await response.json()
    }
  },

  delete: async (url) => {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      }
    });

    let data = null;

    if (response.status !== 204) {
      data = await response.json();
    }
    return {
      success: response.ok,
      status: response.status,
      data: data // This will be null in case of a 204 response
    }
  }
}

export {HTTP, URLS};

