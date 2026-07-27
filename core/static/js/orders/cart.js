document.addEventListener("DOMContentLoaded", () => {

    const removeButtons = document.querySelectorAll(".remove-btn");

    removeButtons.forEach((button) => {

        button.addEventListener("click", (event) => {

            const confirmed = confirm(
                "آیا از حذف این محصول از سبد خرید مطمئن هستید؟"
            );

            if (!confirmed) {

                event.preventDefault();

            }

        });

    });

});