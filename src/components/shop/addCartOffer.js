import {HTTP, URLS} from "../../http/client";
import {updateCart} from "./cart";
import {notyf__short} from "../../utils/error";

function addCartOffer(cartOfferId) {
  const data = {
    cart_offer_id: cartOfferId,
  }

  return HTTP.post(URLS.ADD_CART_OFFER, data).then(response => {
    const data = response.data;
    if (response.success) {
      updateCart(data);

    } else {
      let status_code = response.status;
      if (status_code === 403) {
        notyf__short.error(data.message);
      } else {
        notyf__short.error('Проблем со додавањето на продуктот во кошничка. Ве молиме обидете се повторно.');
      }
    }
  });
}


function getAllCartOfferButtonsById(cartOfferId) {
  return document.querySelectorAll(`.addCartOfferBtn[data-cart-offer-id="${cartOfferId}"]`);
}

function restoreAddCartOfferButtons(cartOfferId) {
  const allButtons = getAllCartOfferButtonsById(cartOfferId);
  allButtons.forEach(function (btn) {
    btn.disabled = false;
    const btnText = btn.querySelector('.buttonText');
    const btnSpinner = btn.querySelector('.buttonSpinner');

    btnText.textContent = 'Додади';
    btnText.classList.remove('hidden');
    btnSpinner.classList.add('hidden');
    btnSpinner.classList.remove('flex');
  });
}


function initializeAddCartOfferButtons() {
  const addCartOfferButtons = document.querySelectorAll('.addCartOfferBtn');
  addCartOfferButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      if (button.disabled) {
        return;
      }
      const cartOfferId = parseInt(button.getAttribute('data-cart-offer-id'));
      const allButtons = getAllCartOfferButtonsById(cartOfferId);

      allButtons.forEach(function (btn) {
        btn.disabled = true;
        const buttonText = btn.querySelector('.buttonText');
        const buttonSpinner = btn.querySelector('.buttonSpinner');

        buttonText.classList.add('hidden');
        buttonSpinner.classList.remove('hidden');
      });


      addCartOffer(cartOfferId).finally(() => {
        allButtons.forEach(function (btn) {
          const btnText = btn.querySelector('.buttonText');
          const btnSpinner = btn.querySelector('.buttonSpinner');

          btnText.classList.remove('hidden');
          btnText.textContent = 'Додаден';
          btnSpinner.classList.add('hidden');
          btnSpinner.classList.remove('flex');
        });

      });
    });
  });
}

export {initializeAddCartOfferButtons, restoreAddCartOfferButtons};