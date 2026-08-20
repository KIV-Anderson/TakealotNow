// async function addToCart(productId) {

//     await fetch(`/api/add_to_cart/${productId}`);

//     location.reload();
// }

// async function removeFromCart(productId) {

//     await fetch(`/api/remove_from_cart/${productId}`);

//     location.reload();
// }
async function addToCart(productId) {

    const response =
        await fetch(`/api/add_to_cart/${productId}`);

    const data =
        await response.json();

    updateCartUI(productId, data);
}

async function removeFromCart(productId) {

    const response =
        await fetch(`/api/remove_from_cart/${productId}`);

    const data =
        await response.json();

    updateCartUI(productId, data);
}

function updateCartUI(productId, data) {

    document.getElementById("cart-link").innerText =
        `Cart (${data.cart_count})`;

    if (data.quantity <= 0) {

        const row =
            document.getElementById(`row-${productId}`);

        if (row) {
            row.remove();
        }

    } else {

        document.getElementById(
            `qty-${productId}`
        ).innerText = data.quantity;

        document.getElementById(
            `subtotal-${productId}`
        ).innerText = `R${data.subtotal}`;
    }

    document.getElementById("cart-total").innerText =
        `Total: R${data.cart_total}`;

    const remainingRows =
        document.querySelectorAll("[id^='row-']");

    if (remainingRows.length === 0) {
        location.reload();
    }
}
