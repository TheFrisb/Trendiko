document.addEventListener("DOMContentLoaded", function () {
  const inlineContainer = document.getElementById('attributes-group');
  console.log('loadded')

  function toggleFields(row) {
    var typeSelect = row.querySelector('.field-type select');
    var contentField = row.querySelector('.field-value input');

    if (typeSelect && contentField) {
      if (typeSelect.value === 'color') {
        contentField.type = 'color';
        // check if value is a color

        if (contentField.value && !contentField.value.match(/^#[0-9A-F]{6}$/i)) {
          contentField.value = '#000000';
        }
      } else {
        contentField.type = 'text';
        // check if value is a text
        if (contentField.value && contentField.value.match(/^#[0-9A-F]{6}$/i)) {
          contentField.value = '';
        }
      }
    }
  }

  // Event delegation for handling changes in the type select dropdown
  inlineContainer.addEventListener('change', function (event) {
    if (event.target.matches('.field-type select')) {
      const row = event.target.closest('.dynamic-attributes');
      toggleFields(row);
    }
  });

  // Initial application of toggleFields to existing rows
  const rows = inlineContainer.querySelectorAll('.form-row');
  rows.forEach(function (row) {
    console.log(row)
    toggleFields(row);
  });
});
