document.addEventListener("DOMContentLoaded", () => {

    const checkoutForm = document.querySelector(".checkout-form");

    if (!checkoutForm) {

        return;

    }

    checkoutForm.addEventListener("submit", (event) => {

        const confirmed = confirm(
            "آیا از ثبت این سفارش اطمینان دارید؟"
        );

        if (!confirmed) {

            event.preventDefault();

        }

    });

});