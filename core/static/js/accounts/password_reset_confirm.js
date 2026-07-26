document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    const passwordInput = form.querySelector('[name="new_password1"]');

    if (passwordInput) {
        passwordInput.focus();
    }

    form.addEventListener("submit", () => {

        const button = form.querySelector(".confirm-btn");

        if (button) {

            button.disabled = true;

            button.textContent = "در حال ذخیره...";

        }

    });

});