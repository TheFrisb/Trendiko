import {initializeToggles} from "../components/toggles/toggles";
import {initProductPageMainSlider} from "../components/sliders/productPageMainSlider";
import {initializeAddToCartButtons} from "../components/shop/addToCart";
import {initializeQuantityActions} from "../components/shop/quantityInput";
import {initializeCart} from "../components/shop/cart";
import {initializeProductAttributesListeners} from "../components/product-attributes/attribute";
import {initializeFAQItems} from "../components/faq/faq";
import {initCheckoutCityListeners} from "../components/checkout/cityAutoComplete";
import {initializeAddToOrderButtons} from "../components/shop/addToOrder";
import {makeCountDownByMinutesAndSeconds} from "../components/timer/timer";
import {initializeCookieConsent} from "../components/cookies/cookieconsent-config";
import {initializeSearchBar} from "../components/searchBar";
import {sendViewContentFacebookPixelEvent} from "../components/facebook/pixelEvents";
import {initializeSubscribeToMailButtons} from "../components/promotions/subscribeToMailButton";
import {initializeAbandonedCart} from "../components/abandonedCart";

document.addEventListener('DOMContentLoaded', function () {
  initializeToggles();
  initProductPageMainSlider();
  initializeAddToCartButtons();
  initializeQuantityActions();
  initializeCart();
  initializeProductAttributesListeners();
  initializeFAQItems();
  initializeAddToOrderButtons();
  makeCountDownByMinutesAndSeconds();
  initCheckoutCityListeners();
  initializeCookieConsent();
  initializeSearchBar();
  sendViewContentFacebookPixelEvent();
  initializeSubscribeToMailButtons();
  initializeAbandonedCart();
  const menuIcon = document.getElementById('menuIcon');
  const navbar = document.getElementById('navbar');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  menuIcon.addEventListener('click', function () {
    navbar.classList.toggle('hidden');
  });
});