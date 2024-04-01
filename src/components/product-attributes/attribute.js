import {updateStickyAddToCartBtnIfExists} from "../shop/stickyAddToCart";
import {formatNumberToLocale, parseLocaleNumber} from "../../utils/numberFormatter";

const mainProduct = document.querySelector('.mainProduct');
const chosenVariationTextContainer = document.querySelector('#chosenVariationTextContainer');
let moneySavedEl = document.querySelector('#productMisc__moneySaved');
let percentageSavedEl = document.querySelector('#productMisc__percentageSaved');
let salePriceEl = document.querySelector('#productMisc__salePrice');
let regularPriceEl = document.querySelector('#productMisc__regularPrice');
// let variationPriceContainer = document.querySelector('#variation__priceContainer');
// let chooseVariationBanner = document.querySelector('#chooseVariationBanner');

function updatePrices(el) {
  let currentSalePrice = parseLocaleNumber(el.getAttribute('data-attribute-sale-price'));
  let currentRegularPrice = parseLocaleNumber(el.getAttribute('data-attribute-regular-price'));
  let currentMoneySaved = currentRegularPrice - currentSalePrice;
  let currentPercentageSaved = Math.round((currentMoneySaved / currentRegularPrice) * 100);

  moneySavedEl.textContent = formatNumberToLocale(currentMoneySaved);
  salePriceEl.textContent = formatNumberToLocale(currentSalePrice);
  regularPriceEl.textContent = formatNumberToLocale(currentRegularPrice);
  percentageSavedEl.textContent = formatNumberToLocale(currentPercentageSaved);

  // if (variationPriceContainer.classList.contains('hidden')) {
  //   variationPriceContainer.classList.remove('hidden');
  //   chooseVariationBanner.classList.add('hidden');
  // }
}

function updateUI(el, attributesContainer, chosenVariationText) {
  attributesContainer.querySelectorAll('.productAttribute').forEach(function (attribute) {
    if (attribute !== el) {
      attribute.classList.remove('selected');
    }
  });

  el.classList.add('selected');
  chosenVariationTextContainer.textContent = chosenVariationText;
  updatePrices(el);
}

function chooseAttribute(el, attributesContainer, addToCartButtons) {
  const attributeId = el.getAttribute('data-attribute-id');
  const price = parseLocaleNumber(el.getAttribute('data-attribute-sale-price'));
  const chosenVariationText = el.getAttribute('data-attribute-name');
  addToCartButtons.forEach(function (button) {
    button.setAttribute('data-attribute-id', attributeId);
  });

  updateStickyAddToCartBtnIfExists(price, null, attributeId);

  updateUI(el, attributesContainer, chosenVariationText);
}

function initializeProductAttributesListeners() {
  let attributesContainer = null;
  let addToCartButtons = null;
  if (mainProduct) {
    attributesContainer = mainProduct.querySelector('.productAttributesContainer');
    addToCartButtons = mainProduct.querySelectorAll('.addToCartButton');
  }

  if (attributesContainer) {
    const attributes = attributesContainer.querySelectorAll('.productAttribute');
    attributes.forEach(function (attribute) {
      attribute.addEventListener('click', function () {
        chooseAttribute(attribute, attributesContainer, addToCartButtons);
      });
    });
  }
}

export {initializeProductAttributesListeners};