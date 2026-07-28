document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    const submitButton = document.querySelector(".btn-primary");

    if (!form || !submitButton) {

        return;

    }

    form.addEventListener("submit", () => {

        submitButton.disabled = true;

        submitButton.textContent = "در حال ذخیره...";

    });

});