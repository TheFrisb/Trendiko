import {tns} from './tinySlider.js';

document.addEventListener('DOMContentLoaded', function () {
  const menuIcon = document.getElementById('menuIcon');
  const navbar = document.getElementById('navbar');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  menuIcon.addEventListener('click', function () {
    navbar.classList.toggle('hidden');
  });

  function addProductToCart(productId, productType, attributeId, quantity) {
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('product_type', productType);
    // formData.append('attribute_id', attributeId);
    formData.append('quantity', quantity);
    fetch('/api/cart/cart-item/', {
      method: 'POST',
      body: formData,
      contentType: 'application/json',
      headers: {
        'X-CSRFToken': csrftoken,
        'Accept': 'application/json',
      },

    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          const cartCount = document.getElementById('cartCount');
          cartCount.textContent = data.cartCount;
        } else {
          console.log(data)
          alert('Failed to add product to cart');
        }
      });
  }

  document.querySelectorAll('.addToCartButton').forEach(function (button) {
    button.addEventListener('click', function () {
      const productId = parseInt(button.getAttribute('data-product-id'));
      const productType = button.getAttribute('data-product-type');
      let attributeId = null
      const quantity = button.getAttribute('data-quantity');

      if (productType === 'variable') {
        attributeId = parseInt(button.getAttribute('data-attribute-id'));
        if (!attributeId || attributeId === 0) {
          alert('Please select an attribute');
          return;
        }

      }

      addProductToCart(productId, productType, attributeId, quantity);
    });
  });
})


document.addEventListener('DOMContentLoaded', function () {
  const productGalleryContainer = document.getElementById('productGalleryContainer');
  const toggles = document.querySelectorAll('.toggle');
  const toggle_contents = document.querySelectorAll('.canBeToggled');
  const addToCartButton = document.getElementById('addToCartButton');

  let slider = tns({
    container: '#productGallery',
    items: 1,
    slideBy: 1,
    autoplay: false,
    nav: false,

    controls: false,
    navAsThumbnails: false,
    mouseDrag: true,

  });

  toggles.forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      // Hide all content sections
      toggle_contents.forEach(function (content) {
        content.classList.add('hidden');
      });

      // Display the content section associated with the clicked toggle
      const contentId = toggle.getAttribute('data-content-id');
      const content = document.getElementById(contentId);
      content.classList.remove('hidden');

      // Update the toggle icons
      toggles.forEach(function (toggle) {
        const icon = toggle.querySelector('.toggle-icon');
        icon.textContent = '+';
        toggle.classList.remove('active');
      });
      const icon = toggle.querySelector('.toggle-icon');
      icon.textContent = '-';
      toggle.classList.add('active');
    });
  });

})