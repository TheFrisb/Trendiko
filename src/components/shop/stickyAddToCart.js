import {formatNumberToLocale} from "../../utils/numberFormatter";

const stickyAddToCartContainer = document.querySelector('#stickyAddToCartContainer');
const stickyAddToCartBtn = document.querySelector('#stickyAddToCartButton');
let quantityContainer = document.querySelector('#stickyAddToCartContainer__quantityHolder');
let priceContainer = document.querySelector('#stickyAddToCartContainer__currentPrice');

function stickyAddToCartExists() {
  return stickyAddToCartContainer !== null;
}

function updateStickyAddToCartBtnIfExists(price = null, quantity = null, attributeId = null, hide = false) {
  if (!stickyAddToCartExists()) {
    return;
  }
  if (quantity) {
    stickyAddToCartBtn.setAttribute('data-quantity', quantity);
    quantityContainer.innerHTML = formatNumberToLocale(quantity) + 'x';
  }
  if (attributeId) {
    stickyAddToCartBtn.setAttribute('data-attribute-id', attributeId);
  }
  if (price) {
    priceContainer.textContent = price;
  }

  if (hide) {
    stickyAddToCartContainer.classList.add('hidden');
  } else {
    stickyAddToCartContainer.classList.remove('hidden');
  }
}

export {
  updateStickyAddToCartBtnIfExists,
};