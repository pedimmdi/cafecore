(function () {
    function toPersian(str) {
        return String(str ?? "").replace(/\d/g, function (d) {
            return "۰۱۲۳۴۵۶۷۸۹"[d];
        });
    }

    function toEnglish(str) {
        return String(str ?? "")
            .replace(/[۰-۹]/g, function (d) {
                return "۰۱۲۳۴۵۶۷۸۹".indexOf(d);
            })
            .replace(/[٠-٩]/g, function (d) {
                return "٠١٢٣٤٥٦٧٨٩".indexOf(d);
            });
    }

    function jalaliToGregorian(jy, jm, jd) {
        var jy2 = jy - 979, jm2 = jm - 1, jd2 = jd - 1;
        var j_day_no =
            365 * jy2 +
            Math.floor(jy2 / 33) * 8 +
            Math.floor(((jy2 % 33) + 3) / 4);
        for (var i = 0; i < jm2; ++i) j_day_no += i < 6 ? 31 : 30;
        j_day_no += jd2;
        var g_day_no = j_day_no + 79;
        var gy = 1600 + 400 * Math.floor(g_day_no / 146097);
        g_day_no %= 146097;
        var leap = true;
        if (g_day_no >= 36525) {
            g_day_no--;
            gy += 100 * Math.floor(g_day_no / 36524);
            g_day_no %= 36524;
            if (g_day_no >= 365) g_day_no++;
            else leap = false;
        }
        gy += 4 * Math.floor(g_day_no / 1461);
        g_day_no %= 1461;
        if (g_day_no >= 366) {
            leap = false;
            g_day_no--;
            gy += Math.floor(g_day_no / 365);
            g_day_no %= 365;
        }
        var sal_a = [0, 31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        var gm = 0;
        while (gm < 13 && g_day_no >= sal_a[gm]) {
            g_day_no -= sal_a[gm];
            gm++;
        }
        return [gy, gm, g_day_no + 1];
    }

    function gregorianToJalali(gy, gm, gd) {
        var g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
        var gy2 = gm > 2 ? gy + 1 : gy;
        var days =
            355666 +
            365 * gy +
            Math.floor((gy2 + 3) / 4) -
            Math.floor((gy2 + 99) / 100) +
            Math.floor((gy2 + 399) / 400) +
            gd +
            g_d_m[gm - 1];
        var jy = -1595 + 33 * Math.floor(days / 12053);
        days %= 12053;
        jy += 4 * Math.floor(days / 1461);
        days %= 1461;
        if (days > 365) {
            jy += Math.floor((days - 1) / 365);
            days = (days - 1) % 365;
        }
        var jm, jd;
        if (days < 186) {
            jm = 1 + Math.floor(days / 31);
            jd = 1 + (days % 31);
        } else {
            jm = 7 + Math.floor((days - 186) / 30);
            jd = 1 + ((days - 186) % 30);
        }
        return [jy, jm, jd];
    }

    function parseJalali(text) {
        var eng = toEnglish(text).trim();
        var m = eng.match(/^(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})$/);
        if (!m) return null;
        return {
            jy: parseInt(m[1], 10),
            jm: parseInt(m[2], 10),
            jd: parseInt(m[3], 10),
        };
    }

    function toGregorianStr(text) {
        var p = parseJalali(text);
        if (!p || p.jm < 1 || p.jm > 12 || p.jd < 1 || p.jd > 31) return null;
        var g = jalaliToGregorian(p.jy, p.jm, p.jd);
        return (
            g[0] +
            "-" +
            String(g[1]).padStart(2, "0") +
            "-" +
            String(g[2]).padStart(2, "0")
        );
    }

    function faDate(jy, jm, jd) {
        return toPersian(
            jy + "/" + String(jm).padStart(2, "0") + "/" + String(jd).padStart(2, "0")
        );
    }

    function enDate(jy, jm, jd) {
        return jy + "/" + String(jm).padStart(2, "0") + "/" + String(jd).padStart(2, "0");
    }

    document.addEventListener("DOMContentLoaded", function () {
        var phoneInput = document.getElementById("id_phone_number");
        var displayInput = document.getElementById("id_date_of_birth_display");
        var hiddenInput = document.getElementById("id_date_of_birth");
        var btn = document.getElementById("datePickerBtn");
        var form =
            document.querySelector(".profile-update-card form") ||
            document.querySelector("form");

        if (phoneInput) {
            if (phoneInput.value) phoneInput.value = toPersian(phoneInput.value);
            phoneInput.addEventListener("input", function () {
                var pos = this.selectionStart;
                this.value = toPersian(toEnglish(this.value).replace(/[^\d]/g, ""));
                try { this.setSelectionRange(pos, pos); } catch (e) {}
            });
        }

        if (!displayInput || !hiddenInput) return;

        if (hiddenInput.value) {
            var parts = hiddenInput.value.split("-");
            if (parts.length === 3) {
                var j = gregorianToJalali(+parts[0], +parts[1], +parts[2]);
                displayInput.value = faDate(j[0], j[1], j[2]);
            }
        }

        if (typeof jalaliDatepicker === "undefined") {
            console.error("jalaliDatepicker not loaded");
            return;
        }

        jalaliDatepicker.startWatch({
            time: false,
            date: true,
            hideAfterChange: true,
            useDropDownYears: true,
            persianDigits: false,
            zIndex: 100000,
            maxDate: "today",
            minDate: "1300/01/01",
        });

        function syncHidden() {
            hiddenInput.value = displayInput.value.trim()
                ? toGregorianStr(displayInput.value) || ""
                : "";
        }

        function toEnglishInInput() {
            var p = parseJalali(displayInput.value);
            if (p) displayInput.value = enDate(p.jy, p.jm, p.jd);
            else if (displayInput.value)
                displayInput.value = toEnglish(displayInput.value);
        }

        function toPersianInInput() {
            var p = parseJalali(displayInput.value);
            if (p) displayInput.value = faDate(p.jy, p.jm, p.jd);
            else if (displayInput.value)
                displayInput.value = toPersian(toEnglish(displayInput.value));
        }

        function openPicker() {
            toEnglishInInput();
            if (typeof jalaliDatepicker.show === "function") {
                jalaliDatepicker.show(displayInput);
            } else {
                displayInput.focus();
                displayInput.click();
            }
        }

        if (btn) {
            btn.addEventListener("click", function (e) {
                e.preventDefault();
                openPicker();
            });
        }

        // بعد از انتخاب روز توسط کتابخانه
        displayInput.addEventListener("change", function () {
            syncHidden();
            toPersianInInput();
        });

        // تایپ دستی — بدون دستکاری focus/blur
        displayInput.addEventListener("input", function () {
            var pos = this.selectionStart;
            this.value = toEnglish(this.value).replace(/[^\d\/\-]/g, "");
            try { this.setSelectionRange(pos, pos); } catch (e) {}
            syncHidden();
        });

        if (form) {
            form.addEventListener("submit", function () {
                if (phoneInput) phoneInput.value = toEnglish(phoneInput.value);
                toEnglishInInput();
                syncHidden();
            });
        }
    });
})();