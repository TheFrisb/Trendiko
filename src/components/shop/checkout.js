import {HTTP, URLS} from "../../http/client";
import {notyf__long} from "../../utils/error";


function checkout(formEl) {
  console.log("checkout formEl", formEl)
  if (!validateForm(formEl)) {
    notyf__long.error('Полињата обележани со црвено се задолжителни!');
    return;
  }

  let formData = new FormData(formEl);
  let jsonFormData = {};
  formData.forEach((value, key) => {
    jsonFormData[key] = value;
  });

  console.log("jsonFormData", jsonFormData)

  HTTP.post(URLS.CHECKOUT, jsonFormData).then(response => {
    if (response.success) {
      window.location.href = response.data.thank_you_page_url;
    } else {
      let errors = response.data;
      Object.keys(errors).forEach(key => {
        console.log("key", key)
        let input = formEl.querySelector(`input[name=${key}]`);
        input.classList.add('error');
        notyf__long.error(errors[key].join(' '));
      });


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