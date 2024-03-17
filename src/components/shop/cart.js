import {attachCartItemInputListeners, removeCartItem} from "./quantityInput";
import {checkout} from "./checkout";

const body = document.querySelector("body");
const cartOverlay = document.getElementById("sideCartOverlay");
const cartEl = document.getElementById("sideCart");
const cartIcon = document.getElementById("cartIcon");
const closeCartIcon = document.getElementById("closeCartIcon");
const cartQuantity = document.getElementById("cartIcon__currentQuantity");
const cartBody = document.getElementById("cartBody");
const cartTotal = document.getElementById("cartTotal");
const cartGoBackButton = document.getElementById("sideCart__goBackButon");
const cartGoToCheckoutButton = document.getElementById("sideCart__goToCheckoutBtn");

const checkoutEl = document.getElementById("checkoutContainer");
const checkoutForm = document.getElementById("checkoutForm");
const clickableCheckout = document.getElementById("checkout");
const closeCheckoutIcon = document.getElementById("closeCheckoutIcon");
const checkoutBody = document.getElementById("checkoutBody");
const checkoutSubtotal = document.getElementById("checkout__subtotalPrice");
const checkoutShipping = document.getElementById("checkout__selectedShipping");
const checkoutTotal = document.getElementById("checkout__totalPrice");
const checkoutButton = document.getElementById("checkoutBtn");

function isSideCartActive() {
  return cartEl.classList.contains("active");
}

function isCheckoutActive() {
  return checkoutEl.classList.contains("active");
}

function isSideCartEmpty() {
  return cartBody.childElementCount === 0;
}

function toggleSideCart() {
  body.classList.toggle("overflow-hidden");
  cartOverlay.classList.toggle("active");
  cartEl.classList.toggle("active");
}

function toggleCheckout() {
  body.classList.toggle("overflow-hidden");
  let inputs = checkoutForm.querySelectorAll('input');
  inputs.forEach(input => {
    input.classList.remove('error');
    let sibling = input.closest('.inputContainer').querySelector('.inputIcon');

    console.log(sibling);
    console.log(input.closest('.inputContainer'))
    sibling.classList.remove('error');

  });
  checkoutEl.classList.toggle("active");
}

function initializeCart() {
  cartIcon.addEventListener("click", function () {
    toggleSideCart();
  });

  closeCartIcon.addEventListener("click", function () {
    toggleSideCart();
  });

  closeCheckoutIcon.addEventListener("click", function () {
    toggleCheckout();
  });

  checkoutEl.addEventListener("click", function (e) {
    if (e.target === checkoutEl) {
      toggleCheckout();
    }
  });

  cartOverlay.addEventListener("click", function () {
    if (isSideCartActive()) {
      toggleSideCart();
    }
  });

  cartGoBackButton.addEventListener("click", function () {
    toggleSideCart();
  });

  cartGoToCheckoutButton.addEventListener("click", function () {
    toggleSideCart();
    toggleCheckout();
  });

  checkoutButton.addEventListener("click", function () {
    console.log("checkout button clicked");
    checkoutButton.disabled = true;
    checkout(checkoutForm);
    checkoutButton.disabled = false;

  });

}

function updateCartQuantityAndTotal(hasFreeShipping) {
  let cartItems = cartBody.querySelectorAll("[data-cart-item-id]");
  if (cartItems.length === 0) {
    cartEl.classList.remove("buyableCart")
    if (isCheckoutActive()) {
      toggleCheckout();
    }
    cartGoToCheckoutButton.disabled = true;
  } else {
    cartEl.classList.add("buyableCart")
    cartGoToCheckoutButton.disabled = false;
  }

  let totalQuantity = 0;
  let cartTotalPrice = 0;
  cartItems.forEach(function (item) {
    let quantity = item.querySelector(".cartItem__quantityInput").value;
    let salePrice = item.querySelector(".cartItem__salePrice").innerText;
    totalQuantity += parseInt(quantity);
    cartTotalPrice += parseInt(salePrice) * parseInt(quantity);
  });

  cartQuantity.innerHTML = totalQuantity;
  cartTotal.innerHTML = cartTotalPrice;

  checkoutSubtotal.innerHTML = cartTotalPrice;
  if (hasFreeShipping) {
    cartTotalPrice += 20;
    checkoutShipping.innerHTML = "бесплатна достава";
    checkoutTotal.innerHTML = cartTotalPrice;
  } else {
    cartTotalPrice += 20 + 130;
    checkoutShipping.innerHTML = "130 ден";
    checkoutTotal.innerHTML = cartTotalPrice
  }

}

function removeCartItemElement(cartItemId, hasFreeShipping) {
  const cartItem = cartBody.querySelector(`[data-cart-item-id="${cartItemId}"]`);
  const checkoutItem = checkoutBody.querySelector(`[data-cart-item-id="${cartItemId}"]`);
  cartItem.remove();
  checkoutItem.remove();
  updateCartQuantityAndTotal(hasFreeShipping);
}

