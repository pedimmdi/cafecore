document.addEventListener("DOMContentLoaded", () => {

    const removeForms = document.querySelectorAll(".favorite-actions form");

    removeForms.forEach((form) => {

        form.addEventListener("submit", (event) => {

            const confirmed = confirm(
                "آیا از حذف این محصول از علاقه‌مندی‌ها مطمئن هستید؟"
            );

            if (!confirmed) {

                event.preventDefault();

                return;

            }

            const button = form.querySelector("button");

            button.disabled = true;

            button.textContent = "در حال حذف...";

        });

    });

});