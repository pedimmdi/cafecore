document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    const emailInput = form.querySelector('[name="email"]');

    if (emailInput) {
        emailInput.focus();
    }

    form.addEventListener("submit", () => {

        const submitButton = form.querySelector(".password-reset-btn");

        if (submitButton) {

            submitButton.disabled = true;
            submitButton.textContent = "در حال ارسال...";

        }

    });

});