document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.querySelector(".search-form input");

    if (searchInput) {

        searchInput.focus();

    }

    const searchForm = document.querySelector(".search-form");

    if (searchForm) {

        searchForm.addEventListener("submit", (event) => {

            const value = searchInput.value.trim();

            if (value === "") {

                event.preventDefault();

                searchInput.focus();

            }

        });

    }

});