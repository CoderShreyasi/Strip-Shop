const stripe = Stripe("{{ stripe_pub_key }}");

document.querySelectorAll('.buy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const productId = btn.dataset.productId;
        const qtyInput = document.querySelector(`input[data-product-id="${productId}"]`);
        const quantity = qtyInput.value;

        const response = await fetch("/create-checkout-session/", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                product_id: productId,
                quantity: quantity
            })
        });

        const data = await response.json();

        if (data.checkout_url) {
            window.location = data.checkout_url;
        }
    });
});
