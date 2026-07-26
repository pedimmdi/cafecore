document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    const firstNameInput = form.querySelector('[name="first_name"]');
    const lastNameInput = form.querySelector('[name="last_name"]');
    const emailInput = form.querySelector('[name="email"]');
    const password1Input = form.querySelector('[name="password1"]');
    const password2Input = form.querySelector('[name="password2"]');

    if (firstNameInput) {
        firstNameInput.focus();
    }

    form.addEventListener("submit", () => {

        [
            firstNameInput,
            lastNameInput,
            emailInput,
            password1Input,
            password2Input
        ].forEach(input => {

            if (input) {
                input.disabled = true;
            }

        });

        const submitButton = form.querySelector(".register-btn");

        if (submitButton) {

            submitButton.disabled = true;
            submitButton.textContent = "در حال ثبت نام...";

        }

    });

});