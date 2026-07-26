document.addEventListener("DOMContentLoaded", () => {

    const mobileMenuButton = document.querySelector(".mobile-menu-btn");

    if (!mobileMenuButton) return;

    mobileMenuButton.addEventListener("click", () => {

        console.log("Mobile Menu");

    });

});