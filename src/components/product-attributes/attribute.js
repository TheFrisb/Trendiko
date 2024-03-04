const mainProduct = document.querySelector('.mainProduct');

function chooseAttribute(el, attributesContainer, addToCartButtons) {
  const attributeId = el.getAttribute('data-attribute-id');
  addToCartButtons.forEach(function (button) {
    button.setAttribute('data-attribute-id', attributeId);
  });

  attributesContainer.querySelectorAll('.productAttribute').forEach(function (attribute) {
    if (attribute !== el) {
      attribute.classList.remove('selected');
    }
  });

  el.classList.add('selected');
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