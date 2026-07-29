document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".contact-form form");

    const submitButton = form?.querySelector("button");

    if (!form || !submitButton) {

        return;

    }

    form.addEventListener("submit", () => {

        submitButton.disabled = true;

        submitButton.textContent = "در حال ارسال...";

    });

});