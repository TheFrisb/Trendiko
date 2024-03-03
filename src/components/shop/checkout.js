import {HTTP, URLS} from "../../http/client";
import {Notyf} from "notyf";

let notyf = new Notyf(
  {
    duration: 10000,
    ripple: true,
    position: {
      x: 'left',
      y: 'bottom',
    },
    dismissible: true,

  }
);

function checkout(formEl) {
  console.log("checkout formEl", formEl)
  if (!validateForm(formEl)) {
    notyf.error('Полињата обележани со црвено се задолжителни!');
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
      // The response has a list of input keys, with the errors as list. Pass all the errors to the notyf and color the inputs by keyname red
      let errors = response.data;
      Object.keys(errors).forEach(key => {
        console.log("key", key)
        let input = formEl.querySelector(`input[name=${key}]`);
        input.classList.add('error');
        notyf.error(errors[key].join(' '));
      });


    }

  });
}

function validateForm(form) {
  let inputs = form.querySelectorAll('input');
  let is_valid = true;
  inputs.forEach(input => {
    if (input.value === "") {
      let sibling = input.previousElementSibling;
      is_valid = false;
      input.classList.add('error');
      sibling.classList.add('error');
    }
  });

  return is_valid;
}

export {checkout};