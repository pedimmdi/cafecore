document.addEventListener("DOMContentLoaded", () => {

    const icon = document.querySelector(".success-card i");

    if (icon) {

        icon.animate(

            [

                { transform: "scale(0.8)", opacity: 0 },

                { transform: "scale(1.15)", opacity: 1 },

                { transform: "scale(1)", opacity: 1 }

            ],

            {

                duration: 700,

                easing: "ease-out"

            }

        );

    }

});