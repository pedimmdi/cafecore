document.addEventListener("DOMContentLoaded", () => {
    const mobileMenuButton = document.querySelector(".mobile-menu-btn");
    const mobilePanel = document.querySelector(".mobile-nav-panel");
    const mobileClose = document.querySelector(".mobile-nav-close");
    const mobileOverlay = document.querySelector(".mobile-nav-overlay");

    if (!mobileMenuButton || !mobilePanel) return;

    function openMenu() {
        mobilePanel.classList.add("is-open");
        if (mobileOverlay) mobileOverlay.classList.add("is-open");
        document.body.classList.add("nav-open");
        mobileMenuButton.setAttribute("aria-expanded", "true");
    }

    function closeMenu() {
        mobilePanel.classList.remove("is-open");
        if (mobileOverlay) mobileOverlay.classList.remove("is-open");
        document.body.classList.remove("nav-open");
        mobileMenuButton.setAttribute("aria-expanded", "false");
    }

    mobileMenuButton.addEventListener("click", openMenu);

    if (mobileClose) {
        mobileClose.addEventListener("click", closeMenu);
    }

    if (mobileOverlay) {
        mobileOverlay.addEventListener("click", closeMenu);
    }

    mobilePanel.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", closeMenu);
    });
});