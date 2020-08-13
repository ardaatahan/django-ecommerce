document.addEventListener("DOMContentLoaded", () => {
  const shipping = "{{ order.is_shipping }}";
  const total = "{{ order.get_cart_total }}";
  const orderUrl = "/process_order/";

  if (shipping === "False") {
    document.querySelector("#shipping-info").innerHTML = "";
  }

  if (user !== "AnonymousUser") {
    document.querySelector("#user-info").innerHTML = "";
  }

  if (shipping === "False" && user !== "AnonymousUser") {
    document.querySelector("#form-wrapper").classList.add("hidden");
    document.querySelector("#payment-info").classList.remove("hidden");
  }

  const form = document.querySelector("#form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    document.querySelector("#form-button").classList.add("hidden");
    document.querySelector("#payment-info").classList.remove("hidden");
  });

  const csrftoken = form.querySelector("input").value;

  const paymentButton = document.querySelector("#make-payment");
  paymentButton.addEventListener("click", () => {
    submitFormData();
  });

  const submitFormData = () => {
    const userFormData = {
      name: null,
      email: null,
      total,
    };

    const shippingInfo = {
      address: null,
      city: null,
      state: null,
      zipcode: null,
    };

    if (shipping !== "False") {
      shippingInfo["address"] = form.address.value;
      shippingInfo["city"] = form.address.city;
      shippingInfo["state"] = form.address.state;
      shippingInfo["zipcode"] = form.address.zipcode;
    }

    if (user === "AnonymousUser") {
      userFormData["name"] = form.name.value;
      userFormData["email"] = form.email.value;
    }

    fetch(orderUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        form: userFormData,
        shipping: shippingInfo,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        window.location.href = "{% url 'store' %}";
      });
  };
});
