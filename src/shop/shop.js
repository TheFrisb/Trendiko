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