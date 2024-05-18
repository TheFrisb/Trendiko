import {Notyf} from "notyf";
import {getCsrfToken} from "../../utils/csrf";

const form = document.querySelector('#Analytics');
const notyf = new Notyf(
  {
    duration: 30000,
    ripple: true,
    position: {
      x: 'right',
      y: 'bottom',
    },
    dismissible: true,
  }
);

// on submit on form, prevent, submit with fetch, then show success message

function initializeRetrieveAdSpend() {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    const formUrl = `${form.action}?${new URLSearchParams(data).toString()}`
    const response = await fetch(formUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
    });

    const responseData = await response.json();

    if (response.ok) {
      console.log(responseData)
      let message = `USD: ${responseData.ad_spend_usd} | MKD: ${responseData.ad_spend_mkd}`;
      notyf.success(message);
    } else {
      notyf.error("Се случи грешка, ве молиме обидете се повторно.");
    }
  });
}

export {initializeRetrieveAdSpend};