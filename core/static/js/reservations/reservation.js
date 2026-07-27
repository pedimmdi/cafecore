document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".reservation-form");

    if (!form) {

        return;

    }

    const submitButton = form.querySelector(
        ".reservation-btn",
    );

    form.addEventListener(
        "submit",
        () => {

            submitButton.disabled = true;

            submitButton.textContent =
                "در حال ثبت درخواست...";

        },
    );

});