document.addEventListener("DOMContentLoaded", () => {

    const productCards = document.querySelectorAll(".product-card");

    productCards.forEach((card) => {

        card.addEventListener("mouseenter", () => {

            card.style.transition = ".35s";

        });

    });

});