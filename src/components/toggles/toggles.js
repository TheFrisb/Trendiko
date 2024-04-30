function initializeToggles(hideAllOnClick = false) {
  const toggles = document.querySelectorAll('.toggle');
  const toggle_contents = document.querySelectorAll('.canBeToggled');

  toggles.forEach(function (toggle) {
    toggle.addEventListener('click', function (e) {


      // Display the content section associated with the clicked toggle
      const contentId = toggle.getAttribute('data-content-id');
      const content = document.getElementById(contentId);
      content.classList.toggle('hidden');

      if (toggle.classList.contains('active')) {
        toggle.classList.remove('active');
        const icon = toggle.querySelector('.toggle-icon');
        icon.textContent = '+';
        return;
      }


      if (hideAllOnClick) {
        toggle_contents.forEach(function (content) {
          content.classList.add('hidden');
        });
        toggles.forEach(function (toggle) {
          const icon = toggle.querySelector('.toggle-icon');
          icon.textContent = '+';
          toggle.classList.remove('active');
        });
      }

      const icon = toggle.querySelector('.toggle-icon');
      icon.textContent = '-';
      toggle.classList.toggle('active');
    });
  });
}

export {initializeToggles};