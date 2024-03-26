import {updateStickyAddToCartBtnIfExists} from "../shop/stickyAddToCart";
import {parseLocaleNumber} from "../../utils/numberFormatter";

const mainProduct = document.querySelector('.mainProduct');
const chosenVariationTextContainer = document.querySelector('#chosenVariationTextContainer');
let variationPriceContainer = document.querySelector('#variation__priceContainer');
let chooseVariationBanner = document.querySelector('#chooseVariationBanner');
let moneySavedEl = document.querySelector('#productMisc__moneySaved');
let percentageSavedEl = document.querySelector('#productMisc__percentageSaved');
let salePriceEl = document.querySelector('#productMisc__salePrice');
let regularPriceEl = document.querySelector('#productMisc__regularPrice');


function updatePrices(el) {
  let currentSalePrice = el.getAttribute('data-attribute-sale-price');
  let currentRegularPrice = el.getAttribute('data-attribute-regular-price');
  let currentMoneySaved = parseInt(currentRegularPrice) - parseInt(currentSalePrice);
  let currentPercentageSaved = Math.round((currentMoneySaved / currentRegularPrice) * 100);

  moneySavedEl.textContent = currentMoneySaved;
  salePriceEl.textContent = currentSalePrice;
  regularPriceEl.textContent = currentRegularPrice;
  percentageSavedEl.textContent = currentPercentageSaved;

  if (variationPriceContainer.classList.contains('hidden')) {
    variationPriceContainer.classList.remove('hidden');
    chooseVariationBanner.classList.add('hidden');
  }
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