(function () {
    document.addEventListener("DOMContentLoaded", function () {
        var H = window.CafeJalali;
        var displayInput = document.getElementById("id_date_of_birth_display");
        var hiddenInput = document.getElementById("id_date_of_birth");
        var btn = document.getElementById("datePickerBtn");
        var form = document.querySelector(".profile-update-card form") || document.querySelector("form");
        var phoneInput = document.getElementById("id_phone_number");

        if (!H) {
            console.error("CafeJalali missing — check jalali-helpers.js");
            return;
        }
        if (typeof jalaliDatepicker === "undefined") {
            console.error("jalaliDatepicker missing — check vendor js path");
            return;
        }
        if (!displayInput || !hiddenInput) {
            console.error("date inputs missing in HTML");
            return;
        }

        // شماره تماس → ارقام فارسی برای نمایش
        if (phoneInput) {
            if (phoneInput.value) phoneInput.value = H.toPersian(phoneInput.value);
            phoneInput.addEventListener("input", function () {
                var pos = this.selectionStart;
                this.value = H.toPersian(H.toEnglish(this.value).replace(/[^\d]/g, ""));
                try { this.setSelectionRange(pos, pos); } catch (e) {}
            });
        }

        // مقدار اولیه تاریخ تولد
        if (hiddenInput.value && /^\d{4}-\d{2}-\d{2}$/.test(hiddenInput.value)) {
            var parts = hiddenInput.value.split("-");
            var j = H.gregorianToJalali(+parts[0], +parts[1], +parts[2]);
            displayInput.value = H.faDate(j[0], j[1], j[2]);
        }

        jalaliDatepicker.startWatch({
            selector: "#id_date_of_birth_display",
            time: false,
            date: true,
            hideAfterChange: true,
            useDropDownYears: true,
            persianDigits: false,
            zIndex: 2147483646,
            // ✅ آبجکت، نه رشته
            minDate: { year: 1300, month: 1, day: 1 },
            maxDate: "today",
        });

        function syncHidden() {
            hiddenInput.value = displayInput.value.trim()
                ? (H.toGregorianStr(displayInput.value) || "")
                : "";
        }

        function toEn() {
            var p = H.parseJalali(displayInput.value);
            if (p) displayInput.value = H.enDate(p.jy, p.jm, p.jd);
            else if (displayInput.value) displayInput.value = H.toEnglish(displayInput.value);
        }

        function toFa() {
            var p = H.parseJalali(displayInput.value);
            if (p) displayInput.value = H.faDate(p.jy, p.jm, p.jd);
        }

        function applyFromDisplay() {
            syncHidden();
            toFa();
        }

        function openPicker() {
            toEn();
            setTimeout(function () {
                try {
                    jalaliDatepicker.show(displayInput);
                } catch (err) {
                    console.error(err);
                    displayInput.focus();
                    displayInput.click();
                }
            }, 10);
        }

        if (btn) {
            btn.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                openPicker();
            });
        }

        displayInput.addEventListener("click", function () {
            openPicker();
        });

        ["change", "input", "jdp:change"].forEach(function (ev) {
            displayInput.addEventListener(ev, function () {
                setTimeout(applyFromDisplay, 0);
            });
        });

        document.addEventListener(
            "click",
            function (e) {
                var day = e.target.closest(".jdp-day");
                if (!day) return;
                if (day.classList.contains("disabled-day")) return;
                setTimeout(applyFromDisplay, 40);
            },
            true
        );

        if (form) {
            form.addEventListener("submit", function () {
                if (phoneInput) phoneInput.value = H.toEnglish(phoneInput.value);
                toEn();
                syncHidden();
            });
        }
    });
})();