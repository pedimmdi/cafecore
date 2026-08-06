document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("dashSidebarToggle");
    var sidebar = document.getElementById("dashSidebar");
    if (toggle && sidebar) {
        toggle.addEventListener("click", function () {
            sidebar.classList.toggle("open");
        });
    }

    var gold = "#D4AF37";
    var goldSoft = "rgba(212,175,55,0.15)";
    var gridColor = "rgba(255,255,255,0.05)";
    var tickColor = "#999";

    var tooltipOpts = {
        backgroundColor: "#1b1b1b",
        titleColor: "#fff",
        bodyColor: "#ddd",
        borderColor: gold,
        borderWidth: 1,
    };

    var scaleOpts = {
        x: {
            grid: { display: false },
            ticks: { color: tickColor },
        },
        y: {
            beginAtZero: true,
            grid: { color: gridColor },
            ticks: { color: tickColor },
        },
    };

    function readJson(id) {
        var el = document.getElementById(id);
        if (!el) return null;
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            return null;
        }
    }

    var revLabels = readJson("revenue-labels");
    var revValues = readJson("revenue-values");
    var revCanvas = document.getElementById("revenueChart");
    if (revCanvas && revLabels) {
        new Chart(revCanvas, {
            type: "line",
            data: {
                labels: revLabels,
                datasets: [{
                    label: "درآمد",
                    data: revValues,
                    borderColor: gold,
                    backgroundColor: goldSoft,
                    fill: true,
                    tension: 0.35,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: gold,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipOpts },
                scales: scaleOpts,
            },
        });
    }

    var ordLabels = readJson("orders-labels");
    var ordValues = readJson("orders-values");
    var ordCanvas = document.getElementById("ordersChart");
    if (ordCanvas && ordLabels) {
        new Chart(ordCanvas, {
            type: "bar",
            data: {
                labels: ordLabels,
                datasets: [{
                    label: "سفارش‌ها",
                    data: ordValues,
                    backgroundColor: gold,
                    borderRadius: 8,
                    maxBarThickness: 40,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipOpts },
                scales: scaleOpts,
            },
        });
    }

    var osLabels = readJson("order-status-labels");
    var osValues = readJson("order-status-values");
    var osCanvas = document.getElementById("orderStatusChart");
    if (osCanvas && osLabels) {
        new Chart(osCanvas, {
            type: "doughnut",
            data: {
                labels: osLabels,
                datasets: [{
                    data: osValues,
                    backgroundColor: [
                        "#facc15",
                        "#22c55e",
                        "#60a5fa",
                        "#c084fc",
                        "#34d399",
                        "#ef4444",
                    ],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { color: "#ccc", padding: 16 },
                    },
                    tooltip: tooltipOpts,
                },
            },
        });
    }

    var rsLabels = readJson("reservation-status-labels");
    var rsValues = readJson("reservation-status-values");
    var rsCanvas = document.getElementById("reservationStatusChart");
    if (rsCanvas && rsLabels) {
        new Chart(rsCanvas, {
            type: "doughnut",
            data: {
                labels: rsLabels,
                datasets: [{
                    data: rsValues,
                    backgroundColor: ["#facc15", "#22c55e", "#ef4444"],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { color: "#ccc", padding: 16 },
                    },
                    tooltip: tooltipOpts,
                },
            },
        });
    }

    var rtLabels = readJson("rating-labels");
    var rtValues = readJson("rating-values");
    var rtCanvas = document.getElementById("ratingChart");
    if (rtCanvas && rtLabels) {
        new Chart(rtCanvas, {
            type: "bar",
            data: {
                labels: rtLabels,
                datasets: [{
                    data: rtValues,
                    backgroundColor: [
                        "#ef4444",
                        "#f97316",
                        "#facc15",
                        "#84cc16",
                        "#22c55e",
                    ],
                    borderRadius: 6,
                    maxBarThickness: 28,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipOpts },
                scales: scaleOpts,
            },
        });
    }

    var tpLabels = readJson("top-products-labels");
    var tpValues = readJson("top-products-values");
    var tpCanvas = document.getElementById("topProductsChart");
    if (tpCanvas && tpLabels && tpLabels.length) {
        new Chart(tpCanvas, {
            type: "bar",
            data: {
                labels: tpLabels,
                datasets: [{
                    label: "فروش",
                    data: tpValues,
                    backgroundColor: gold,
                    borderRadius: 8,
                    maxBarThickness: 28,
                }],
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipOpts },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: gridColor },
                        ticks: { color: tickColor, precision: 0 },
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: tickColor },
                    },
                },
            },
        });
    }
});
