function addToCart(itemId) {
        fetch("/add_to_cart", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            success: true,
            item_id: itemId
         })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Item added. Cart count:", data.cart_count);
            showPopup("Item added to cart!");
        } 
        else {
            console.log("Failed to add item");
        }
    }); 
    console.log("Adding item to cart:", itemId);
}
function showPopup(message) {
    const popup = document.createElement("div");
    popup.textContent = message;

    Object.assign(popup.style, {
        position: "fixed",
        bottom: "20px",
        right: "20px",
        backgroundColor: "#28a745",
        color: "white",
        padding: "12px 20px",
        borderRadius: "8px",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.2)",
        zIndex: "1000",
        opacity: "1",
        transition: "opacity 0.5s ease"
    });

    document.body.appendChild(popup);

    // Start fade-out after 1.5 seconds
    setTimeout(() => {
        popup.style.opacity = "0";
    }, 1500);

    // Remove after fade-out completes (2s total)
    setTimeout(() => {
        popup.remove();
    }, 2000);
}

function recalcTotal() {
  let total = 0;
  document.querySelectorAll('.item-card').forEach(card => {
    const price = parseFloat(card.dataset.price);
    const qty = parseInt(card.querySelector('.qty-display').textContent) || 0;
    total += price * qty;
  });
  // Update total cost display
  document.getElementById('total-cost').textContent = total.toFixed(2);
}