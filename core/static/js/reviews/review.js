document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".review-form");

    if (!form) {

        return;

    }

    const submitButton = form.querySelector(".review-btn");

    form.addEventListener("submit", () => {

        submitButton.disabled = true;

        submitButton.textContent = "Submitting...";

    });

});