document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    const emailInput = form.querySelector('[name="username"]');
    const passwordInput = form.querySelector('input[type="password"]');

    if (emailInput) {
        emailInput.focus();
    }

    form.addEventListener("submit", () => {

        if (emailInput) {
            emailInput.disabled = true;
        }

        if (passwordInput) {
            passwordInput.disabled = true;
        }

        const submitButton = form.querySelector(".login-btn");

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "در حال ورود...";
        }

    });

});