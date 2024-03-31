import {FACEBOOK_PIXEL_EVENTS_URLS, HTTP} from "../../http/client";

function sendInitiateCheckoutFacebookPixelEvent() {
  HTTP.post(FACEBOOK_PIXEL_EVENTS_URLS.INITIATE_CHECKOUT, {});
}

function sendViewContentFacebookPixelEvent() {

  const urls = window.location.href.split('/');

  if (urls.includes('product')) {
    let slug = urls[urls.length - 2];
    HTTP.post(`${FACEBOOK_PIXEL_EVENTS_URLS.VIEW_CONTENT}${slug}/`, {});
  }

  
}

export {sendInitiateCheckoutFacebookPixelEvent, sendViewContentFacebookPixelEvent};