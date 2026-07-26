document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".category-card");

    cards.forEach((card) => {

        card.addEventListener("mouseenter", () => {

            card.style.transition = ".35s";

        });

    });

});