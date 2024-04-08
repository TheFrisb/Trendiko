import {HTTP, URLS} from "../../http/client";
import {notyf__long} from "../../utils/error";


function checkout(formEl) {

  if (!validateForm(formEl)) {
    notyf__long.error('Полињата обележани со црвено се задолжителни!');
    return Promise.resolve();
  }

  let formData = new FormData(formEl);
  let jsonFormData = {};
  formData.forEach((value, key) => {
    jsonFormData[key] = value;
  });


  return HTTP.post(URLS.CHECKOUT, jsonFormData).then(response => {
    if (response.success) {
      window.location.href = response.data.thank_you_page_url;
    } else {
      let data = response.data;
      let status_code = response.status;
      if (status_code === 400) {
        let errors = response.data;
        Object.keys(errors).forEach(key => {
          let input = formEl.querySelector(`input[name=${key}]`);
          input.classList.add('error');
          notyf__long.error(errors[key].join(' '));
        });
      } else if (status_code === 403) {
        notyf__long.error(data.message);
      }
    }

  });
}

function validateForm(form) {
  let inputs = form.querySelectorAll('input');
  let is_valid = true;
  inputs.forEach(input => {
    if (input.value === "" && input.hasAttribute('required')) {

      let sibling = input.closest('.inputContainer').querySelector('.inputIcon');
      is_valid = false;
      input.classList.add('error');
      sibling.classList.add('error');
    }
  });

  return is_valid;
}

export {checkout};