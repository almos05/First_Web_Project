document.addEventListener("DOMContentLoaded", () => {
    const productContainer = document.querySelector(".shop__grid");
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

    fetch("/api/products/")
        .then((response) => response.json())
        .then((products) => {
            productContainer.innerHTML = products.map(product => `
                <div class="product__card">
                    <img src="${product.image_url}" alt="${product.name}">
                    <h2>${product.name}</h2>
                    <p>$${product.price}</p>
                    <button class="shop__button" data-id="${product.id}">Add to Cart</button>
                </div>
            `).join("");
        });

    productContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains("shop__button")) {
            const productId = event.target.getAttribute("data-id");
            fetch("/api/cart/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ product_id: productId, quantity: 1 })
            }).then((response) => {
                if (response.ok) {
                    alert("Product added to cart!");
                }
            });
        }
    });
});
