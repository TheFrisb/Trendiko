function initializeToggles() {
  const toggles = document.querySelectorAll('.toggle');
  const toggle_contents = document.querySelectorAll('.canBeToggled');

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
}

export {initializeToggles};