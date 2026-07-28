document.addEventListener("DOMContentLoaded", () => {

    const statCards = document.querySelectorAll(".stat-card");

    statCards.forEach((card) => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-6px)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0)";

        });

    });

    const dashboardItems = document.querySelectorAll(".dashboard-card li");

    dashboardItems.forEach((item) => {

        item.addEventListener("mouseenter", () => {

            item.style.paddingLeft = "10px";

        });

        item.addEventListener("mouseleave", () => {

            item.style.paddingLeft = "0";

        });

    });

});