document.addEventListener("DOMContentLoaded", function () {
  const cartItemsContainer = document.getElementById("cart-items");
  const totalAmountEl = document.getElementById("total-amount");
  const totalMrpEl = document.getElementById("total-mrp-amount");
  const discountAmountEl = document.getElementById("discount-amount");
  const finalAmountEl = document.getElementById("final-amount");
  const totalAmountInput = document.getElementById("grand-total");

  function calculateTotal() {
    let total = 0;
    let totalMrp = 0;
    let discount = 0;
    let finalAmount = 0;

    // Iterate over each cart item to calculate the total amounts
    document.querySelectorAll(".cart-item").forEach((row) => {
      const quantity = parseInt(row.querySelector(".qty").textContent, 10);
      const price = parseFloat(row.querySelector(".price").textContent);
      const mrp = parseFloat(row.querySelector(".mrp").textContent);

      const itemTotal = quantity * price;
      const mrpItemTotal = quantity * mrp;

      // Update the total and mrp amounts for the item
      row.querySelector(".item-total-amount").textContent =
        itemTotal.toFixed(2);

      total += itemTotal;
      totalMrp += mrpItemTotal;
    });

    // Calculate discount (Total MRP - Total Selling Price)
    discount = totalMrp - total;

    // Calculate the final bill amount
    finalAmount = total;

    // Update the DOM elements with calculated values
    totalMrpEl.textContent = totalMrp.toFixed(2);
    discountAmountEl.textContent = discount.toFixed(2);
    finalAmountEl.textContent = finalAmount.toFixed(2);
    totalAmountEl.textContent = finalAmount.toFixed(2);
    totalAmountInput.value = finalAmount.toFixed(2);

    console.log(
      `Total MRP: ${totalMrp}, Discount: ${discount}, Final Amount: ${finalAmount}`
    );
  }

  cartItemsContainer.addEventListener("click", function (event) {
    if (
      event.target.classList.contains("increase") ||
      event.target.classList.contains("decrease")
    ) {
      const qtyEl = event.target
        .closest(".item-quantity")
        .querySelector(".qty");
      let qty = parseInt(qtyEl.textContent, 10);
      if (event.target.classList.contains("increase")) {
        qty += 1;
      } else if (event.target.classList.contains("decrease") && qty > 1) {
        qty -= 1;
      }
      qtyEl.textContent = qty;
      calculateTotal();
    }

    if (event.target.closest(".delete-item")) {
      const itemId = event.target.closest(".cart-item").getAttribute("data-id");
      event.target.closest(".cart-item").remove();
      calculateTotal();

      // Send AJAX request to update session on the server
      fetch("/remove-from-cart/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // Django CSRF protection
        },
        body: JSON.stringify({ item_id: itemId }),
      })
        .then((response) => {
          if (!response.ok) {
            console.error("Failed to update session on server");
          }
        })
        .catch((error) => console.error("Error:", error));
    }
  });

  calculateTotal();
});

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
