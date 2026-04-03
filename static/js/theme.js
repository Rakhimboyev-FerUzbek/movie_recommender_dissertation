(function () {
    const storageKey = "site-theme";
    const defaultTheme = "dark";
    const body = document.body;
    const toggle = document.getElementById("themeToggle");

    if (!body) return;

    function updateToggleLabel(theme) {
        if (!toggle) return;

        const label = toggle.querySelector(".theme-toggle-label");
        const darkLabel = toggle.dataset.labelDark || "Dark Mode";
        const lightLabel = toggle.dataset.labelLight || "Light Mode";

        const nextLabel = theme === "dark" ? lightLabel : darkLabel;

        if (label) {
            label.textContent = nextLabel;
        }

        toggle.setAttribute("aria-label", nextLabel);
        toggle.setAttribute("title", nextLabel);
    }

    function applyTheme(theme) {
        const normalizedTheme = theme === "light" ? "light" : "dark";
        body.setAttribute("data-theme", normalizedTheme);
        localStorage.setItem(storageKey, normalizedTheme);
        updateToggleLabel(normalizedTheme);
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