import {initializeToggles} from "../components/toggles/toggles";
import {initProductPageMainSlider} from "../components/sliders/productPageMainSlider";
import {initializeAddToCartButtons} from "../components/shop/addToCart";
import {initializeQuantityInput} from "../components/shop/quantityInput";
import {initializeSideCart} from "../components/shop/sideCart";

document.addEventListener('DOMContentLoaded', function () {
  initializeToggles();
  initProductPageMainSlider();
  initializeAddToCartButtons();
  initializeQuantityInput();
  initializeSideCart();
  const menuIcon = document.getElementById('menuIcon');
  const navbar = document.getElementById('navbar');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  menuIcon.addEventListener('click', function () {
    navbar.classList.toggle('hidden');
  });
});