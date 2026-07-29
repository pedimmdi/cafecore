document.addEventListener("DOMContentLoaded", () => {

    const couponForm = document.querySelector(".coupon-form");

    if (couponForm) {

        couponForm.addEventListener("submit", (event) => {

            const input = couponForm.querySelector("input[name='code']");

            const button = couponForm.querySelector("button");

            if (!input.value.trim()) {

                event.preventDefault();

                alert("لطفاً کد تخفیف را وارد کنید.");

                input.focus();

                return;

            }

            button.disabled = true;

            button.textContent = "در حال بررسی...";

        });

    }

    const quantityForms = document.querySelectorAll(".quantity-form");

    quantityForms.forEach((form) => {

        form.addEventListener("submit", () => {

            const button = form.querySelector("button");

            button.disabled = true;

            button.textContent = "در حال بروزرسانی...";

        });

    });

    const removeForms = document.querySelectorAll(".cart-remove form");

    removeForms.forEach((form) => {

        form.addEventListener("submit", (event) => {

            const confirmed = confirm(
                "آیا از حذف این محصول از سبد خرید مطمئن هستید؟"
            );

            if (!confirmed) {

                event.preventDefault();

            }

        });

    });

});