document.addEventListener("DOMContentLoaded", () => {
  const url = "/update_item/";

  // Get all the update buttons
  const updateButtons = document.querySelectorAll(".update-cart");

  // For each of the update buttons add a click listener
  updateButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const { product: productId, action } = this.dataset;
      if (user === "AnonymousUser") {
        console.log("Not authenticated.");
      } else {
        updateUserOrder(productId, action);
      }
    });
  });

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
