document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    const oldPasswordInput = form.querySelector('[name="old_password"]');

    if (oldPasswordInput) {
        oldPasswordInput.focus();
    }

    form.addEventListener("submit", () => {

        const submitButton = form.querySelector(".password-change-btn");

        if (submitButton) {

            submitButton.disabled = true;
            submitButton.textContent = "در حال تغییر...";

        }

    });

});