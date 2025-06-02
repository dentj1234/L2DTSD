function addToCart(itemId) {
        fetch("/add_to_cart", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ item_id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Item added. Cart count:", data.cart_count);
            // You can update a cart count on the page here if you want
        } 
        else {
            console.log("Failed to add item");
        }
    }); 
}