function createSideCartItem(cartItem) {
  const thumbnails = cartItem.thumbnails;
  const sideCartItemDiv = document.createElement("div");
  sideCartItemDiv.classList.add("flex", "gap-2", "items-center", "py-4", "border-b-2", "p-5", "cartItem");
  sideCartItemDiv.setAttribute("data-cart-item-id", cartItem.id);
  sideCartItemDiv.innerHTML = `
                                <picture class="">
                                  <source srcset="${thumbnails.webp}" type="image/webp">
                                  <source srcset="${thumbnails.jpg}" type="image/png">
                                  <img src="${thumbnails.jpg}" alt=""
                                       class="rounded-lg min-w-[120px]" width="120" height="120">
                              </picture>
                              <div class="flex-grow">
                                  <p class="font-semibold">${cartItem.title}</p>
                                  <p class="font-semibold text-brand-action mt-2"><span class="cartItem__salePrice">${cartItem.sale_price}</span> ден</p>
                                  <div class="flex items-center w-9/12 h-9 bg-white rounded-lg mb-4">
                                      <button class="w-3/12 h-full hover:bg-brand-primary hover:text-white rounded-l-lg border border-r-0 border-black/60">
                                          -
                                      </button>
                                      <input type="number" value="${cartItem.quantity}" min="1"
                                             class="w-4/12 h-full text-center cartItem__quantityInput border-t border-b border-black/60 focus:outline-0">
                                      <button class="w-3/12 h-full hover:bg-brand-primary hover:text-white rounded-r-lg border border-l-0 border-black/60">
                                          +
                                      </button>
                                  </div>
                                  <div>
                                      <svg class="text-black cursor-pointer hover:text-black/60 cartItem__removeItem" width="22"
                                           height="22"
                                           fill="currentColor">
                                          <use xlink:href="/static/common/assets/svg_sprite.svg#trash"></use>
                                      </svg>
                      
                                  </div>
                              </div>
  `;

  const quantityInput = sideCartItemDiv.querySelector(".cartItem__quantityInput");
  const removeButton = sideCartItemDiv.querySelector(".cartItem__removeItem");
  const cartItemId = cartItem.id;
  attachCartItemInputListeners(quantityInput);
  removeButton.addEventListener("click", function () {
    removeCartItem(cartItemId);
  });

  cartBody.appendChild(sideCartItemDiv);
}

function createCheckoutItem(cartItem) {
  const thumbnails = cartItem.thumbnails;
  const checkoutCartItemDiv = document.createElement("div");
  checkoutCartItemDiv.classList.add("flex", "gap-2", "items-center", "pb-4", "border-b", "cartItem");
  checkoutCartItemDiv.setAttribute("data-cart-item-id", cartItem.id);
  checkoutCartItemDiv.innerHTML = `
                                <picture class="">
                                  <source srcset="${thumbnails.webp}" type="image/webp">
                                  <source srcset="${thumbnails.jpg}" type="image/png">
                                  <img src="${thumbnails.jpg}" alt=""
                                       class="rounded-lg min-w-[120px]" width="120" height="120"> 
                              </picture>
                              <div class="flex-grow">
                                  <p class="font-semibold">${cartItem.title}</p>
                                  <p class="font-semibold text-brand-action mt-2"><span class="cartItem__salePrice">${cartItem.sale_price}</span> ден</p>
                                  <div class="flex items-center w-9/12 h-9 bg-white rounded-lg mb-4">
                                      <button class="w-3/12 h-full hover:bg-brand-primary hover:text-white rounded-l-lg border border-r-0 border-black/60">
                                          -
                                      </button>
                                      <input type="number" value="${cartItem.quantity}" min="1"
                                             class="w-6/12 h-full text-center cartItem__quantityInput border-t border-b border-black/60 focus:outline-0">
                                      <button class="w-3/12 h-full hover:bg-brand-primary hover:text-white rounded-r-lg border border-l-0 border-black/60">
                                          +
                                      </button>
                                  </div>
                                  <div>
                                      <svg class="text-black cursor-pointer hover:text-black/60 cartItem__removeItem" width="22"
                                           height="22"
                                           fill="currentColor">
                                          <use xlink:href="/static/common/assets/svg_sprite.svg#trash"></use>
                                      </svg>
                      
                                  </div>
                              </div>
  `;

  const quantityInput = checkoutCartItemDiv.querySelector(".cartItem__quantityInput");
  const removeButton = checkoutCartItemDiv.querySelector(".cartItem__removeItem");
  const cartItemId = cartItem.id;
  attachCartItemInputListeners(quantityInput);
  removeButton.addEventListener("click", function () {
    removeCartItem(cartItemId);
  });

  checkoutBody.appendChild(checkoutCartItemDiv);
}

function updateCart(response) {
  const cartItem = cartBody.querySelector(`[data-cart-item-id="${response.id}"]`);
  const checkoutItem = checkoutBody.querySelector(`[data-cart-item-id="${response.id}"]`);
  if (cartItem) {
    const cartItemQuantityInput = cartItem.querySelector(".cartItem__quantityInput");
    const checkoutItemQuantityInput = checkoutItem.querySelector(".cartItem__quantityInput");
    cartItemQuantityInput.value = response.quantity;
    checkoutItemQuantityInput.value = response.quantity;
  } else {
    createSideCartItem(response);
    createCheckoutItem(response);
  }
  console.log(response);
  updateCartQuantityAndTotal(response.has_free_shipping);
}


export {
  initializeCart,
  isSideCartActive,
  toggleSideCart,
  updateCart,
  removeCartItemElement,
  toggleCheckout
};