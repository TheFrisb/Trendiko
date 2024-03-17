import {initializeToggles} from "../components/toggles/toggles";
import {initProductPageMainSlider} from "../components/sliders/productPageMainSlider";
import {initializeAddToCartButtons} from "../components/shop/addToCart";
import {initializeQuantityActions} from "../components/shop/quantityInput";
import {initializeCart} from "../components/shop/cart";
import {initializeProductAttributesListeners} from "../components/product-attributes/attribute";
import {initializeFAQItems} from "../components/faq/faq";
import {autoCompleteJS, initCheckoutCityListeners} from "../components/checkout/cityAutoComplete";
import {initializeAddToOrderButtons} from "../components/shop/addToOrder";
import {makeCountDownByMinutesAndSeconds} from "../components/timer/timer";

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
  const menuIcon = document.getElementById('menuIcon');
  const navbar = document.getElementById('navbar');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  menuIcon.addEventListener('click', function () {
    navbar.classList.toggle('hidden');
  });
});