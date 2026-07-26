document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    const firstNameInput = form.querySelector('[name="first_name"]');

    if (firstNameInput) {
        firstNameInput.focus();
    }

    form.addEventListener("submit", () => {

        const submitButton = form.querySelector(".update-btn");

        if (submitButton) {

            submitButton.disabled = true;
            submitButton.textContent = "در حال ذخیره...";

        }

    });

});