document.addEventListener("DOMContentLoaded", () => {
  const url = "/update_item/";

  // Get all the update buttons
  const updateButtons = document.querySelectorAll(".update-cart");

  // For each of the update buttons add a click listener
  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const { product: productId, action } = this.dataset;
      if (user === "AnonymousUser") {
        addCookieItem(productId, action);
      } else {
        updateUserOrder(productId, action);
      }
    });
  });

  const addCookieItem = (productId, action) => {
    if (action === "add") {
      if (typeof cart[productId] === "undefined") {
        cart[productId] = {
          quantity: 1,
        };
      } else {
        cart[productId]["quantity"] += 1;
      }
    } else if (action === "remove") {
      cart[productId]["quantity"] -= 1;

      if (cart[productId]["quantity"] < 1) {
        delete cart[productId];
      }
    }

    document.cookie = `cart=${JSON.stringify(cart)};domain=;path=/`;
    location.reload();
  };

  const updateUserOrder = (productId, action) => {
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        productId,
        action,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        location.reload();
      });
  };
});
