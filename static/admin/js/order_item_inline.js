/*
    On document load, in the order item inline formset, for each order item inline, add event listener on product or attribute change, and fetch the price of the product and attribute from the server and update the price input field.

 */


function fetchProductPrice(row) {
  const productSelect = row.querySelector('.field-product select');
  const priceInput = row.querySelector('.field-price input');

  const productId = productSelect.value;

  if (productId === '' || productId === null) {
    return;
  }

  fetch(`/api/products/${productId}/`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      priceInput.value = data.sale_price;
      priceInput.setAttribute('data-current-selected-price', data.sale_price);
    })
    .catch((error) => {
      console.error(error);
    });
}

function fetchAttributePrice(row) {
  const attributeSelect = row.querySelector('.field-attribute select');
  const priceInput = row.querySelector('.field-price input');

  if (attributeSelect.value === '' || attributeSelect.value === null) {
    return;
  }
  const attributeId = attributeSelect.value;

  fetch(`/api/product-attributes/${attributeId}/`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      priceInput.value = data.sale_price;
      priceInput.setAttribute('data-current-selected-price', data.sale_price);
    })
    .catch((error) => {
      console.error(error);
    });
}

function updateDiscount(row) {
  const priceInput = row.querySelector('.field-price input');
  const discountInput = row.querySelector('.field-rabat input');

  if (priceInput.value === '' || priceInput.value === null) {
    return;
  }

  if (discountInput.value === '' || discountInput.value === null) {
    discountInput.value = 0;
  }

  let currentPrice = parseInt(priceInput.getAttribute('data-current-selected-price'));
  let currentDiscountPercentage = parseInt(discountInput.value);

  let discountAmount = (currentPrice * currentDiscountPercentage) / 100;

  let finalPrice = parseInt(currentPrice - discountAmount);

  priceInput.value = finalPrice;
}

window.addEventListener('load', function () {
    const formsetContainer = document.querySelector('#order_items-group');

    formsetContainer.onchange = function (event) {
      const row = event.target.closest('.dynamic-order_items');

      if (event.target.matches('.field-product select')) {
        fetchProductPrice(row);
      }

      if (event.target.matches('.field-attribute select')) {
        fetchAttributePrice(row);
      }

      if (event.target.matches('.field-rabat input')) {
        updateDiscount(row);
      }
    }
  }
);
