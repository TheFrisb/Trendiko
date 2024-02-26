import {getCsrfToken} from "../utils/csrf";

let INTERNAL_API_BASE_PATH = "/api";

const URLS = {
  'ADD_TO_CART': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'UPDATE_CART_ITEM_QUANTITY': INTERNAL_API_BASE_PATH + '/cart/cart-item/', // Takes PK of cart item
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
}

export {HTTP, URLS};

