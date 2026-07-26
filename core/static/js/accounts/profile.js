document.addEventListener("DOMContentLoaded", () => {

    const profileActions = document.querySelectorAll(".profile-actions a");

    profileActions.forEach(button => {

        button.addEventListener("mouseenter", () => {

            button.style.transform = "translateY(-2px)";

        });

        button.addEventListener("mouseleave", () => {

            button.style.transform = "translateY(0)";

        });

    });

});