document.addEventListener("DOMContentLoaded", function () {
  const inlineContainer = document.getElementById('attributes-group'); // Adjust the ID to match the container of your inline forms

  function toggleFields(row) {
    var typeSelect = row.querySelector('.field-type select');
    var contentField = row.querySelector('.field-content');
    var colorField = row.querySelector('.field-color');

    if (typeSelect && contentField && colorField) { // Check if elements exist
      if (typeSelect.value === 'color') {
        contentField.style.display = 'none'; // Hide the content field for color type
        colorField.style.display = '';       // Show the color field
      } else {
        contentField.style.display = '';     // Show the content field for other types
        colorField.style.display = 'none';   // Hide the color field
      }
    }
  }

  // Event delegation for handling changes in the type select dropdown
  inlineContainer.addEventListener('change', function (event) {
    if (event.target.matches('.field-type select')) { // Check if the changed element is a type select
      const row = event.target.closest('.dynamic-attributes'); // Find the closest row
      toggleFields(row);
    }
  });

  // Initial application of toggleFields to existing rows
  document.querySelectorAll('.dynamic-attributes').forEach(function (row) {
    toggleFields(row);
  });
});
