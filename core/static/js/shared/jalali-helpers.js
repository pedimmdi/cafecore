window.CafeJalali = (function () {
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
        return { jy: +m[1], jm: +m[2], jd: +m[3] };
    }

    function toGregorianStr(text) {
        var p = parseJalali(text);
        if (!p || p.jm < 1 || p.jm > 12 || p.jd < 1 || p.jd > 31) return null;
        var g = jalaliToGregorian(p.jy, p.jm, p.jd);
        return g[0] + "-" + String(g[1]).padStart(2, "0") + "-" + String(g[2]).padStart(2, "0");
    }

    function faDate(jy, jm, jd) {
        return toPersian(jy + "/" + String(jm).padStart(2, "0") + "/" + String(jd).padStart(2, "0"));
    }

    function enDate(jy, jm, jd) {
        return jy + "/" + String(jm).padStart(2, "0") + "/" + String(jd).padStart(2, "0");
    }

    function todayJalaliEn() {
        var n = new Date();
        var j = gregorianToJalali(n.getFullYear(), n.getMonth() + 1, n.getDate());
        return enDate(j[0], j[1], j[2]);
    }

    return {
        toPersian: toPersian,
        toEnglish: toEnglish,
        parseJalali: parseJalali,
        toGregorianStr: toGregorianStr,
        faDate: faDate,
        enDate: enDate,
        gregorianToJalali: gregorianToJalali,
        todayJalaliEn: todayJalaliEn,
    };
})();