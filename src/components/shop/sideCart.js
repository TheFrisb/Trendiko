const cartEl = document.getElementById("sideCart");
const cartIcon = document.getElementById("cartIcon");
const closeCartIcon = document.getElementById("closeCartIcon");
const cartQuantity = document.getElementById("cartIcon__currentQuantity");
const cartBody = document.getElementById("cartBody");
const cartTotal = document.getElementById("cartTotal");

function isSideCartActive() {
  return cartEl.classList.contains("active");
}

function toggleSideCart() {
  cartEl.classList.toggle("active");
}

function initializeSideCart() {
  cartIcon.addEventListener("click", function () {
    toggleSideCart();
  });

  closeCartIcon.addEventListener("click", function () {
    toggleSideCart();
  });
}

function updateCartQuantityAndTotal() {
  let cartItems = cartBody.querySelectorAll("[data-cart-item-id]");

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
}

function createSideCartItem(cartItem) {
  const thumbnails = cartItem.thumbnails;
  const sideCartItemDiv = document.createElement("div");
  sideCartItemDiv.classList.add("flex", "gap-2", "items-center", "py-4", "border-b-2", "p-5 cartItem");
  sideCartItemDiv.setAttribute("data-cart-item-id", cartItem.id);
  sideCartItemDiv.innerHTML = `
                                <picture class="">
                                  <source srcset="${thumbnails.webp}" type="image/webp">
                                  <source srcset="${thumbnails.jpg}" type="image/png">
                                  <img src="${thumbnails.jpg}" alt=""
                                       class="rounded-lg" width="120" height="120">
                              </picture>
                              <div class="flex-grow">
                                  <p class="font-semibold">${cartItem.title}</p>
                                  <p class="font-semibold text-brand-action mt-2"><span class="cartItem__salePrice"${cartItem.sale_price}</span> ден</p>
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
                                      <svg class="text-black cursor-pointer hover:text-black/60" width="22"
                                           height="22"
                                           fill="currentColor">
                                          <use xlink:href="{% static 'common/assets/svg_sprite.svg' %}#trash"></use>
                                      </svg>
                      
                                  </div>
                              </div>
  `;

  // add event listeners for the quantity buttons
  cartBody.appendChild(sideCartItemDiv);
}

console.log(cartBody);

function updateSideCart(response) {
  const cartItem = cartBody.querySelector(`[data-cart-item-id="${response.id}"]`);

  if (cartItem) {
    const quantityInput = cartItem.querySelector(".cartItem__quantityInput");
    quantityInput.value = response.quantity;
  } else {
    createSideCartItem(response);
  }

  updateCartQuantityAndTotal();
}


export {initializeSideCart, isSideCartActive, toggleSideCart, updateSideCart};