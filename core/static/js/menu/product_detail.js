document.addEventListener("DOMContentLoaded", () => {

    const productImage = document.querySelector(".product-image img");

    if (productImage) {

        productImage.addEventListener("mousemove", (event) => {

            const rect = productImage.getBoundingClientRect();

            const x = ((event.clientX - rect.left) / rect.width - 0.5) * 6;
            const y = ((event.clientY - rect.top) / rect.height - 0.5) * -6;

            productImage.style.transform =
                `perspective(1000px) rotateY(${x}deg) rotateX(${y}deg) scale(1.03)`;

        });

        productImage.addEventListener("mouseleave", () => {

            productImage.style.transform =
                "perspective(1000px) rotateY(0deg) rotateX(0deg) scale(1)";

        });

    }

});