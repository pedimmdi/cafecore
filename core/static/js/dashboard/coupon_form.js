(function () {
    document.addEventListener("DOMContentLoaded", function () {
        var H = window.CafeJalali;
        if (!H || typeof jalaliDatepicker === "undefined") return;

        function bindDate(displayId, hiddenId, btnId) {
            var display = document.getElementById(displayId);
            var hidden = document.getElementById(hiddenId);
            var btn = document.getElementById(btnId);
            if (!display || !hidden) return;

            if (hidden.value && /^\d{4}-\d{2}-\d{2}$/.test(hidden.value)) {
                var parts = hidden.value.split("-");
                var j = H.gregorianToJalali(+parts[0], +parts[1], +parts[2]);
                display.value = H.faDate(j[0], j[1], j[2]);
            }

            jalaliDatepicker.startWatch({
                selector: "#" + displayId,
                time: false,
                date: true,
                hideAfterChange: true,
                useDropDownYears: true,
                persianDigits: false,
                zIndex: 2147483646,
                minDate: { year: 1400, month: 1, day: 1 },
            });

            function sync() {
                hidden.value = display.value.trim()
                    ? (H.toGregorianStr(display.value) || "")
                    : "";
            }
            function toEn() {
                var p = H.parseJalali(display.value);
                if (p) display.value = H.enDate(p.jy, p.jm, p.jd);
            }
            function toFa() {
                var p = H.parseJalali(display.value);
                if (p) display.value = H.faDate(p.jy, p.jm, p.jd);
            }
            function openPicker() {
                toEn();
                setTimeout(function () {
                    try { jalaliDatepicker.show(display); } catch (e) { display.click(); }
                }, 10);
            }

            if (btn) btn.addEventListener("click", function (e) {
                e.preventDefault();
                openPicker();
            });
            display.addEventListener("click", openPicker);
            ["change", "input", "jdp:change"].forEach(function (ev) {
                display.addEventListener(ev, function () {
                    setTimeout(function () { sync(); toFa(); }, 0);
                });
            });
            document.addEventListener("click", function (e) {
                var day = e.target.closest(".jdp-day");
                if (!day || day.classList.contains("disabled-day")) return;
                if (!display.closest || !document.getElementById(displayId)) return;
                setTimeout(function () { sync(); toFa(); }, 40);
            }, true);

            return { sync: sync, toEn: toEn };
        }

        var from = bindDate("from_date_display", "id_valid_from_date", "fromDateBtn");
        var to = bindDate("to_date_display", "id_valid_to_date", "toDateBtn");

        var form = document.getElementById("couponForm");
        if (form) {
            form.addEventListener("submit", function () {
                if (from) { from.toEn(); from.sync(); }
                if (to) { to.toEn(); to.sync(); }
            });
        }
    });
})();