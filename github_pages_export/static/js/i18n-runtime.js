// static/js/i18n-runtime.js
// Key-based runtime translation helper for dynamic JavaScript messages only.
// This file does not scan or replace DOM text.
(function () {
    "use strict";

    const script = document.getElementById("js-i18n-data");
    let messages = {};

    if (script) {
        try {
            messages = JSON.parse(script.textContent || "{}");
        } catch (error) {
            console.error("Invalid js-i18n-data JSON:", error);
            messages = {};
        }
    }

    window.t = function (key, fallback) {
        return messages[key] || fallback || key;
    };

    window.getI18nMessages = function () {
        return Object.assign({}, messages);
    };
})();
