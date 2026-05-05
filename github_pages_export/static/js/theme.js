(function () {
    const storageKey = "site-theme";
    const defaultTheme = "dark";
    const body = document.body;
    const toggle = document.getElementById("themeToggle");

    if (!body) return;

    function updateThemeIcons(theme) {
        if (!toggle) return;

        const moonIcon = toggle.querySelector(".theme-icon-moon");
        const sunIcon = toggle.querySelector(".theme-icon-sun");
        const darkLabel = toggle.dataset.labelDark || "Dark Mode";
        const lightLabel = toggle.dataset.labelLight || "Light Mode";

        if (theme === "dark") {
            if (moonIcon) moonIcon.classList.add("d-none");
            if (sunIcon) sunIcon.classList.remove("d-none");
            toggle.setAttribute("title", lightLabel);
            toggle.setAttribute("aria-label", lightLabel);
        } else {
            if (sunIcon) sunIcon.classList.add("d-none");
            if (moonIcon) moonIcon.classList.remove("d-none");
            toggle.setAttribute("title", darkLabel);
            toggle.setAttribute("aria-label", darkLabel);
        }
    }

    function applyTheme(theme) {
        const normalizedTheme = theme === "light" ? "light" : "dark";
        body.setAttribute("data-theme", normalizedTheme);
        localStorage.setItem(storageKey, normalizedTheme);
        updateThemeIcons(normalizedTheme);
    }

    const savedTheme = localStorage.getItem(storageKey) || defaultTheme;
    applyTheme(savedTheme);

    if (toggle) {
        toggle.addEventListener("click", function () {
            const currentTheme = body.getAttribute("data-theme") || defaultTheme;
            const nextTheme = currentTheme === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
        });
    }
})();