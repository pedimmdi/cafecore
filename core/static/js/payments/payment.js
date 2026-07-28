document.addEventListener("DOMContentLoaded", () => {

    const paymentButton = document.querySelector(".btn-primary");

    if (!paymentButton) {

        return;

    }

    paymentButton.addEventListener("click", () => {

        paymentButton.classList.add("disabled");

        paymentButton.textContent = "Redirecting...";

        paymentButton.style.pointerEvents = "none";

    });

});