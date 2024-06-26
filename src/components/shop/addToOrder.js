import {HTTP, URLS} from "../../http/client";
import {notyf__long, notyf__short} from "../../utils/error";
import {formatNumberToLocale} from "../../utils/numberFormatter";

const ordersTable = document.getElementById('ordersTable');
const orderItemsContainer = document.getElementById('orderItemsContainer');
const orderSubtotalPriceContainer = document.getElementById('order__subtotalPrice');
const orderTotalPriceContainer = document.getElementById('order__totalPrice');
const orderShippingMethodContainer = document.getElementById('order__selectedShipping');

function addToOrder(orderId, orderItemId, quantity, trackingCode, promotionPrice) {
  const data = {
    order_id: orderId,
    order_item_id: orderItemId,
    quantity: quantity,
    tracking_code: trackingCode,
    promotion_price: promotionPrice
  }

  return HTTP.post(URLS.ADD_TO_ORDER, data)
}

function updateOrderTotals(data) {
  orderSubtotalPriceContainer.innerText = formatNumberToLocale(data.order_subtotal);
  orderTotalPriceContainer.innerText = formatNumberToLocale(data.order_total);
  orderShippingMethodContainer.innerText = data.order_shipping_method;
}

function makeOrUpdateOrderItemRow(orderItem) {
  const orderItemRow = orderItemsContainer.querySelector(`[data-order-item-id="${orderItem.id}"]`);
  if (orderItemRow) {
    const quantity = orderItemRow.querySelector('.orderItem__quantity');
    const totalPrice = orderItemRow.querySelector('.orderItem__totalPrice');
    quantity.innerText = formatNumberToLocale(orderItem.quantity);
    totalPrice.innerText = formatNumberToLocale(orderItem.total_price);
  } else {
    const orderItemHtml = makeOrderItemHtml(orderItem);
    orderItemsContainer.insertAdjacentHTML('beforeend', orderItemHtml);
  }
}

function makeOrderItemHtml(orderItem) {
  let thumbnails = orderItem.thumbnails;
  return `
                          <div class="flex items-center justify-between" data-order-item-id="${orderItem.id}">
                            <div class="flex gap-2">
                                    <picture>
                                        <source srcset="${thumbnails.webp}" type="image/webp">
                                        <source srcset="${thumbnails.jpg}" type="image/jpeg">
                                        <img src="${thumbnails.jpg}" alt="Image of a product"
                                             class="min-w-[64px] min-h-[64px] object-cover rounded-lg" width="64" height="64">
                                    </picture>
                                <div>
                                    <p class="font-bold">${orderItem.get_readable_name}</p>
                                    <p class="text-sm">${formatNumberToLocale(orderItem.price)} ден x <span
                                            class="orderItem__quantity">${orderItem.quantity}</span></p> 
                                </div>
                            </div>
                            <p class="font-bold"><span class="orderItem__totalPrice">${formatNumberToLocale(orderItem.total_price)}</span>
                                ден</p>
                        </div>
  `;
}

function initializeAddToOrderButtons() {
  const addToOrderButtons = document.querySelectorAll('.addToOrderButton');
  addToOrderButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      const orderItemId = parseInt(button.getAttribute('data-order-item-id'));
      const quantity = parseInt(button.getAttribute('data-quantity'));
      const orderId = parseInt(button.getAttribute('data-order-id'));
      const trackingCode = window.location.pathname.split('/')[2];
      const promotionPrice = parseInt(button.getAttribute('data-promotion-price'));

      const buttonText = button.querySelector('.buttonText');
      const buttonSpinner = button.querySelector('.buttonSpinner');

      button.disabled = true;
      buttonText.classList.add('hidden');
      buttonSpinner.classList.remove('hidden');
      buttonSpinner.classList.add('flex');


      addToOrder(orderId, orderItemId, quantity, trackingCode, promotionPrice).then(response => {
        const data = response.data;
        if (response.success) {
          notyf__short.success("Продуктот е додаден во порачката");
          makeOrUpdateOrderItemRow(data);
          updateOrderTotals(data);
          ordersTable.scrollIntoView({behavior: "smooth"});

          buttonText.textContent = 'Додаден';

        } else {
          let status_code = response.status;
          if (status_code === 403) {
            notyf__long.error(data.message);
          } else {
            notyf__long.error("Се случи грешка, ве молиме обидете се повторно.");
          }

          button.disabled = false;
        }
      }).finally(() => {
        buttonText.classList.remove('hidden');
        buttonSpinner.classList.add('hidden');
        buttonSpinner.classList.remove('flex');
      });
    });
  });
}

export {initializeAddToOrderButtons};