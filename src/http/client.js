import {getCsrfToken} from "../utils/csrf";

let INTERNAL_API_BASE_PATH = "/api";
let FACEBOOK_PIXEL_EVENTS_URL = INTERNAL_API_BASE_PATH + "/facebook/pixel"

const URLS = {
  'ADD_TO_CART': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'ADD_CART_OFFER': INTERNAL_API_BASE_PATH + '/cart/cart-offer/',
  'UPDATE_CART_ITEM_QUANTITY': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'REMOVE_CART_ITEM': INTERNAL_API_BASE_PATH + '/cart/cart-item/',
  'CHECKOUT': INTERNAL_API_BASE_PATH + '/cart/checkout/',
  'ADD_TO_ORDER': INTERNAL_API_BASE_PATH + '/cart/order-item/',
  'ABANDONED_CART_DETAILS': INTERNAL_API_BASE_PATH + '/cart/abandoned-cart-details/',

  'SUBSCRIBE_TO_MAIL': INTERNAL_API_BASE_PATH + '/common/mail-subscription/',
}

const FACEBOOK_PIXEL_EVENTS_URLS = {
  'INITIATE_CHECKOUT': FACEBOOK_PIXEL_EVENTS_URL + '/initiate-checkout/',
  'VIEW_CONTENT': FACEBOOK_PIXEL_EVENTS_URL + '/view-content/',
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
    let responseData = null;
    if (response.status !== 204) {
      responseData = await response.json();
    }
    return {
      success: response.ok,
      status: response.status,
      data: responseData
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
  },

  get: async (url) => {
    const response = await fetch(url);
    return {
      success: response.ok,
      status: response.status,
      data: await response.json()
    }
  }
}

export {HTTP, URLS, FACEBOOK_PIXEL_EVENTS_URLS};

