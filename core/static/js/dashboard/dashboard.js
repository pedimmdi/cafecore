document.addEventListener("DOMContentLoaded", () => {

    initializeRevenueChart();

    initializeOrdersChart();

});


function initializeRevenueChart() {

    const canvas = document.getElementById("revenueChart");

    if (!canvas) return;

    const labels = JSON.parse(
        document.getElementById("revenue-labels").textContent
    );

    const values = JSON.parse(
        document.getElementById("revenue-values").textContent
    );

    new Chart(canvas, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "درآمد",

                    data: values,

                    borderColor: "#D4AF37",

                    backgroundColor: "rgba(212,175,55,.15)",

                    fill: true,

                    tension: .35,

                    borderWidth: 3,

                    pointRadius: 5,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#D4AF37",

                    pointBorderColor: "#111",

                    pointBorderWidth: 2,

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {

                mode: "index",

                intersect: false,

            },

            plugins: {

                legend: {

                    display: false,

                },

                tooltip: {

                    backgroundColor: "#1b1b1b",

                    titleColor: "#fff",

                    bodyColor: "#ddd",

                    borderColor: "#D4AF37",

                    borderWidth: 1,

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false,

                    },

                    ticks: {

                        color: "#bbb",

                    }

                },

                y: {

                    beginAtZero: true,

                    grid: {

                        color: "rgba(255,255,255,.05)",

                    },

                    ticks: {

                        color: "#bbb",

                    }

                }

            }

        }

    });

}


function initializeOrdersChart() {

    const canvas = document.getElementById("ordersChart");

    if (!canvas) return;

    const labels = JSON.parse(
        document.getElementById("orders-labels").textContent
    );

    const values = JSON.parse(
        document.getElementById("orders-values").textContent
    );

    new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "سفارش‌ها",

                    data: values,

                    backgroundColor: [

                        "#D4AF37",

                        "#C9A227",

                        "#B8911E",

                        "#A57D15",

                        "#8F6B10",

                        "#D4AF37",

                        "#C9A227",

                        "#B8911E",

                        "#A57D15",

                        "#8F6B10",

                        "#D4AF37",

                        "#C9A227",

                    ],

                    borderRadius: 8,

                    maxBarThickness: 45,

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false,

                },

                tooltip: {

                    backgroundColor: "#1b1b1b",

                    titleColor: "#fff",

                    bodyColor: "#ddd",

                    borderColor: "#D4AF37",

                    borderWidth: 1,

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false,

                    },

                    ticks: {

                        color: "#bbb",

                    }

                },

                y: {

                    beginAtZero: true,

                    grid: {

                        color: "rgba(255,255,255,.05)",

                    },

                    ticks: {

                        color: "#bbb",

                    }

                }

            }

        }

    });

}