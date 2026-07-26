document.addEventListener("DOMContentLoaded", () => {

    const button = document.querySelector(".complete-btn");

    if (!button) return;

    button.addEventListener("mouseenter", () => {

        button.style.transform = "translateY(-2px)";

    });

    button.addEventListener("mouseleave", () => {

        button.style.transform = "translateY(0)";

    });

});