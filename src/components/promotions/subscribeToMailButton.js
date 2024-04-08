import {HTTP, URLS} from "../../http/client";
import {notyf__short} from "../../utils/error";

function subscribeToMail(email) {
  const data = {
    email: email,
  }

  HTTP.post(URLS.SUBSCRIBE_TO_MAIL, data).then(response => {
    if (response.success) {
      notyf__short.success('Се претплативте успешно!');
    } else if (response.data && response.data.email[0].includes('already exists')) {
      notyf__short.error("Оваа e-mail адреса веќе е претплатена.");
    } else {
      notyf__short.error("Ве молиме внесете валидна e-mail адреса.");
    }
  });
}

function initializeSubscribeToMailButtons() {
  const subscribeToMailButtons = document.querySelectorAll('.subscribeToMailButton');
  subscribeToMailButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      let input = button.parentElement.querySelector('.subscribeToMailInput');
      let email = input.value;
      subscribeToMail(email);
    });
  });
}

export {initializeSubscribeToMailButtons};

